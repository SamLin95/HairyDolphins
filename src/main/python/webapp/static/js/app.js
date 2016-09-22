'use strict';

var app = angular.module('HairyDolphinsApp', ['ui.bootstrap']);

app.config(['showErrorsConfigProvider', function(showErrorsConfigProvider) {
  showErrorsConfigProvider.showSuccess(true);
}]);

app.directive('showErrors', function ($timeout, showErrorsConfig) {
      var getShowSuccess, linkFn;
      getShowSuccess = function (options) {
        var showSuccess;
        showSuccess = showErrorsConfig.showSuccess;
        if (options && options.showSuccess != null) {
          showSuccess = options.showSuccess;
        }
        return showSuccess;
      };
      linkFn = function (scope, el, attrs, formCtrl) {
        var blurred, inputEl, inputName, inputNgEl, options, showSuccess, toggleClasses;
        blurred = false;
        options = scope.$eval(attrs.showErrors);
        showSuccess = getShowSuccess(options);
        inputEl = el[0].querySelector('[name]');
        inputNgEl = angular.element(inputEl);
        inputName = inputNgEl.attr('name');
        if (!inputName) {
          throw 'show-errors element has no child input elements with a \'name\' attribute';
        }
        inputNgEl.bind('blur', function () {
          blurred = true;
          return toggleClasses(formCtrl[inputName].$invalid);
        });
        scope.$watch(function () {
          return formCtrl[inputName] && formCtrl[inputName].$invalid;
        }, function (invalid) {
          if (!blurred) {
            return;
          }
          return toggleClasses(invalid);
        });
        scope.$on('show-errors-check-validity', function () {
          return toggleClasses(formCtrl[inputName].$invalid);
        });
        scope.$on('show-errors-reset', function () {
          return $timeout(function () {
            el.removeClass('has-error');
            el.removeClass('has-success');
            return blurred = false;
          }, 0, false);
        });
        return toggleClasses = function (invalid) {
          el.toggleClass('has-error', invalid);
          if (showSuccess) {
            return el.toggleClass('has-success', !invalid);
          }
        };
      };
      return {
        restrict: 'A',
        require: '^form',
        compile: function (elem, attrs) {
          if (!elem.hasClass('form-group')) {
            throw 'show-errors element does not have the \'form-group\' class';
          }
          return linkFn;
        }
      };
    }
);
  
app.provider('showErrorsConfig', function () {
    var _showSuccess;
    _showSuccess = false;
    this.showSuccess = function (showSuccess) {
      return _showSuccess = showSuccess;
    };
    this.$get = function () {
      return { showSuccess: _showSuccess };
    };
});

app.directive('navbar', function() {
    return {
        restrict: 'A', //This menas that it will be used as an attribute and NOT as an element. I don't like creating custom HTML elements
        replace: true,
        templateUrl: "/static/directives/navbar.html",
        controller: "navbarController",
        controllerAs: "$navCtrl"
    }
});

app.directive("datepicker", function(){
  return {
    restrict: "A",
    controller: ['$scope', '$filter', function ($scope, $filter) {
        $scope.dateOptions = {
            formatYear: 'yy',
            maxDate: new Date(2020, 5, 22),
            minDate: new Date(),
            startingDay: 1
        };

        $scope.openDatePicker = function() {
            $scope.popup.opened = true;
        };

        $scope.popup = {
            opened: false
        };

        $scope.format = 'yyyy-MM-dd';
    }],
    templateUrl: "/static/directives/datepicker.html",
  }
});

app.controller('mainController', function($scope) {
});

app.controller('navbarController', ['$scope', '$uibModal', function ($scope, $uibModal) {
            var $ctrl = this;
            $ctrl.openLoginModal = function() {
                var modalInstance = $uibModal.open({
                    ariaLabelledBy: 'modal-title',
                    ariaDescribedBy: 'modal-body',
                    templateUrl: '/static/directives/login.html',
                    controller: 'loginController',
                    controllerAs: '$loginCtrl',
                    size:'sm'
                });

                modalInstance.result.then( function(result) {
                    if(result.localeCompare('login'))
                    {
                        $ctrl.openSignupModal();
                    }
                });
            }

            $ctrl.openSignupModal = function() {
                var modalInstance = $uibModal.open({
                    ariaLabelledBy: 'modal-title',
                    ariaDescribedBy: 'modal-body',
                    templateUrl: '/static/directives/signup.html',
                    controller: 'signupController',
                    controllerAs: '$signupCtrl',
                    size:'sm'
                });

                modalInstance.result.then( function(result) {
                    if(result.localeCompare('signup'))
                    {
                        $ctrl.openLoginModal();
                    }
                });
            }
        }]
)

app.controller('loginController', function($scope, $uibModalInstance, $http) {
        var $ctrl = this;
        $ctrl.alerts = [];

        $ctrl.openSignupModal = function() {
            $uibModalInstance.close('signup');
        }

        $ctrl.submitLoginRequest = function() {
            $scope.$broadcast('show-errors-check-validity');
    
            if ($scope.loginForm.$valid) {
            }
        }
    }
);

app.controller('signupController', function($scope, $uibModalInstance, $http) {
        var $ctrl = this;
        $ctrl.alerts = [];

        $ctrl.openLoginModal = function() {
            $uibModalInstance.close('login');
        }

        $ctrl.submitSignupRequest = function() {
            $scope.$broadcast('show-errors-check-validity');
    
            if ($scope.signupForm.$valid) {
                if(!($ctrl.password === $ctrl.confirmPassword))
                {
                    $ctrl.addAlert('danger', "password and confirm password should be the same");
                }

                $http({
                    method: 'POST',
                    url: 'api/users',
                    params: {
                        username: $ctrl.username,
                        password: $ctrl.password,
                        first_name: $ctrl.firstName,
                        last_name: $ctrl.lastName,
                        email: $ctrl.email
                    }
                }).then(function successCallback(response) {
                    console.log(response);
                }, function errorCallback(response) { 
                    $ctrl.addAlert('danger', response.data.message)
                });
            }
        }

        $ctrl.addAlert = function(type, message) {
            if(typeof message === 'string'){
                $ctrl.alerts.push({ type: type, msg: message });
            }
            else{
                Object.keys(message).forEach(function (key) {
                    $ctrl.alerts.push({ type: type, msg: key + " : " + message[key]});
                });
            }
        }

        $ctrl.closeAlert = function(index) {
            $ctrl.alerts.splice(index, 1);
        }
    }
);
