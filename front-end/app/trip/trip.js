'use strict';

angular.module('HairyDolphinsApp.trip', ['ngRoute'])

// Declared route
.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/trip', {
        templateUrl: 'trip/trip.html',
        controller: 'tripCtrl'
    });
}])

// Home controller
.controller('tripCtrl', [function() {

}]);
