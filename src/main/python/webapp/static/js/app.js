'use strict';

var app = angular.module('HairyDolphinsApp', ['ui.bootstrap', 'ui.router', 'bootstrap.angular.validation']);

app.config(['bsValidationConfigProvider', function(bsValidationConfigProvider) {
  bsValidationConfigProvider.global.setValidateFieldsOn('submit');
  // We can also customize to enable the multiple events to display form validation state
  //bsValidationConfigProvider.global.setValidateFieldsOn(['submit', 'blur]);
  
  bsValidationConfigProvider.global.errorMessagePrefix = '<span class="glyphicon glyphicon-warning-sign"></span> &nbsp;';
}])

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
