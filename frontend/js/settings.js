const Settings = Vue.component('settings', {
    template: `
        <div>
            <app-title title="settings"></app-title>
            <p><strong>{{$t('team')}}:</strong> <input v-model="team" placeholder="Team name"></p>
            <p>
                <strong>{{$t('language')}}:</strong>
                <select v-model="language">
                    <option>En</option>
                    <option>Pt</option>
                </select>
            </p>
            <a class="waves-effect waves-light btn" v-on:click="save">Save</a>
        </div>
    `,
    data: () => ({
        team: Cookies.get('team'),
        language: Cookies.get('lang') || 'En'
    }),
    methods: {
        save() {
            const lang = $('select').val();
            Cookies.set('team', this.team);
            Cookies.set('lang', lang);
            app.$i18n.locale = lang;
        }
    },
    mounted() {
        $(document).ready(function() {
            $('select').material_select();
        });
    }
});
