'use strict';

var app = angular.module('HairyDolphinsApp', ['ui.bootstrap', 'ui.router', 'bootstrap.angular.validation']);

app.controller('mainController', function($scope) {
});

app.config(function($stateProvider, $urlRouterProvider) {
  // An array of state definitions
  $stateProvider
    .state('unauth', {
      abstract: true,
      url: '/unauth',
      views: { 
        'header' : { 
          templateUrl: '/static/partials/unauth/unauth_nav.html',
          controller: 'unauthNavController',
          controllerAs: 'nav'
        }
      }
    })
    .state('unauth.home', { 
      url: '/home', 
      views: { 
        'content@' : {
          templateUrl: '/static/partials/common/home.html'
        }
      }    
    })
    .state('auth', {
      abstract: true,
      url: '/auth',
      views: { 
        'header' : { 
          templateUrl: '/static/partials/auth/auth_nav.html',
          controller: 'unauthNavController',
          controllerAs: 'nav'
        }
      }
    })
    .state('auth.home', { 
      url: '/home', 
      views: { 
        'content@' : {
          templateUrl: '/static/partials/common/home.html'
        }
      }    
    })

    $urlRouterProvider.otherwise('/unauth/home');
  
});
