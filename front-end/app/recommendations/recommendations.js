'use strict';

angular.module('HairyDolphinsApp.reccomendations', ['ngRoute'])

// Declared route
.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/recommendations', {
        templateUrl: 'reccomendations/reccomendations.html',
        controller: 'reccomendationsCtrl'
    });
}])

// Home controller
.controller('recommendationsCtrl', [function() {

}]);
