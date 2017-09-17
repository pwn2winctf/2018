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
            }, intervalTime || 10000);
        },
        stop () {
            this.isStarted = false
            clearInterval(interval);
        }
    }
};

const getSubmisionsPath = () => settings.submissions_project.split('/')[1];

const getSettings = () => $.getJSON('settings.json');
const getNews = () => $.getJSON('submissions/news.json');
const getChallenges = () => $.getJSON('challenges/index.json');
const getChallenge = (id) => $.getJSON(`challenges/${id}.json`);
const getSolvedChallenges = () => $.getJSON(`/${getSubmisionsPath()}/accepted-submissions.json`);
const getTeam = hash => $.getJSON(`/${getSubmisionsPath()}/${hash}/team.json`);
const getTeamMembers = hash => $.getJSON(`/${getSubmisionsPath()}/${hash}/members.json`);

String.prototype.splice = function(idx, rem, str) {
    return this.slice(0, idx) + str + this.slice(idx + Math.abs(rem));
};