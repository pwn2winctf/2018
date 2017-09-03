const Rank = Vue.component('rank', {
    template: `
        <div>
            <app-title v-if="!hideTitle" title="Rank"></app-title>
            <ul class="rank collection z-depth-1">
                <li class="collection-item" v-for="(team, index) in rank">
                    <div>{{index + 1}}. {{team.name}}
                        <div class="secondary-content">{{team.totalPoints}}</div>
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
            const mapTeamsByHash = acceptedSubmissions => acceptedSubmissions
                .reduce((reducer, submission) => {
                    if (!reducer[submission.team]) {
                        reducer[submission.team] = {
                            hash: submission.team,
                            totalPoints: 0,
                            solvedChalls: []
                        }
                    }

                    reducer[submission.team].totalPoints += submission.points;
                    reducer[submission.team].solvedChalls.push({
                        name: submission.chall,
                        points: submission.points,
                        time: submission.time
                    })
                    return reducer;
                }, {});
            const rank = mapTeamsByHash(acceptedSubmissions);
            this.rank = Object.keys(mapTeamsByHash(acceptedSubmissions))
                .sort((a, b) => rank[a].totalPoints < rank[b].totalPoints)
                .slice(0, this.limit)
                .map(key => rank[key]);

            this.rank.forEach(async (rankTeam, index) => {
                if (rankTeam.name) {
                    return;
                }

                const team = await this.loadTeam(rankTeam.hash)
                this.rank.splice(index, 1, Object.assign({}, rankTeam, { name: team.name }));
            });
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
