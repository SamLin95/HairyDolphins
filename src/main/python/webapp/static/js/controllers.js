var app = angular.module('HairyDolphinsApp');

app.controller('unauthNavController', ['$scope', '$uibModal', function ($scope, $uibModal) {
    var $ctrl = this;
    $ctrl.openSignupModal = openSignupModal;
    $ctrl.openLoginModal = openLoginModal;
    $scope.isCollapsed = true;

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

app.controller('authNavController', function ($scope, $state, AuthService) {
    var $ctrl = this;
    $ctrl.logout = logout;
    $scope.user = AuthService.getUser();
    $scope.isCollapsed = true;
  
    function logout(){
        AuthService.logout()
            .then(function() {
                    alert("You have been logged out")
                    $state.go('unauth.home');
                }
            )
    }
});


app.controller('loginController', function($scope, $uibModalInstance, $http, $state, alertFactory, AuthService) {
        var $ctrl = this;
        $ctrl.alerts = [];
        $ctrl.openSignupModal = openSignupModal;
        $ctrl.submitLoginRequest = submitLoginRequest;
        $ctrl.addAlert = addAlert;
        $ctrl.closeAlert = closeAlert;
        $ctrl.clearData = clearData;

        function openSignupModal() {
            $uibModalInstance.close('signup');
        }

        function submitLoginRequest() {
            if($scope.loginForm.$valid)
            {
                AuthService.login($ctrl.username, $ctrl.password)
                    .then(function () {
                        $ctrl.clearData();
                        $state.go('auth.home');
                        $uibModalInstance.close('success');
                    }).catch(function () {
                        $ctrl.clearData();
                        $ctrl.addAlert('danger', "Invalid username and/or password")
                    })
            }
        }

        function addAlert(type, message) {
            alertFactory.addAlert($ctrl, type, message);
        }

        function closeAlert(index) {
            alertFactory.closeAlert($ctrl, index);
        }

        function clearData() {
            $ctrl.username = undefined;
            $ctrl.password = undefined;
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
                    $ctrl.alerts = []
                    alert("Your account has been successfully created!")
                    $uibModalInstance.close('login');
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
