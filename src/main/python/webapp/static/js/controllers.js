var app = angular.module('HairyDolphinsApp');

app.controller('mainController', function($scope, $state) {
    $scope.sendSearchRequest = sendSearchRequest;
    $scope.flag = true;
    function sendSearchRequest() {
        $scope.flag = false;
        keyword = $scope.searchString
        available_date = $scope.dt? moment($scope.dt).format("YYYY-MM-DD"):undefined

        $state.go(
            '^.laSearch',
            {
                keyword: keyword,
                available_date: available_date,
                request_fields: [
                    'first_name',
                    'local_advisor_profile',
                    'last_name',
                    'id',
                    'average_rating',
                    'profile_photo_url'
                ],
                flag: false
            }
        )

    }
})

app.controller('unauthNavController', function ($scope, AuthService ) {
    var $ctrl = this;
    $ctrl.openSignupModal = AuthService.openSignupModal;
    $ctrl.openLoginModal = AuthService.openLoginModal;
    $scope.isCollapsed = true;

});

app.controller('authNavController', function ($scope, $state, AuthService) {
    var $ctrl = this;
    $ctrl.logout = logout;
    $scope.user = AuthService.getUser();
    $scope.isCollapsed = true;
  
    function logout(){
        AuthService.logout()
            .then(function() {
                    alert("You have been logged out")
                    $state.reload();
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
                        $state.reload();
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

  $scope.alert = function(param) {
      id = param.id;

      $state.go(
          '^.advisorDetail',
          {
              id: id,
              request_fields: []
          })
  }

  function sendSearchRequest() {
        available_date = $scope.dt? moment($scope.dt).format("YYYY-MM-DD"):undefined
        keyword = $scope.searchString? $scope.searchString:undefined
,
        searchHelper.searchLocalAdvisors({
                keyword: keyword,
                available_date: available_date,
                request_fields: [
                    'first_name',
                    'local_advisor_profile',
                    'id',
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

app.controller('advisorDetailController', function($scope, advisor, $state, $stateParams, utils, alertFactory, AuthService, reviewManager, $uibModal) {
    $scope.alerts = [];
    $scope.addAlert = addAlert;
    $scope.closeAlert = closeAlert;
    $scope.user = AuthService.getUser();
    $scope.openLoginModal = AuthService.openLoginModal;
    $scope.openSignupModal = AuthService.openSignupModal;
    $scope.checkAvailability = checkAvailability;
    $scope.available_dates = advisor.local_advisor_profile.available_dates.map(function(available_date){
        return available_date.date
    })

    utils.replaceInvalidImages(advisor, 'profile_photo_url')
    $scope.advisor = advisor
    $scope.review_count = advisor.local_advisor_profile.reviews.length
    $scope.displayCollection = [].concat($scope.advisor.local_advisor_profile.reviews)
    $scope.submitPostReviewRequest = submitPostReviewRequest
    $scope.newReview = null

    function addAlert(type, message) {
        alertFactory.addAlert($scope, type, message);
    }

    function closeAlert(index) {
        alertFactory.closeAlert($scope, index);
    }

    function submitPostReviewRequest() {
        if(!$scope.newReview || !$scope.newReview.rating) {
            addAlert('danger', "A rating needs to be submitted")
        }

        if($scope.reviewForm.$valid) {
            reviewManager.createNewReview({
                title : $scope.newReview.title,
                content : $scope.newReview.content,
                rating : $scope.newReview.rating,
                reviewer_id : $scope.user.id,
                local_advisor_profile_id : $scope.advisor.local_advisor_profile.id
            }).then(function(review){
                utils.requestEnd();
                $scope.addAlert('success', "Your review has been successfully submitted")
                $scope.advisor.local_advisor_profile.reviews.push(review)
                $scope.advisor.average_rating = ($scope.advisor.average_rating * $scope.review_count + $scope.newReview.rating)/($scope.review_count + 1)
                $scope.newReview = null

                //refresh review_count
                $scope.review_count += 1
                $scope.displayCollection = [].concat($scope.advisor.local_advisor_profile.reviews)
            }).catch(function (response) {
                addAlert('danger', response.data.message)
            })
        }
    }

    function checkAvailability() {
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/static/partials/detail/availabilityModal.html',
            windowClass: 'dateModal',
            scope: $scope,
            size:'sm',
            controller: function ($scope, $filter) {
                $scope.dateOptions = {
                    formatYear: 'yy',
                    maxDate: new Date(2020, 5, 22),
                    minDate: new Date(),
                    startingDay: 1,
                    dateDisabled: function(date, mode) {
                        if(date.mode == 'day'){
                            date_to_check = moment(date.date).format("YYYY-MM-DD")
                            
                            if($scope.available_dates.indexOf(date_to_check) == -1) {
                                return true
                            }
                            return false
                        }
                    },
                    customClass: function(date) {
                         if(date.mode == 'day'){
                            date_to_check = moment(date.date).format("YYYY-MM-DD")
                            
                            if($scope.available_dates.indexOf(date_to_check) == -1) {
                                return ''
                            }

                            return 'btn-date-available'
                        }
                    }
                };
            }
        })
    }
});

app.controller('locRecController', function($scope, recommendations, cities, recommendation_categories, $state, $stateParams, searchHelper, utils){
    $scope.cities = cities
    $scope.recommendation_categories = recommendation_categories
    utils.replaceInvalidImages(recommendations, 'primary_picture')
    $scope.recommendations = recommendations
    $scope.sendSearchRequest = sendSearchRequest;
    $scope.displayCollection = [].concat($scope.recommendations);

    $scope.alert = function(param) {
        id = param.id;
        $state.go(
            '^.recDetail',
            {
                id: id,
                request_fields: []
            })
    }

    function sendSearchRequest() {
        city_id = $scope.selected_city ? $scope.selected_city.id:undefined
        recommendation_category_id = $scope.selected_recommendation_category ? $scope.selected_recommendation_category.id:undefined

        searchHelper.searchRecommendations({
            city_id: city_id,
            recommendation_category_id: recommendation_category_id,
            request_fields: [
                'recommendation_category',
                'recommendation_photos',
                'recommender',
                'reviews',
                'title',
                'average_rating',
                'description',
                'city',
                'id',
                'primary_picture',
                'address_line_one',
                'address_line_two',
                'zip_code'
            ]
        }).then(function(data){
            utils.replaceInvalidImages(data, 'primary_picture')
            $scope.recommendations = data
            $scope.displayCollection = [].concat($scope.recommendations);
            $scope.isLoading = false
            utils.requestEnd();
        })

    }

});

app.controller('recDetailController', function($scope, recommendation, $state, $stateParams, utils, alertFactory, AuthService, reviewManager) {
    $scope.alerts = [];
    $scope.addAlert = addAlert;
    $scope.closeAlert = closeAlert;
    $scope.user = AuthService.getUser();

    $scope.openLoginModal = AuthService.openLoginModal;
    $scope.openSignupModal = AuthService.openSignupModal;
    utils.replaceInvalidImages(recommendation, 'primary_picture')
    $scope.recommendation = recommendation
    $scope.review_count = recommendation.reviews.length
    $scope.displayCollection = [].concat($scope.recommendation.reviews)
    $scope.submitPostReviewRequest = submitPostReviewRequest
    $scope.newReview = null

    $scope.map = { center: { latitude: recommendation.geo.lat, longitude: recommendation.geo.lng }, zoom: 8 };

    function addAlert(type, message) {
        alertFactory.addAlert($scope, type, message);
    }

    function closeAlert(index) {
        alertFactory.closeAlert($scope, index);
    }

    function submitPostReviewRequest() {
        if(!$scope.newReview || !$scope.newReview.rating) {
            addAlert('danger', "A rating needs to be submitted")
        }

        if($scope.reviewForm.$valid) {
            reviewManager.createNewReview({
                title : $scope.newReview.title,
                content : $scope.newReview.content,
                rating : $scope.newReview.rating,
                reviewer_id : $scope.user.id,
                recommendation_id : $scope.recommendation.id
            }).then(function(review){
                utils.requestEnd();
                $scope.addAlert('success', "Your review has been successfully submitted")
                $scope.recommendation.reviews.push(review)
                $scope.recommendation.average_rating = ($scope.recommendation.average_rating * $scope.review_count + $scope.newReview.rating)/($scope.review_count + 1)
                $scope.newReview = null

                //refresh review_count
                $scope.review_count += 1
                $scope.displayCollection = [].concat($scope.recommendation.reviews)
            }).catch(function (response) {
                addAlert('danger', response.data.message)
            })
        }
    }

});


app.controller('messengerController', function($scope, searchHelper, userContacts, utils, AuthService) {
    self_user = AuthService.getUser()
    $scope.userContacts = utils.fillFallbackList(userContacts, 10)
    $scope.displayContacts = [].concat($scope.userContacts)
    $scope.searchUsers = searchUsers
    $scope.onContactSelect = onContactSelect

    function searchUsers(keyword) {
        return searchHelper.searchUsers({
            keyword : keyword,
            limit : 8,
            request_fields : [
                'id',
                'first_name',
                'last_name',
                'username',
                'profile_photo_url',
                'email'
            ]
        }).then(function(data) {
            return data
        })
    }

    function onContactSelect(item, model, label) {
        contact_id_list = userContacts.map(function(contact){
            return contact.id
        })

        if(contact_id_list.indexOf(model.id) == -1 && model.id != self_user.id) 
        {
            userContacts.unshift(model)
            $scope.userContacts = utils.fillFallbackList(userContacts, 10)
            $scope.displayContacts = [].concat($scope.userContacts)
        }
    }
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

app.controller('recCreationController', function($scope, cities, recommendation_categories, utils, fileManager, AuthService, recManager, alertFactory) {
    $scope.alerts = [];
    $scope.addAlert = addAlert;
    $scope.closeAlert = closeAlert;
    $scope.user = AuthService.getUser();

    $scope.cities = cities
    $scope.recommendation_categories = recommendation_categories
    $scope.submitRecCreationRequest = submitRecCreationRequest
    $scope.displayed_recommendation_photo = "/static/images/placeholder.png"
    
    $scope.doUpload = function() {
        fileManager.uploadFile(event.target.files[0]).then(function(data){
            $scope.displayed_recommendation_photo = data.download_link
            $scope.current_photo = data
            utils.requestEnd();
        })
    }

    function addAlert(type, message) {
        alertFactory.addAlert($scope, type, message);
    }

    function closeAlert(index) {
        alertFactory.closeAlert($scope, index);
    }

    function submitRecCreationRequest() {
        if($scope.recCrtForm.$valid)
        {
            recManager.createNewRec({
                title : $scope.title,
                description : $scope.description,
                address_line_one : $scope.address_line_one,
                address_line_two : $scope.address_line_two,
                zip_code : $scope.zip_code,
                city_id : $scope.selected_city.id,
                recommendation_category_id : $scope.selected_recommendation_category.id,
                recommender_id : $scope.user.id,
                file_id : $scope.current_photo.id 
            }).then(function(data){
                utils.requestEnd();
                $scope.addAlert('success', "Your recommendation has been successfully created!")
            }).catch(function (data) {
                utils.requestEnd();
                addAlert('danger', "Failed to create the new recommendation")
            })
        }
    }


})
