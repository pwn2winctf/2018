(function(_) {
    _.nizkctf = {};

    var challengesDiv = $('#challenges');

    var challengeTpl = function(challenge) {
        var tags = challenge.tags.map(function(tag){
            return '<span class="new badge" data-badge-caption="">' + tag + '</span>'
        });

        return  '<div class="col s12 m4">'
            +       '<div class="card blue-grey darken-1">'
            +           '<div class="card-content white-text">'
            +               '<span class="card-title">'
            +                   challenge.title
            +                   '<span class="new badge red" data-badge-caption="points">' + challenge.points + '</span>'
            +               '</span>'
            +               '<p>' + challenge.description.substr(0,100) + '...' + '</p>'
            +               '<p>' + tags.join('') + '</p>'
            +           '</div>'
            +           '<div class="card-action">'
            +               '<a href="#">More</a>'
            +           '</div>'
            +       '</div>'
            +   '</div>';
    };

    var getChallenges = function() {
        var mountChallTpl = function(challenge) {
            var tpl = challengesDiv.append(challengeTpl(challenge));
        };

        var mountChallPromise = function(challUrl) {
            return $.getJSON('../challenges/' + challUrl + '.json')
                .then(mountChallTpl);
        };

        var challPromiseMap = function(challList) {
            return $.when.apply($, challList.map(mountChallPromise));
        };

        return $.getJSON('../challenges/index.json')
            .then(challPromiseMap);
    };


    var renderChallenges = function() {
        challengesDiv.html('');
        getChallenges();
    }

    _.nizkctf.init = function() {
        renderChallenges();
    }

    _.nizkctf.init();

})(window);
