const Team = Vue.component('team', {
    template: `
        <div>
            <div v-if="loaded && team">
                <h4>{{team.name}}</h4>
                <p><strong>{{$t('position')}}:</strong> {{teamRank.pos}}</p>
                <p><strong>{{$t('score')}}:</strong> {{teamRank.score}}</p>
                <p><strong>Crypt PK:</strong> {{team.crypt_pk}}</p>
                <p><strong>Sign PK:</strong> {{team.sign_pk}}</p>
                <h5>{{$t('members')}}</h5>
                <ul class="rank collection z-depth-1">
                    <li class="collection-item" v-for="(member, index) in members">
                        {{index + 1}}. {{member.username}}
                    </li>
                </ul>
                <h5>{{$t('solved-challenges')}}</h5>
                <ul class="rank collection z-depth-1">
                    <li class="collection-item" v-for="(chall, key, index) in teamRank.taskStats">
                        {{index + 1}}. {{key}}
                    </li>
                </ul>
            </div>
            <div v-if="loaded && !team">
                <h4 class="header center">404 - Team "{{$route.params.name}}" not found</h4>
            </div>
        </div>
    `,
    data: () => ({
        loaded: false
    }),
    methods: {
        loadTeam: async function(teamName) {
            return getTeam(teamName);
        },
        loadMembers: async function(teamName) {
            return getTeamMembers(teamName);
        },
        loadTeamRank: async function(teamName) {
            const solvedChallenges = await getSolvedChallenges()
            return solvedChallenges.standings.filter(teamRank => teamRank.team === teamName)[0];  
        }
    },
    mounted: async function() {
        await Promise.all([
            this.loadTeamRank(this.$route.params.name)
                .then(teamRank => { this.teamRank = teamRank }),
            this.loadTeam(this.$route.params.name)
                .then(team => { this.team = team }),
            this.loadMembers(this.$route.params.name)
                .then(members => { this.members = members })
        ]);
        this.loaded = true;
    }
});
