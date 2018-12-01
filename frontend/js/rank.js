const Rank = Vue.component('rank', {
    template: `
        <div>
            <app-title v-if="!hideTitle" title="Rank"></app-title>
            <div class="center" v-if="!hideTitle">
                <img id="chart" alt="Chart" />
            </div>
            <ul class="rank collection z-depth-1">
                <li v-bind:class="{ 'team-selected': userTeam === team.team }" v-on:click="teamClick(team.team)" class="clickable collection-item" v-for="team in rank">
                    <div>{{team.pos}}. {{team.team}}
                        <div style="width: 50px; text-align: center;" class="secondary-content">{{team.score}}</div>
                        <div v-if="!hideTitle" class="secondary-content">
                            <img class="country-flag" v-for="country in team.countries" v-bind:src="getTeamFlagUrl(country)">
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    `,
    data: () => ({
        rank: [],
        teams: {},
        userTeam: Cookies.get('team')
    }),
    methods: {
        getTeamFlagUrl: country => `https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/${settings.flag_icon_css_ver || '2.8.0'}/flags/4x3/${country}.svg`,
        loadChart: function(data) {
            $('#chart').attr('src', data);
        },
        loadTeam: async function(teamName) {
            if (!this.teams[teamName]) {
                this.teams[teamName] = await getTeam(teamName);
            }

            return this.teams[teamName];
        },
        loadRank: function(acceptedSubmissions) {
            this.rank = acceptedSubmissions.standings.filter((team, i) => i < (this.limit || acceptedSubmissions.standings.length));
            this.rank.forEach(async (rank, index) => {
                this.rank.splice(index, 1, Object.assign({}, rank, {
                    countries: (await this.loadTeam(rank.team)).countries
                }));
            })
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
        this.chartPolling = createPooling(
            getChart,
            this.loadChart
        );
        this.chartPolling.start();
    },
    beforeDestroy: function() {
        this.rankPolling.stop();
        this.chartPolling.stop();
    }
});
