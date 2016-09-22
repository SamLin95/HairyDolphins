var app = angular.module('HairyDolphinsApp');

app.controller('unauthNavController', ['$scope', '$uibModal', function ($scope, $uibModal) {
    var $ctrl = this;
    $ctrl.openSignupModal = openSignupModal;
    $ctrl.openLoginModal = openLoginModal;

    function openLoginModal() {
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/static/directives/login.html',
            controller: 'loginController',
            controllerAs: '$ctrl',
            size:'sm'
        });

        modalInstance.result.then( function(result) {
            if(result === 'signup')
            {
                $ctrl.openSignupModal();
            }
        });
    }

    function openSignupModal(){
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/static/directives/signup.html',
            controller: 'signupController',
            controllerAs: '$ctrl',
            size:'sm'
        });

        modalInstance.result.then( function(result) {
            if(result === 'login')
            {
                $ctrl.openLoginModal();
            }
        });
    }
}]);

app.controller('loginController', function($scope, $uibModalInstance, $http, $state) {
        var $ctrl = this;
        $ctrl.alerts = [];
        $ctrl.openSignupModal = openSignupModal;
        $ctrl.submitLoginRequest = submitLoginRequest;
        $ctrl.addAlert = addAlert;
        $ctrl.closeAlert = closeAlert;

        function openSignupModal() {
            $uibModalInstance.close('signup');
        }

        function submitLoginRequest() {
            if($scope.loginForm.$valid)
            {
                $state.go('auth.home');

                $uibModalInstance.close('success');
            }
        }

        function addAlert(type, message) {
            alertFactory.addAlert($ctrl, type, message);
        }

        function closeAlert(index) {
            alertFactory.closeAlert($ctrl, index);
        }
    }
);

app.controller('signupController', function($scope, $uibModalInstance, $http, $state, alertFactory) {
        var $ctrl = this;
        $ctrl.alerts = [];
        $ctrl.openLoginModal = openLoginModal;
        $ctrl.submitSignupRequest = submitSignupRequest;
        $ctrl.addAlert = addAlert;
        $ctrl.closeAlert = closeAlert;

        function openLoginModal() {
            $uibModalInstance.close('login');
        }

        function submitSignupRequest() {
            if($scope.signupForm.$valid)
            {
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
                    $state.go('auth.home');
                    $uibModalInstance.close('success');
                }, function errorCallback(response) { 
                    $ctrl.addAlert('danger', response.data.message)
                });
            }
        }

        function addAlert(type, message) {
            alertFactory.addAlert($ctrl, type, message);
        }

        function closeAlert(index) {
            alertFactory.closeAlert($ctrl, index);
        }
    }
);
