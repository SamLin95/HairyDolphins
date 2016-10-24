'use strict';

var app = angular.module('HairyDolphinsApp', ['ui.bootstrap', 'ngAnimate', 'ui.router',
  'bootstrap.angular.validation', 'smart-table', 'angularSpinner', 'btford.socket-io', 'lr.upload',
  'uiGmapgoogle-maps']);

app.config(['usSpinnerConfigProvider', function (usSpinnerConfigProvider) {
    usSpinnerConfigProvider.setDefaults({radius:6, length: 1});
}]);

app.config(function(uiGmapGoogleMapApiProvider) {
    uiGmapGoogleMapApiProvider.configure({
        //    key: 'your api key',
        v: '3.20', //defaults to latest 3.X anyhow
        libraries: 'weather,geometry,visualization',
        key: 'AIzaSyCe4fuOg-Njod6WBo8P6UPeWhOaOdErsgE'
    });
})

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
      auth_redirect: "auth",
      onEnter: function(utils) {
        utils.requestEnd()
      }
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
      resolve: {
        localAdvisors: function(searchHelper){
          return searchHelper.searchLocalAdvisors({"limit":3, "request_fields":["id","first_name", "last_name", "profile_photo_url", "local_advisor_profile"]})
        },
        recommendations: function(searchHelper){
          return searchHelper.searchRecommendations({"limit":3, "request_fields":["id","title", "description", "primary_picture"]})
        }
      },
      auth_redirect: "auth.home",
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('unauth.laSearch', {
      url: '/laSearch?keyword&available_date&limit',
      views: {
        'content@' : {
          templateUrl: '/static/partials/common/laSearch.html',
          params: {
            keyword: null,
            available_date: null
          },
          controller: 'laSearchController',
          controllerAs: 'laSearch'
        }
      },
      auth_redirect: "auth.laSearch",
      resolve: {
        localAdvisors: function($stateParams, searchHelper){
          $stateParams.request_fields = [
            'first_name',
            'local_advisor_profile',
            'last_name',
            'id',
            'average_rating',
            'profile_photo_url'
          ]

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
      unauth_redirect: "unauth",
      onEnter: function(utils) {
        utils.requestEnd()
      }
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
      resolve: {
        localAdvisors: function(searchHelper){
          return searchHelper.searchLocalAdvisors({"limit":3, "request_fields":["id","first_name", "last_name", "profile_photo_url", "local_advisor_profile"]})
        },
        recommendations: function(searchHelper){
          return searchHelper.searchRecommendations({"limit":3, "request_fields":["id", "title", "description", "primary_picture"]})
        }
      },
      unauth_redirect: "unauth.home",
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('auth.laSearch', {
      url: '/laSearch?keyword&available_date&limit',
      views: {
        'content@' : {
          templateUrl: '/static/partials/common/laSearch.html',
          params: {
            keyword: null,
            available_date: null
          },
          controller: 'laSearchController',
          controllerAs: 'laSearch'
        }
      },
      unauth_redirect: "unauth.laSearch",
      resolve: {
        localAdvisors: function($stateParams, searchHelper){
          $stateParams.request_fields = [
            'first_name',
            'local_advisor_profile',
            'last_name',
            'id',
            'average_rating',
            'profile_photo_url'
          ]
          return searchHelper.searchLocalAdvisors($stateParams)
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('auth.messenger', {
      url: '/messenger',
      views: {
        'content@' : {
            templateUrl: '/static/partials/auth/messenger.html',
            controller: "messengerController",
            controllerAs: "mes"
        }
      },
      resolve: {
        userContacts: function(searchHelper) {
          return searchHelper.searchUserContacts()
        }
      },
      unauth_redirect: "unauth.home",
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('auth.messenger.chatpanel', {
      url: '/messenger/chatpanel?user_id&first_name&last_name&profile_photo_url',
      views: {
        'chatpanel@auth.messenger' : {
            templateUrl: '/static/partials/auth/messenger.chatpanel.html',
            controller: "messengerChatPanelController",
            controllerAs: "mescp"
        }
      },
      unauth_redirect: "unauth.home",
      resolve: {
        messageHistory: function(searchHelper, $stateParams) {
          return searchHelper.searchMessageHistory($stateParams.user_id)
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('auth.locRec', {
      url: '/locRec?city_id&recommendation_category_id&limit',
      views: {
        'content@' : {
          templateUrl: '/static/partials/common/locRec.html',
          controller: 'locRecController',
          controllerAs: 'locRec'
        }
      },
      unauth_redirect: "unauth.locRec",
      resolve: {
        recommendations: function($stateParams, searchHelper){
          $stateParams.request_fields = [
                'recommendation_category',
                'recommendation_photos',
                'entity_recommendations',
                'title',
                'average_rating',
                'description',
                'city',
                'id',
                'reviews',
                'primary_picture',
                'address_line_one',
                'address_line_two',
                'zip_code'
          ]
          return searchHelper.searchRecommendations($stateParams)
        },
        cities: function(searchHelper){
          return searchHelper.getCityOptions()
        },
        recommendation_categories: function(searchHelper) {
          return searchHelper.getRecommendationCategoryOptions()
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('unauth.locRec', {
      url: '/locRec?city_id&recommendation_category_id&limit',
      views: {
        'content@' : {
          templateUrl: '/static/partials/common/locRec.html',
          controller: 'locRecController',
          controllerAs: 'locRec'
        }
      },
      auth_redirect: "auth.locRec",
      resolve: {
        recommendations: function($stateParams, searchHelper){
          $stateParams.request_fields = [
                'recommendation_category',
                'recommendation_photos',
                'entity_recommendations',
                'title',
                'average_rating',
                'description',
                'city',
                'id',
                'reviews',
                'primary_picture',
                'address_line_one',
                'address_line_two',
                'zip_code'
          ]
          return searchHelper.searchRecommendations($stateParams)
        },
        cities: function(searchHelper){
          return searchHelper.getCityOptions()
        },
        recommendation_categories: function(searchHelper) {
          return searchHelper.getRecommendationCategoryOptions()
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('auth.recCreation', {
      url: '/recommendation_creation',
      views: {
        'content@' : {
          templateUrl: '/static/partials/auth/recommendation_creation.html',
          controller: 'recCreationController',
          controllerAs: 'recCre'
        }
      },
      resolve: {
        cities: function(searchHelper){
          return searchHelper.getCityOptions()
        },
        recommendation_categories: function(searchHelper) {
          return searchHelper.getRecommendationCategoryOptions()
        }
      },
      unauth_redirect: "unauth.home",
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('auth.advisorDetail', {
      url: '/advisorDetail?id',
      views: {
        'content@' : {
          templateUrl: '/static/partials/detail/advisorDetail.html',
          params: {
            id: null
          },
          controller: 'advisorDetailController',
          controllerAs: 'advisorDetail'
        }
      },
      unauth_redirect: "unauth.advisorDetail",
      resolve: {
        advisor: function($stateParams, searchHelper){
          return searchHelper.getAdvisorDetail($stateParams)
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('unauth.advisorDetail', {
      url: '/advisorDetail?id',
      views: {
        'content@' : {
          templateUrl: '/static/partials/detail/advisorDetail.html',
          params: {
            id: null
          },
          controller: 'advisorDetailController',
          controllerAs: 'advisorDetail'
        }
      },
      auth_redirect: "auth.advisorDetail",
      resolve: {
        advisor: function($stateParams, searchHelper){
          return searchHelper.getAdvisorDetail($stateParams)
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('auth.recDetail', {
      url: '/recDetail?id',
      views: {
        'content@' : {
          templateUrl: '/static/partials/detail/recDetail.html',
          params: {
            id: null
          },
          controller: 'recDetailController',
          controllerAs: 'recDetail'
        }
      },
      unauth_redirect: "unauth.recDetail",
      resolve: {
        recommendation: function($stateParams, searchHelper){
          return searchHelper.getRecDetail($stateParams)
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })
    .state('unauth.recDetail', {
      url: '/recDetail?id',
      views: {
        'content@' : {
          templateUrl: '/static/partials/detail/recDetail.html',
          params: {
            id: null
          },
          controller: 'recDetailController',
          controllerAs: 'recDetail'
        }
      },
      auth_redirect: "auth.recDetail",
      resolve: {
        recommendation: function($stateParams, searchHelper){
          return searchHelper.getRecDetail($stateParams)
        }
      },
      onEnter: function(utils) {
        utils.requestEnd()
      }
    })

    $urlRouterProvider.otherwise('/unauth/home');
  
});

app.run(function($rootScope, $location, $anchorScroll){
  $rootScope.isLoading = false;

  $rootScope.gotoTop = function() {
      // set the location.hash to the id of
      // the element you wish to scroll to.
      $location.hash('pageBody');

      // call $anchorScroll()
      $anchorScroll();
  };

  $rootScope.s3url = "https://s3.amazonaws.com/hairydolphins/"
})

app.run(function ($rootScope, $state, AuthService, utils) {
  $rootScope.$on("$stateChangeStart", function(event, toState, toParams, fromState, fromParams){
    utils.requestStart()
    AuthService.loadCurrentUser()
      .then(function(){
        if(toState.auth_redirect){
          $state.transitionTo(toState.auth_redirect, toParams);
          event.preventDefault();
        }
      })
      .catch(function(){
        if(toState.unauth_redirect){
          $state.transitionTo(toState.unauth_redirect, toParams);
          event.preventDefault(); 
        }
      })
  });
});

