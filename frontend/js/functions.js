(function(_) {
    _.nizkctf = {};

    var challengesDiv = $('#challenges');
    var modalsDiv = $('#modals');

    var challTagsTpl = function(tags) {
        return tags.map(function(tag){
            return '<span class="new badge" data-badge-caption="">' + tag + '</span>';
        }).join('');
    };

    var challModalTpl = function(challenge) {
        return  '<div id="' + challenge.id + '" class="modal">'
            +       '<div class="modal-content">'
            +           '<h4>' + challenge.title + '</h4>'
            +           '<p>' + challenge.description + '</p>'
            +           '<p><b>Points</b>: ' + challenge.points + '</></p>'
            +           '<p><b>Tags</b>: ' + challenge.tags.join(', ') + '</></p>'
            +       '</div>'
            +       '<div class="modal-footer">'
            +           '<a href="#!" class=" modal-action modal-close waves-effect waves-green btn-flat">Close</a>'
            +       '</div>'
            +   '</div>';
    }

    var challCardTpl = function(challenge) {

        return  '<div class="col s12 m4">'
            +       '<div class="card blue-grey darken-1">'
            +           '<div class="card-content white-text">'
            +               '<span class="card-title">'
            +                   challenge.title
            +                   '<span class="new badge red" data-badge-caption="points">' + challenge.points + '</span>'
            +               '</span>'
            +               '<p>' + challenge.description.substr(0,100) + '...' + '</p>'
            +               '<p>' + challTagsTpl(challenge.tags) + '</p>'
            +           '</div>'
            +           '<div class="card-action">'
            +               '<a class="waves-effect waves-light btn" href="#' + challenge.id + '">More</a>'
            +           '</div>'
            +       '</div>'
            +   '</div>';
    };

    var getChallenges = function() {
        var mountChallTpl = function(challenge) {
            challengesDiv.append(challCardTpl(challenge));
            modalsDiv.append(challModalTpl(challenge));
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

    var getSettings = function() {
        var handleSettings = function(settings) {
            $('#logo-container').text(settings.ctf_name);
        };

        $.getJSON('../settings.json')
            .then(handleSettings);
    };

    var renderChallenges = function() {
        challengesDiv.html('');
        getChallenges()
            .then(function() {
                $('.modal').modal();
            });
    }

    _.nizkctf.init = function() {
        renderChallenges();
        getSettings();
    }

    _.nizkctf.init();

})(window);
