const News = Vue.component('news', {
    template: `
        <div class="news z-depth-1">
            <div v-for="singleNews in news">[ {{formatDate(singleNews.time)}} ] admin: {{singleNews.msg}}</div>
        </div>
    `,
    data: () => ({
        title: "Home",
        news: []
    }),
    methods: {
        formatDate: date => moment(date).format('DD-MM-YYYY HH:mm:ss'),
        loadNews: function(news) {
            this.news = news;
        }
    },
    mounted: function() {
        this.newsPolling = createPooling(
            getNews,
            this.loadNews
        );
        this.newsPolling.start();
    },
    beforeDestroy: function() {
        this.newsPolling.stop();
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
