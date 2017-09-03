const ChallengeComponent = Vue.component('challenge-card', {
    template: `
        <div class="col s12 m4">
            <div class="card blue-grey darken-1">
                <div class="card-content white-text">
                    <span class="card-title">{{challenge.title}}
                        <span class="new badge red" data-badge-caption="points">{{challenge.points}}</span>
                    </span>
                    <p>{{challenge.description.substr(0,100)}}...</p>
                    <p>
                        <span v-for="tag in challenge.tags" class="new badge" data-badge-caption="">{{tag}}</span>
                    </p>
                    <p>{{challenge.solves}}</p>
                </div>
                <div class="card-action">
                    <a class="waves-effect waves-light btn" href="# + challenge.id + ">More</a>
                </div>
            </div>
        </div>
    `,
    props: ['challenge']
});

const Challenges = Vue.component('challenges', {
    template: `
        <div class="row">
            <app-title v-if="!hideTitle" title="Challenges"></app-title>
            <div v-for="challenge in challenges">
                <challenge-card :challenge="challenge" />
            </div>
        </div>
    `,
    data: () => ({
        challenges: []
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
            solves = acceptedSubmissions.reduce((reducer, { chall }) => {
                reducer[chall]++ || (reducer[chall] = 1)
                return reducer;
            }, {});

            this.challenges.forEach((challenge, index) => {
                this.challenges.splice(index, 1, Object.assign({}, challenge, { solves: solves[challenge.id] || 0 }));
            });
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
