Vue.use(VueI18n);
if (!Cookies.get('lang')) {
    Cookies.set('lang', 'En');
}
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
    },
    {
        path: '/team/:name',
        component: Team
    },
    {
        path: '/settings',
        component: Settings
    }
];

const router = new VueRouter({
    routes
});

const Title = Vue.component('app-title', {
    template: `
    <div class="section no-pad-bot" id="index-banner">
      <div class="container">
        <h4 class="header center orange-text">{{$t(title)}}</h4>
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
    },
    i18n: new VueI18n({
        locale: Cookies.get('lang'),
        fallbackLocale: 'En',
        messages: {
            En: enLocale,
            Pt: ptLocale
        } 
    })
}).$mount('#app');
