const createPooling = (promise, cb, intervalTime) => {
    let interval;
    return {
        isStarted: false,
        async start() {
            if (this.isStarted) {
                return;
            }

            this.isStarted = true;

            cb(await promise());
            interval = setInterval(async () => {
                cb(await promise());
            }, intervalTime || 60000);
        },
        stop () {
            this.isStarted = false
            clearInterval(interval);
        }
    }
};

const converter = new showdown.Converter();
const getSubmisionsPath = () => settings.submissions_project.split('/')[1];
const getTeamPath = teamName => sha256(teamName).splice(1, 0, '/').splice(5, 0, '/');
const mountUrl = (path, time = (1000 * 60 * 10)) => `${path}?_${Math.floor(+(new Date)/time)}`

const getSettings = () => $.getJSON('settings.json');
const getNews = () => $.getJSON(mountUrl(`/${getSubmisionsPath()}/news.json`));
const getChallenges = () => $.getJSON(mountUrl('challenges/index.json'));
const getChallenge = id => $.getJSON(mountUrl(`challenges/${id}.json`));
const getChallengeDescription = (id, lang) => $.get(mountUrl(`challenges/${id}.${lang.toLowerCase()}.md`));
const getSolvedChallenges = () => $.getJSON(mountUrl(`/${getSubmisionsPath()}/accepted-submissions.json`, 1000 * 60));
const getChart = () => mountUrl("https://cloud.ufscar.br:8080/v1/AUTH_c93b694078064b4f81afd2266a502511/charts/top.svg", 1000 * 60);
const getTeam = teamName => $.getJSON(mountUrl(`/${getSubmisionsPath()}/${getTeamPath(teamName)}/team.json`));
const getTeamMembers = teamName => $.getJSON(mountUrl(`/${getSubmisionsPath()}/${getTeamPath(teamName)}/members.json`));
const getLocaleMessages = lang => $.getJSON(mountUrl(`frontend/locales/${lang}.json`));

String.prototype.splice = function(idx, rem, str) {
    return this.slice(0, idx) + str + this.slice(idx + Math.abs(rem));
};
