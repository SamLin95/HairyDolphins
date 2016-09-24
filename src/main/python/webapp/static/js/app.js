'use strict';

var app = angular.module('HairyDolphinsApp', ['ui.bootstrap', 'ngAnimate', 'ui.router',
  'bootstrap.angular.validation', 'smart-table', 'angularSpinner']);

app.config(['usSpinnerConfigProvider', function (usSpinnerConfigProvider) {
    usSpinnerConfigProvider.setDefaults({radius:6, length: 1});
}]);

app.config(['bsValidationConfigProvider', function(bsValidationConfigProvider) {
  bsValidationConfigProvider.global.setValidateFieldsOn('submit');
  // We can also customize to enable the multiple events to display form validation state
  //bsValidationConfigProvider.global.setValidateFieldsOn(['submit', 'blur]);
  
  bsValidationConfigProvider.global.errorMessagePrefix = '<span class="glyphicon glyphicon-warning-sign"></span> &nbsp;';
}])

app.config(function($stateProvider, $urlRouterProvider) {
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
      },
      auth_redirect: "auth"
    })
    .state('unauth.home', { 
      url: '/home', 
      views: { 
        'content@' : {
          templateUrl: '/static/partials/common/home.html',
          controller: 'mainController',
          controllerAs: 'main'
        }
      },
      auth_redirect: "auth.home",
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('unauth.laSearch', { 
      url: '/laSearch?keyword&available_date&request_fields', 
      views: { 
        'content@' : {
          templateUrl: '/static/partials/common/laSearch.html',
          controller: 'laSearchController',
          controllerAs: 'laSearch'
        }
      },
      auth_redirect: "auth.laSearch",
      resolve: {
        localAdvisors: function($stateParams, searchHelper){
          return searchHelper.searchLocalAdvisors($stateParams)
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('auth', {
      abstract: true,
      url: '/auth',
      views: { 
        'header' : { 
          templateUrl: '/static/partials/auth/auth_nav.html',
          controller: 'authNavController',
          controllerAs: 'nav'
        }
      },
      unauth_redirect: "unauth"
    })
    .state('auth.home', {
      url: '/home', 
      views: { 
        'content@' : {
          templateUrl: '/static/partials/common/home.html',
          controller: 'mainController',
          controllerAs: 'main'
        }
      },
      unauth_redirect: "unauth.home",
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('auth.laSearch', { 
      url: '/laSearch?keyword&available_date&request_fields', 
      views: { 
        'content@' : {
          templateUrl: '/static/partials/common/laSearch.html',
          controller: 'laSearchController',
          controllerAs: 'laSearch'
        }
      },
      unauth_redirect: "unauth.laSearch",
      resolve: {
        localAdvisors: function($stateParams, searchHelper){
          return searchHelper.searchLocalAdvisors($stateParams)
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })

    $urlRouterProvider.otherwise('/unauth/home');
  
});

app.run(function($rootScope){
  $rootScope.isLoading = false;
  $rootScope.s3url = "https://s3.amazonaws.com/hairydolphins/"
})

app.run(function ($rootScope, $state, AuthService) {
  $rootScope.$on("$stateChangeStart", function(event, toState, toParams, fromState, fromParams){
    toState.name
    AuthService.loadCurrentUser()
      .then(function(){
        if(toState.auth_redirect){
          $state.transitionTo(toState.auth_redirect);
          event.preventDefault();
        }
      })
      .catch(function(){
        if(toState.unauth_redirect){
          $state.transitionTo(toState.unauth_redirect);
          event.preventDefault(); 
        }
      })
  });
});

