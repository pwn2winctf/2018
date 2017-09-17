const News = Vue.component('news', {
    template: `
        <div class="news z-depth-1">
            <div class="col s12">
            <ul class="tabs">
                <li class="tab col s3">
                    <a class="active" href="#test1">
                        <div>Messages <div class="chip">{{news.length}}</div></div>
                    </a>
                </li>
                <li class="tab col s3">
                    <a href="#test2">
                        <div>Solves <div class="chip">{{solves.length}}</div></div>
                    </a>
                </li>
            </ul>
            </div>
            <div id="test1" class="col s12">
                <div v-for="singleNews in news">[ {{formatDate(singleNews.time)}} ] admin: {{singleNews.msg}}</div>
            </div>
            <div id="test2" class="col s12">
                <div v-for="solve in solves">[ {{formatDate(solve.time)}} ] {{solve.team}} solved {{solve.chall}}</div>
            </div>
        </div>
    `,
    data: () => ({
        title: "Home",
        news: [],
        solves: []
    }),
    methods: {
        formatDate: date => moment(date).format('DD-MM-YYYY HH:mm:ss'),
        loadNews: function(news) {
            this.news = news;
        },
        setChallengesSolves: function(acceptedSubmissions) {
            this.solves = acceptedSubmissions.standings.reduce((reducer, { taskStats, team }) => {
                Object.keys(taskStats).forEach(chall => {
                    reducer.push({
                        team,
                        chall,
                        time: taskStats[chall].time
                    });
                });
                return reducer;
            }, [])
            .sort((solveA, solveB) => solveA <= solveB);
        }
    },
    mounted: function() {
        $('ul.tabs').tabs();
        this.newsPolling = createPooling(
            getNews,
            this.loadNews
        );
        this.newsPolling.start();

        this.submissionsPolling = createPooling(
            getSolvedChallenges,
            this.setChallengesSolves
        );
        this.submissionsPolling.start();
    },
    beforeDestroy: function() {
        this.newsPolling.stop();
        this.submissionsPolling.stop();
    }
});

const Home = {
    template: `
        <div>
            <app-title title="Home"></app-title>
            <div class="row news-rank-row">
                <div class="col s8">
                    <h5>News</h5>
                    <news></news>
                </div>
                <div class="col s4">
                    <h5>Rank</h5>
                    <rank :hideTitle=true :limit=5></rank>
                </div>
            </div>
            <div class="row">
                <div class="col s12">
                    <h5>Challenges</h5>
                    <challenges :hideTitle=true></challenges>
                </div>
            </div>
        </div>
    `,
    mounted: () => {
        title = "Home";
    },

}
