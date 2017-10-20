const ChallengeModal = Vue.component('challenge-modal', {
    template: `
        <div id="modal1" class="modal">
            <div class="modal-content">
                <h4>{{challenge.title}}</h4>
                <p v-html="challenge.description"></p>
                <p><strong>{{$t('total-solves')}}:</strong> {{challenge.solves}}</p>
                <p><strong>{{$t('score')}}:</strong> {{challenge.points}}</p>
                <p><strong>{{$t('categories')}}:</strong> {{challenge.tags.join(', ')}}</p>
            </div>
            <div class="modal-footer">
                <button class="modal-action modal-close waves-effect waves-green btn-flat">Close</button>
            </div>
        </div>
    `,
    props: ['challenge'],
    data: () => ({
        loaded: false,
        descriptionMap: {}
    }),
    methods: {
        loadDescription: async function(challenge) {
            const lang = Cookies.get('lang').toLowerCase();

            if (!this.descriptionMap[lang]) {
                this.descriptionMap[lang] = {};
            }

            if (this.descriptionMap[lang][challenge.id]) {
                this.challenge.description = this.descriptionMap[lang][challenge.id];
                return;
            }

            const challengeMd = await getChallengeDescription(this.challenge.id, lang);
            this.descriptionMap[lang][challenge.id] = converter.makeHtml(challengeMd);
            this.challenge.description = this.descriptionMap[lang][challenge.id];
        },
    },
    mounted: async function() {
        $('.modal').modal();
        this.loadDescription(this.challenge);
    },
    watch: {
        challenge: function(challenge) {
            thisloaded = false
            this.loadDescription(challenge);
        }
    },
})

const ChallengeComponent = Vue.component('challenge-card', {
    template: `
        <div v-on:click="selectChallenge" class="col s12 m4">
            <div v-bind:class="{ 'is-solved': challenge.solved }" class="clickable card blue-grey darken-1">
                <div class="card-content white-text">
                    <span class="card-title">{{challenge.title}}</span>
                    <div class="row"><strong>{{$t('total-solves')}}:</strong> {{challenge.solves}}</div>
                    <div class="row"><strong>{{$t('score')}}:</strong> {{challenge.points}}</div>
                </div>
                <div class="card-action">
                    <div class="row">
                        <span v-if="challenge.optional" class="new badge red" data-badge-caption="">{{$t(challenge.optional)}}</span>
                        <span v-for="tag in challenge.tags" class="new badge" data-badge-caption="">{{tag}}</span>
                    </div>
                </div>
            </div>
        </div>
    `,
    props: ['challenge', 'selectChallengeFunction'],
    methods: {
        selectChallenge: function() {
            this.selectChallengeFunction(this.challenge);
        }
    }
});

const Challenges = Vue.component('challenges', {
    template: `
        <div class="row">
            <app-title v-if="!hideTitle" title="challenges"></app-title>
            <div v-if="loaded" class="row categories">
                <span v-bind:class="{green: category === selectedCategory}" v-for="category in categories" class="new badge" data-badge-caption="" v-on:click="selectCategory(category)">{{category}}</span>
            </div>
            <div v-if="loaded" v-for="challenge in filteredChallenges">
                <challenge-card :selectChallengeFunction="openModal" :challenge="challenge" />
            </div>
            <div v-if="selectedChallenge">
                <challenge-modal :challenge="selectedChallenge"/>
            </div>
        </div>
    `,
    data: () => ({
        loaded: false,
        challenges: [],
        selectedChallenge: null,
        categories: [],
        filteredChallenges: [],
        selectedCategory: null
    }),
    props: ['hideTitle', 'submissions'],
    watch: {
        submissions: function(submissions) {
            this.loadSubmissions(submissions);
        }
    },
    methods: {
        selectCategory: function(category) {
            if (this.selectedCategory === category) {
                this.selectedCategory = null;
                this.filteredChallenges = this.challenges;
                return;
            }

            this.selectedCategory = category;
            this.filteredChallenges = this.challenges.filter(challenge => challenge.tags.indexOf(category) >= 0);
        },
        loadChallenges: async function(challengeList) {
            const mountChallPromise = (challId, index) => getChallenge(challId)
                .then(chall => this.challenges.splice(index, 0, chall));

            const challPromiseMap = challList => challList
                .filter(chall => this.challenges.map(c => c.id).indexOf(chall) < 0)
                .map(mountChallPromise);
            
            await Promise.all(challPromiseMap(challengeList));
            const categories = new Set();
            this.challenges.forEach(challenge => {
                challenge.tags.forEach(category => {
                    categories.add(category);
                });
            })
            this.categories = [...categories];
            this.challenges = this.challenges.sort((challA, challB) => challA.title.localeCompare(challB.title))
            this.filteredChallenges = this.challenges;
            
            if (!this.submissions && !this.submissionsPolling.isStarted) {
                this.submissionsPolling.start();
            }
            this.loaded = true
        },
        loadSubmissions: function(acceptedSubmissions) {
            const userTeam = Cookies.get('team');
            let teamSolves = new Set();
            solves = acceptedSubmissions.standings.reduce((reducer, { taskStats, team }) => {
                Object.keys(taskStats).forEach(chall => {
                    reducer[chall]++ || (reducer[chall] = 1)
                });

                if (userTeam && userTeam === team) {
                    teamSolves = new Set(Object.keys(taskStats));
                }
                return reducer;
            }, {});

            this.challenges.forEach((challenge, index) => {
                this.challenges.splice(index, 1, Object.assign({}, challenge, {
                    solves: solves[challenge.id] || 0,
                    points: this.calculatePoints(solves[challenge.id]),
                    solved: teamSolves.has(challenge.id)
                }));
            });
        },
        calculatePoints: function(solves) {
            const { K, V, minpts, maxpts } = settings['dynamic_scoring'];
            return parseInt(Math.max(minpts, Math.floor(maxpts - K * Math.log2(((solves + 1 || 1) + V)/(1 + V)))))
        },
        openModal: function(challenge) {
            this.selectedChallenge = challenge;
            Vue.nextTick(() => {
                $('.modal').modal('open');
            })
        }
    },
    mounted: async function() {
        this.loadChallenges(await getChallenges());
        this.submissionsPolling = createPooling(
            getSolvedChallenges,
            this.loadSubmissions
        );
        title = 'Challenges';
    },
    beforeDestroy: function() {
        this.challengesPolling.stop();
        this.submissionsPolling.stop();
    }
});
