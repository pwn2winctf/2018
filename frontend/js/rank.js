const Rank = Vue.component('rank', {
    template: `
        <div>
            <app-title v-if="!hideTitle" title="Rank"></app-title>
            <ul class="rank collection z-depth-1">
                <li v-on:click="teamClick(team.team)" class="clickable collection-item" v-for="team in rank">
                    <div>{{team.pos}}. {{team.team}}
                        <div class="secondary-content">{{team.score}}</div>
                    </div>
                </li>
            </ul>
        </div>
    `,
    data: () => ({
        rank: [],
        teams: {}
    }),
    methods: {
        loadTeam: async function(hash) {
            if (!this.teams[hash]) {
                this.teams[hash] = await getTeam(hash);
            }

            return this.teams[hash];
        },
        loadRank: function(acceptedSubmissions) {
            this.rank = acceptedSubmissions.standings;
        },
        teamClick: function(teamName) {
            this.$router.push({ path: `/team/${teamName}` });
        }
    },
    props: ['limit', 'hideTitle'],
    mounted: function() {
        this.rankPolling = createPooling(
            getSolvedChallenges,
            this.loadRank
        );
        this.rankPolling.start();
    },     
    beforeDestroy: function() {
        this.rankPolling.stop();
    }
});
