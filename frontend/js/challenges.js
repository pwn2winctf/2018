const ChallengeModal = Vue.component('challenge-modal', {
    template: `
        <div id="modal1" class="modal">
            <div class="modal-content">
                <h4>{{challenge.title}}</h4>
                <p>{{challenge.description}}</p>
                <p>Total solves: {{challenge.solves}}</p>
                <p>Points: {{challenge.points}}</p>
                <p>Categories: {{challenge.tags.join(', ')}}</p>
            </div>
            <div class="modal-footer">
                <button class="modal-action modal-close waves-effect waves-green btn-flat">Close</button>
            </div>
        </div>
    `,
    props: ['challenge'],
    mounted: function() {
        $('.modal').modal();
    }
})

const ChallengeComponent = Vue.component('challenge-card', {
    template: `
        <div v-on:click="selectChallenge" class="col s12 m4">
            <div class="clickable card blue-grey darken-1">
                <div class="card-content white-text">
                    <span class="card-title">{{challenge.title}}</span>
                    <div class="row"><strong>Total solves:</strong> {{challenge.solves}}</div>
                </div>
                <div class="card-action">
                    <div class="row"><span v-for="tag in challenge.tags" class="new badge" data-badge-caption="">{{tag}}</span></div>
                    <div class="row"><span class="new badge red" data-badge-caption="points">{{challenge.points}}</span></div>
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
            <app-title v-if="!hideTitle" title="Challenges"></app-title>
            <div v-for="challenge in challenges">
                <challenge-card :selectChallengeFunction="openModal" :challenge="challenge" />
            </div>
            <div v-if="selectedChallenge">
                <challenge-modal :challenge="selectedChallenge"/>
            </div>
        </div>
    `,
    data: () => ({
        challenges: [],
        selectedChallenge: null
    }),
    props: ['hideTitle', 'submissions'],
    watch: {
        submissions: function(submissions) {
            this.setChallengesSolves(submissions);
        }
    },
    methods: {
        loadChallenges: async function(challengeList) {
            const mountChallPromise = (challId, index) => getChallenge(challId)
                .then(chall => this.challenges.splice(index, 0, chall));

            const challPromiseMap = challList => challList
                .filter(chall => this.challenges.map(c => c.id).indexOf(chall) < 0)
                .map(mountChallPromise);

            await Promise.all(challPromiseMap(challengeList));
            if (!this.submissions && !this.submissionsPolling.isStarted) {
                this.submissionsPolling.start();
            }
        },
        setChallengesSolves: function(acceptedSubmissions) {
            solves = acceptedSubmissions.standings.reduce((reducer, { taskStats }) => {
                Object.keys(taskStats).forEach(chall => {
                    reducer[chall]++ || (reducer[chall] = 1)
                });
                return reducer;
            }, {});

            this.challenges.forEach((challenge, index) => {
                this.challenges.splice(index, 1, Object.assign({}, challenge, { solves: solves[challenge.id] || 0 }));
            });
        },
        openModal: function(challenge) {
            this.selectedChallenge = challenge;
            Vue.nextTick(() => {
                $('.modal').modal('open');
            })
        }
    },
    mounted: function() {
        this.challengesPolling = createPooling(
            getChallenges,
            this.loadChallenges
        );
        this.challengesPolling.start();

        this.submissionsPolling = createPooling(
            getSolvedChallenges,
            this.setChallengesSolves
        );
        title = 'Challenges';
    },
    beforeDestroy: function() {
        this.challengesPolling.stop();
        this.submissionsPolling.stop();
    }
});
