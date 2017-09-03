$.ajaxSetup({ cache: false });

const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/challenges',
        component: Challenges
    },
    {
        path: '/rank',
        component: Rank
    }
];

const router = new VueRouter({
    routes
});

const Title = Vue.component('app-title', {
    template: `
    <div class="section no-pad-bot" id="index-banner">
      <div class="container">
        <h4 class="header center orange-text">{{title}}</h4>
      </div>
    </div>
    `,
    props: ['title']
})

const app = new Vue({
    router,
    data: () => ({
        loaded: false
    }),
    async mounted() {
        settings = await getSettings();
        this.loaded = true;
    }
}).$mount('#app');
