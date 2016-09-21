'use strict';

angular.module('HairyDolphinsApp.laSearch', ['ngRoute'])

// Declared route
.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/laSearch', {
        templateUrl: 'templates/laSearch.html',
        controller: 'laSearchCtrl'
    });
}])

// Home controller
.controller('laSearchCtrl', [function() {

}]);
