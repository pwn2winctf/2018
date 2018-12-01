const Rank = Vue.component('rank', {
    template: `
        <div>
            <app-title v-if="!hideTitle" title="Rank"></app-title>
            <!--<div v-if="!hideTitle">
                <canvas id="chart"></canvas>
            </div>-->
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
        userTeam: Cookies.get('team'),
        chart: null
    }),
    methods: {
        getTeamFlagUrl: country => `https://cdnjs.cloudflare.com/ajax/libs/flag-icon-css/${settings.flag_icon_css_ver || '2.8.0'}/flags/4x3/${country}.svg`,
        startChart: function(data) {
            this.chart = new Chart($('#chart'), {
                "type":"line",
                "data": {
                    "labels":["January","February","March","April","May","June","July"],
                    "datasets":[
                        {
                            "label":"My First Dataset",
                            "data":[65,59,80,81,56,55,40],
                            "fill":false,
                            "borderColor":"rgb(75, 192, 192)",
                            "lineTension":0.1
                        }
                    ]
                },
                "options": {}
            });
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
            this.startChart();
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
