const ChallengeComponent = Vue.component('challenge-card', {
    template: `
        <div class="col s12 m4">
            <div class="card blue-grey darken-1">
                <div class="card-content white-text">
                    <span class="card-title">{{challenge.title}}</span>
                    <p>{{challenge.description.substr(0,100)}}...</p>
                    <p>
                        <span v-for="tag in challenge.tags" class="new badge" data-badge-caption="">{{tag}}</span>
                    </p>
                </div>
                <div class="card-action">
                    <a class="waves-effect waves-light btn" href="# + challenge.id + ">More</a>
                </div>
            </div>
        </div>
    `,
    props: ['challenge']
});

const Challenges = {
    template: `
        <div class="row">
            <challenge-card v-for="challenge in challenges" :challenge="challenge" />
        </div>
    `,
    data: () => ({
        challenges
    })
}
