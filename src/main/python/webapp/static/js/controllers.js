var app = angular.module('HairyDolphinsApp');

app.controller('mainController', function($scope, $state) {
    $scope.sendSearchRequest = sendSearchRequest;

    function sendSearchRequest() {
        available_date = $scope.dt? moment($scope.dt).format("YYYY-MM-DD"):undefined

        $state.go(
            '^.laSearch',
            {
                keyword: $scope.searchString,
                available_date: available_date,
                request_fields: [
                    'first_name',
                    'local_advisor_profile',
                    'last_name',
                    'average_rating',
                    'profile_photo_url'
                ]
            }
        )
    }
})

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

app.controller('signupController', function($scope, $uibModalInstance, $rootScope, $http, $state, utils, alertFactory) {
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
                utils.requestStart()
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
                    utils.requestEnd()
                }, function errorCallback(response) { 
                    $ctrl.addAlert('danger', response.data.message)
                    utils.requestEnd()
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

app.controller('laSearchController', function($scope, localAdvisors, $state, $stateParams, searchHelper, utils){
  utils.replaceInvalidImages(localAdvisors, 'profile_photo_url')
  $scope.localAdvisors = localAdvisors
  $scope.sendSearchRequest = sendSearchRequest;
  $scope.displayCollection = [].concat($scope.localAdvisors);

  $scope.alert = function() {
    alert('clicked')
  }

  function sendSearchRequest() {
        available_date = $scope.dt? moment($scope.dt).format("YYYY-MM-DD"):undefined
        keyword = $scope.searchString? $scope.searchString:undefined

        searchHelper.searchLocalAdvisors({
                keyword: keyword,
                available_date: available_date,
                request_fields: [
                    'first_name',
                    'local_advisor_profile',
                    'last_name',
                    'average_rating',
                    'profile_photo_url'
                ]
        }).then(function(data){
            utils.replaceInvalidImages(data, 'profile_photo_url')
            $scope.localAdvisors = data
            $scope.displayCollection = [].concat($scope.localAdvisors);
            $scope.isLoading = false
            utils.requestEnd();
        })
    }
});

app.controller('messengerController', function($scope, userContacts, utils) {
    $scope.userContacts = utils.fillFallbackList(userContacts, 10)
    $scope.displayContacts = [].concat($scope.userContacts)
})


app.controller('messengerChatPanelController', function($scope, $stateParams, utils, messageHistory, AuthService, socketService) {
    //Self
    self_user = AuthService.getUser()
    $scope.self_id = self_user.id
    $scope.self_name = self_user.first_name + ' ' + self_user.last_name
    $scope.self_profile_photo_url = self_user.profile_photo_url
    utils.replaceInvalidImages($scope, 'self_profile_photo_url')

    //The other chatter
    $scope.contact_id = $stateParams.user_id
    $scope.contact_name = $stateParams.first_name + ' ' +  $stateParams.last_name
    $scope.contact_profile_photo_url = $stateParams.profile_photo_url
    utils.replaceInvalidImages($scope, 'contact_profile_photo_url')

    $scope.messageHistory = messageHistory

    $scope.send_message = send_message

    function send_message(){
        socketService.emit('message', $scope.message_to_send)
    }
})