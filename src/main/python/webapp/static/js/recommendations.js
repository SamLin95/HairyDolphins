'use strict';

angular.module('HairyDolphinsApp.reccomendations', ['ngRoute'])

// Declared route
.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/recommendations', {
        templateUrl: 'templates/reccomendations.html',
        controller: 'reccomendationsCtrl'
    });
}])

// Home controller
.controller('recommendationsCtrl', [function() {

}]);
