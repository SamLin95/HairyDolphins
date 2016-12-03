var app = angular.module('HairyDolphinsApp');

//Contoller for the main page
app.controller('mainController', function($scope, $state, localAdvisors, recommendations, cities) {
    $scope.sendSearchRequest = sendSearchRequest;
    $scope.localAdvisors = localAdvisors;
    $scope.cities = cities;
    $scope.recommendations = recommendations;
    //place holder text for the date picker
    $scope.datepicker_placeholder = "Expected Date"
    $scope.dateOptions = {
        formatYear: 'yy',
        maxDate: new Date(2020, 5, 22),
        minDate: new Date(),
        startingDay: 1
    };

    //function to send local advisor search request
    function sendSearchRequest() {
        //All three criteria are optional. Except for keyword, the other two need to be processed before sent.
        keyword = $scope.searchString
        available_date = $scope.dt ? moment($scope.dt).format("YYYY-MM-DD") : undefined
        city_id = $scope.selected_city ? $scope.selected_city.id : undefined

        $state.go(
            '^.laSearch', {
                city_id: city_id,
                keyword: keyword,
                available_date: available_date
            }
        )

    }

    //function to redirect user to a local adviosr's detail page
    $scope.viewAdvisorDetails = function(param) {
        id = param.id;

        $state.go(
            '^.advisorDetail', {
                id: id
            })
    }

    //function to redirect user to a recommendation's detail page
    $scope.viewRecommendationDetails = function(param) {
        id = param.id;

        $state.go(
            '^.recDetail', {
                id: id
            })
    }

    //function to direct user to recommendation search pages
    $scope.searchMoreRecommendations = function() {
        $state.go(
            '^.locRec', {
                limit: 5
            })

    }

    //function to direct user to local advisor search pages
    $scope.searchMoreAdvisors = function() {
        $state.go(
            '^.laSearch', {
                limit: 5
            })

    }
})

//Controller for the navbar of all unauth states
app.controller('unauthNavController', function($scope, AuthService) {
    var $ctrl = this;

    //Functions to open signup and login modals
    $ctrl.openSignupModal = AuthService.openSignupModal;
    $ctrl.openLoginModal = AuthService.openLoginModal;
    $scope.isCollapsed = true;

});

//Controller for the navbar of all auth states
app.controller('authNavController', function($scope, $state, AuthService) {
    var $ctrl = this;
    $ctrl.logout = logout;
    $scope.user = AuthService.getUser();
    $scope.isCollapsed = true;

    //function to log out and notify the user
    function logout() {
        AuthService.logout()
            .then(function() {
                alert("You have been logged out")
                $state.reload();
            })
    }

    //When the profile has been edited, the user's profile pic or name may need to be updated
    $scope.$on('updateUser', function(event, args) {
        $scope.user = AuthService.getUser();
    })
});

app.controller('loginController', function($scope, $uibModalInstance, $state, alertFactory, AuthService) {
    var $ctrl = this;
    $ctrl.alerts = [];
    $ctrl.openSignupModal = openSignupModal;
    $ctrl.submitLoginRequest = submitLoginRequest;
    $ctrl.addAlert = addAlert;
    $ctrl.closeAlert = closeAlert;
    $ctrl.clearData = clearData;

    //The function to jump to the signup modal
    function openSignupModal() {
        //use uibModalInstance's close action and mark the reason as 'signup'
        $uibModalInstance.close('signup');
    }

    //Function to submit the login request
    function submitLoginRequest() {
        if ($scope.loginForm.$valid) {
            AuthService.login($ctrl.username, $ctrl.password)
                .then(function() {
                    //if successful, clear the current data, reload state to be redirected to the
                    //corresponding auth state.
                    $ctrl.clearData();
                    $state.reload();
                    //use uibModalInstance's close action and mark the reason as 'success'
                    $uibModalInstance.close('success');
                }).catch(function() {
                    //if error, clear the current data and give user the actionable error msg.
                    $ctrl.clearData();
                    $ctrl.addAlert('danger', "Invalid username and/or password")
                })
        }
    }

    //The function to display alert
    function addAlert(type, message) {
        alertFactory.addAlert($ctrl, type, message);
    }

    //The function to close the chosen alert
    function closeAlert(index) {
        alertFactory.closeAlert($ctrl, index);
    }

    //The function to clear username and password
    function clearData() {
        $ctrl.username = undefined;
        $ctrl.password = undefined;
    }
});

//The controller for the signup modal
app.controller('signupController', function($scope, $uibModalInstance, $rootScope, $http, $state, utils, alertFactory) {
    var $ctrl = this;
    $ctrl.alerts = [];
    $ctrl.openLoginModal = openLoginModal;
    $ctrl.submitSignupRequest = submitSignupRequest;
    $ctrl.addAlert = addAlert;
    $ctrl.closeAlert = closeAlert;

    //The function to close the signup window and open the login window
    function openLoginModal() {
        $uibModalInstance.close('login');
    }

    //The function to submit the request to register a new account
    function submitSignupRequest() {
        //Only send the http request when all inputs are valid
        if ($scope.signupForm.$valid) {
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
                //Go to the signin modal
                $uibModalInstance.close('login');
                utils.requestEnd()
            }, function errorCallback(response) {
                //Give the user actionable error message
                $ctrl.addAlert('danger', response.data.message)
                utils.requestEnd()
            });
        }
    }

    //The function to display alert
    function addAlert(type, message) {
        alertFactory.addAlert($ctrl, type, message);
    }

    //The function to close the chosen alert
    function closeAlert(index) {
        alertFactory.closeAlert($ctrl, index);
    }
});

//The controller for the local advisor search partial
app.controller('laSearchController', function($scope, localAdvisors, cities, $state, $stateParams, searchHelper, utils) {
    $scope.localAdvisors = localAdvisors
    //All city options
    $scope.cities = cities
    $scope.sendSearchRequest = sendSearchRequest;
    //All local advisors to be displayed
    $scope.displayCollection = [].concat($scope.localAdvisors);
    //placeholder for the datepicker
    $scope.datepicker_placeholder = "Expected Date"
    $scope.dateOptions = {
        formatYear: 'yy',
        maxDate: new Date(2020, 5, 22),
        minDate: new Date(),
        startingDay: 1
    };

    //function to redirect to a local advisor's homepage
    $scope.viewDetails = function(param) {
        id = param.id;

        $state.go(
            '^.advisorDetail', {
                id: id
            })
    }

    //The function sends request to search for local advisors with given criteria
    function sendSearchRequest() {
        //All three criteria are optional. Except for keyword, the other two need to be processed before sent.
        available_date = $scope.dt ? moment($scope.dt).format("YYYY-MM-DD") : undefined
        keyword = $scope.searchString ? $scope.searchString : undefined
        city_id = $scope.selected_city ? $scope.selected_city.id : undefined

        searchHelper.searchLocalAdvisors({
            keyword: keyword,
            available_date: available_date,
            city_id: city_id,
            request_fields: [
                'first_name',
                'local_advisor_profile',
                'id',
                'last_name',
                'average_rating',
                'profile_photo_url'
            ]
        }).then(function(data) {
            $scope.localAdvisors = data
            //refreseh the local advisors to be displaed
            $scope.displayCollection = [].concat($scope.localAdvisors);
            $scope.isLoading = false
            utils.requestEnd();
        })

    }

});

//The controller for the local advisor's detail page partial
app.controller('advisorDetailController', function($scope, advisor, $state, $stateParams, utils, alertFactory, AuthService, dbUpdater, $uibModal) {
    $scope.alerts = [];
    $scope.addAlert = addAlert;
    $scope.closeAlert = closeAlert;
    //Get current logged in user info
    $scope.user = AuthService.getUser();
    //Those two functions are prepared for unauth states. Users need to sign in to give comments.
    $scope.openLoginModal = AuthService.openLoginModal;
    $scope.openSignupModal = AuthService.openSignupModal;
    $scope.checkAvailability = checkAvailability;
    //Collect all available dates in a list for the local advisor
    $scope.available_dates = advisor.local_advisor_profile.available_dates.map(function(available_date) {
        return available_date.date
    })

    $scope.advisor = advisor
    //Count the number of reviews
    $scope.review_count = advisor.local_advisor_profile.reviews.length
    //The reviews to be displayed
    $scope.displayCollection = [].concat($scope.advisor.local_advisor_profile.reviews)
    $scope.submitPostReviewRequest = submitPostReviewRequest
    $scope.newReview = null

    //The paginator attributes for recommendations provided list
    $scope.currentPage = 1
    $scope.pageChanged = pageChanged
    $scope.numPerPage = 6
    //Initialize the paginator
    $scope.pageChanged()

    function addAlert(type, message) {
        alertFactory.addAlert($scope, type, message);
    }

    function closeAlert(index) {
        alertFactory.closeAlert($scope, index);
    }

    //The function to post a new review
    function submitPostReviewRequest() {
        //Manually check if the rating is given since it is not covered by the validation module
        if (!$scope.newReview || !$scope.newReview.rating) {
            addAlert('danger', "A rating needs to be submitted")
        }

        //Only send the http request when all inputs are valid
        if ($scope.reviewForm.$valid) {
            dbUpdater.createNewReview({
                title: $scope.newReview.title,
                content: $scope.newReview.content,
                rating: $scope.newReview.rating,
                reviewer_id: $scope.user.id,
                local_advisor_profile_id: $scope.advisor.local_advisor_profile.id
            }).then(function(review) {
                utils.requestEnd();
                $scope.addAlert('success', "Your review has been successfully submitted")
                //Update the review list
                $scope.advisor.local_advisor_profile.reviews.push(review)
                //Update the average rating
                $scope.advisor.average_rating = ($scope.advisor.average_rating * $scope.review_count + $scope.newReview.rating) / ($scope.review_count + 1)
                //clear the comment area
                $scope.newReview = null

                //refresh review_count
                $scope.review_count += 1
                $scope.displayCollection = [].concat($scope.advisor.local_advisor_profile.reviews)
            }).catch(function(response) {
                utils.requestEnd();
                addAlert('danger', response.data.message)
            })
        }
    }

    //The function to open a calendar and display all available dates of the local advisor
    function checkAvailability() {
        var modalInstance = $uibModal.open({
            ariaLabelledBy: 'modal-title',
            ariaDescribedBy: 'modal-body',
            templateUrl: '/static/partials/detail/availabilityModal.html',
            windowClass: 'dateModal',
            scope: $scope,
            size: 'sm',
            controller: function($scope, $filter) {
                $scope.dateOptions = {
                    formatYear: 'yy',
                    maxDate: new Date(2020, 5, 22),
                    minDate: new Date(),
                    startingDay: 1,
                    //The function defines which date should be disabled
                    dateDisabled: function(date, mode) {
                        //disable all dates that don't exist in the available dates list
                        if (date.mode == 'day') {
                            date_to_check = moment(date.date).format("YYYY-MM-DD")

                            if ($scope.available_dates.indexOf(date_to_check) == -1) {
                                return true
                            }
                            return false
                        }
                    },
                    //The function customizes html class for dates that satisfy the given criteria
                    customClass: function(date) {
                        if (date.mode == 'day') {
                            date_to_check = moment(date.date).format("YYYY-MM-DD")

                            //unavailable dates will not have additional class
                            if ($scope.available_dates.indexOf(date_to_check) == -1) {
                                return ''
                            }

                            //available dates will have the class 'btn-date-available'
                            return 'btn-date-available'
                        }
                    }
                };
            }
        })
    }

    //This function manages page change action of the provided recommendation list
    function pageChanged() {
        //caculate the begin and end index of the recommendation list to be displayed for the current page
        var begin = (($scope.currentPage - 1) * $scope.numPerPage)
        var end = begin + $scope.numPerPage;

        $scope.recommendations_to_show = $scope.advisor.local_advisor_profile.recommendations.slice(begin, end);
    }

    //This function will redirect the user to the detail page of certain recommendation
    $scope.viewRecommendationDetails = function(param) {
        id = param.id;

        $state.go(
            '^.recDetail', {
                id: id
            })
    }
});

//The controller for the local recommendation search partial
app.controller('locRecController', function($scope, recommendations, cities, recommendation_categories, $state, $stateParams, searchHelper, utils) {
    //all city options
    $scope.cities = cities
    //all recommendation category options
    $scope.recommendation_categories = recommendation_categories
    $scope.recommendations = recommendations
    $scope.sendSearchRequest = sendSearchRequest;
    //recommnedation to be displayed
    $scope.displayCollection = [].concat($scope.recommendations);

    //The function redirect the user to the detail page of certain recommendation
    $scope.viewDetails = function(param) {
        id = param.id;
        $state.go(
            '^.recDetail', {
                id: id
            })
    }

    //The function will resend search request with new criteria and refresh results
    function sendSearchRequest() {
        //both city and recommendation can be not defined
        city_id = $scope.selected_city ? $scope.selected_city.id : undefined
        recommendation_category_id = $scope.selected_recommendation_category ? $scope.selected_recommendation_category.id : undefined

        searchHelper.searchRecommendations({
            city_id: city_id,
            recommendation_category_id: recommendation_category_id,
            request_fields: [
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
        }).then(function(data) {
            $scope.recommendations = data
            //refresh the display results
            $scope.displayCollection = [].concat($scope.recommendations);
            $scope.isLoading = false
            utils.requestEnd();
        })

    }

});

//The controller for the recommendation detail partial
app.controller('recDetailController', function($scope, recommendation, $state, $stateParams, utils, alertFactory, AuthService, dbUpdater) {
    $scope.alerts = [];
    $scope.addAlert = addAlert;
    $scope.closeAlert = closeAlert;
    //Get current user information
    $scope.user = AuthService.getUser();
    //Those two functions are prepared for unauth states. Users need to sign in to give comments and recommend this place.
    $scope.openLoginModal = AuthService.openLoginModal;
    $scope.openSignupModal = AuthService.openSignupModal;
    $scope.recommendation = recommendation
    //count the number of reviews
    $scope.review_count = recommendation.reviews.length
    $scope.displayCollection = [].concat($scope.recommendation.reviews)
    $scope.submitPostReviewRequest = submitPostReviewRequest
    $scope.recommendPlaceRequest = recommendPlaceRequest
    $scope.provideRecommendationRequest = provideRecommendationRequest
    //The new comment object
    $scope.newReview = null

    //The attributes required for the Google Map display
    $scope.map = {
        center: {
            latitude: recommendation.geo.lat,
            longitude: recommendation.geo.lng
        },
        zoom: 8
    };
    //The marker to show where the recommendation is
    $scope.geo = {
        latitude: recommendation.geo.lat,
        longitude: recommendation.geo.lng
    }

    //Paginator attributes for recommender list
    $scope.currentPage1 = 1
    $scope.pageChanged1 = pageChanged1
    $scope.numPerPage1 = 8
    $scope.pageChanged1()

    //Paginator for local advisor meetup list
    $scope.currentPage2 = 1
    $scope.pageChanged2 = pageChanged2
    $scope.numPerPage2 = 6
    $scope.pageChanged2()

    //Check if the current logged in user has recommended this place already
    if (!$scope.user ||
        $scope.recommendation.recommenders.map(function(recommender) {
            return recommender.id
        }).indexOf($scope.user.id) == -1
    ) {
        $scope.recommend_already = false
    } else {
        $scope.recommend_already = true
    }

    //If the current user is a local adviosr, check if the user has provided this recommendation
    if (
        $scope.user &&
        $scope.user.role.id == 2 &&
        $scope.recommendation.local_advisor_profiles.map(function(local_advisor_profile) {
            return local_advisor_profile.entity[0].id
        }).indexOf($scope.user.id) != -1
    ) {
        $scope.provide_already = true
    } else {
        $scope.provide_already = false
    }

    function addAlert(type, message) {
        alertFactory.addAlert($scope, type, message);
    }

    function closeAlert(index) {
        alertFactory.closeAlert($scope, index);
    }

    //The function to send request to post a new review
    function submitPostReviewRequest() {
         //Manually check if the rating is given since it is not covered by the validation module
        if (!$scope.newReview || !$scope.newReview.rating) {
            addAlert('danger', "A rating needs to be submitted")
        }

        //Only submit the http request when all inputs are valid
        if ($scope.reviewForm.$valid) {
            dbUpdater.createNewReview({
                title: $scope.newReview.title,
                content: $scope.newReview.content,
                rating: $scope.newReview.rating,
                reviewer_id: $scope.user.id,
                recommendation_id: $scope.recommendation.id
            }).then(function(review) {
                utils.requestEnd();
                $scope.addAlert('success', "Your review has been successfully submitted")
                //Refresh the review list and recalculate the average score of the recommendation
                $scope.recommendation.reviews.push(review)
                $scope.recommendation.average_rating = ($scope.recommendation.average_rating * $scope.review_count + $scope.newReview.rating) / ($scope.review_count + 1)
                //clear the comment area
                $scope.newReview = null

                //refresh review_count and review lists
                $scope.review_count += 1
                $scope.displayCollection = [].concat($scope.recommendation.reviews)
            }).catch(function(response) {
                utils.requestEnd();
                addAlert('danger', response.data.message)
            })
        }
    }

    //The function for a user to recommend this recommendation
    function recommendPlaceRequest() {
        //Force user to login if not logged in
        if (!$scope.user) {
            $scope.openLoginModal()
        } else {
            dbUpdater.createNewEntityRecommendation({
                user_id: $scope.user.id,
                recommendation_id: $scope.recommendation.id
            }).then(function(entity_recommendation) {
                utils.requestEnd();
                //refresh the recommender list
                $scope.recommendation.entity_recommendations.push(entity_recommendation)
                $scope.recommendation.recommenders.push(entity_recommendation.entity)
                //Refresh the current page
                pageChanged1()
                //Mark the recommend_already as true
                $scope.recommend_already = true
            }).catch(function(response) {
                utils.requestEnd();
                addAlert('danger', response.data.message)
            })
        }
    }

    //The function for a local advisor to claim that he or she can provide the recommendation
    function provideRecommendationRequest() {
        dbUpdater.createNewLocalAdvisorProfileRec({
            user_id: $scope.user.id,
            recommendation_id: $scope.recommendation.id
        }).then(function(local_advisor_profile) {
            utils.requestEnd();
            //refresh the meetup list
            $scope.recommendation.local_advisor_profiles.push(local_advisor_profile)
            pageChanged2()
            $scope.provide_already = true
        }).catch(function(response) {
            utils.requestEnd();
            addAlert('danger', response.data.message)
        })
    }

    //This function manages page change action of the recommender list 
    function pageChanged1() {
        //caculate the begin and end index of the recommender list to be displayed for the current page
        var begin = (($scope.currentPage1 - 1) * $scope.numPerPage1)
        var end = begin + $scope.numPerPage1;

        $scope.recommenders_to_show = $scope.recommendation.recommenders.slice(begin, end);
    }

    //This function manages page change action of the meetup list
    function pageChanged2() {
        //caculate the begin and end index of the meetup list to be displayed for the current page
        var begin = (($scope.currentPage2 - 1) * $scope.numPerPage2)
        var end = begin + $scope.numPerPage2;

        $scope.local_advisors_to_show = $scope.recommendation.local_advisor_profiles.slice(begin, end);
    }

    //This function redirect the user to a local advisor's homepage
    $scope.viewAdvisorDetails = function(param) {
        id = param.id;

        $state.go(
            '^.advisorDetail', {
                id: id
            })
    }

});

//This controller is for the contact list partial
app.controller('messengerController', function($scope, searchHelper, userContacts, utils, AuthService) {
    self_user = AuthService.getUser()
    //fill the user contact list whose minimum length is 10 with the user contacts of the current user
    $scope.userContacts = utils.fillFallbackList(userContacts, 10)
    $scope.displayContacts = [].concat($scope.userContacts)
    $scope.searchUsers = searchUsers
    $scope.onContactSelect = onContactSelect

    //This function will look up users with the given keyword
    function searchUsers(keyword) {
        return searchHelper.searchUsers({
            keyword: keyword,
            limit: 8,
            request_fields: [
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

    //This function will shift the chosen user to the first place of contact list
    function onContactSelect(item, model, label) {
        contact_id_list = userContacts.map(function(contact) {
            return contact.user.id
        })

        //Shift the contact to the first place of the contact list
        if (contact_id_list.indexOf(model.id) == -1 && model.id != self_user.id) {
            userContacts.unshift({
                "user": model,
                "unread_count": 0
            })
            $scope.userContacts = utils.fillFallbackList(userContacts, 10)
            $scope.displayContacts = [].concat($scope.userContacts)
        }
    }

    //When the user enters the chat panel with another, the unread count for that contact will become 0
    $scope.$on('panelEntered', function(event, args) {
        $scope.userContacts.forEach(function(contact) {
            if (contact.user && contact.user.id == args) {
                contact.unread_count = 0
            }
        })
    })
})


app.controller('messengerChatPanelController', function($scope, $stateParams, utils, messageHistory, AuthService, socketService) {
    //Self Information
    self_user = AuthService.getUser()
    $scope.self_id = self_user.id
    $scope.self_name = self_user.first_name + ' ' + self_user.last_name
    $scope.self_profile_photo_url = self_user.profile_photo_url
    //replace profile photo if invalid
    utils.replaceInvalidImages($scope, 'self_profile_photo_url')

    //The other chatter's information
    $scope.contact_id = $stateParams.user_id;
    $scope.contact_name = $stateParams.first_name + ' ' + $stateParams.last_name
    $scope.contact_profile_photo_url = $stateParams.profile_photo_url
    //replace profile photo if invalid
    utils.replaceInvalidImages($scope, 'contact_profile_photo_url')

    $scope.messageHistory = messageHistory

    $scope.send_message = send_message;
    $scope.cur_room_id = null;

    //join the chatroom, emit to the action signal to the backend socket
    var room = {
        currentUser: $scope.self_id,
        targetUser: $scope.contact_id
    };
    socketService.emit('join', room);

    //Message sending action listener which is responsible of processing
    //message sent from socket server
    socketService.on('message', function(msg, str) {
        //if the room is not initialzed, it will be
        if ($scope.cur_room_id == null) {
            $scope.cur_room_id = msg['room'];
        }

        var msg_history = $scope.messageHistory;
        var sender_id = parseInt(msg['sender']);
        var receiver_id = parseInt(msg['receiver']);

        var newId = msg_history.length == 0 ? 1 : msg_history[msg_history.length - 1]['id'] + 1;

        //Upon message received, push the message to the chat history
        if (msg['type'] === 'msg' || msg['type'] === 'offline') {
            $scope.messageHistory.push({
                id: newId,
                message_body: msg['body'],
                read_at: null,
                receiver: receiver_id,
                sender: sender_id,
                //will be parsed by filter
                sent_at: new Date()
            })
        };

    });

    //For debugging
    socketService.on('send message', function(msg, str) {
        console.log(msg);
    });

    //For debugging
    socketService.on('join', function(data) {
        console.log(data);
    });

    //The funtion to send message to the socket server
    function send_message() {
        data = {};
        data['body'] = $scope.message_to_send;
        data['receiver'] = $scope.contact_id;
        data['sender'] = $scope.self_id;
        data['room'] = $scope.cur_room_id;
        socketService.emit('send message', data);

        $scope.message_to_send = null;
    }
});

//The controller for the recommendation creation partial
app.controller('recCreationController', function($scope, cities, recommendation_categories, utils, fileManager, AuthService, recManager, alertFactory) {
    $scope.alerts = [];
    $scope.addAlert = addAlert;
    $scope.closeAlert = closeAlert;
    //For recommender
    $scope.user = AuthService.getUser();

    $scope.cities = cities
    $scope.recommendation_categories = recommendation_categories
    $scope.submitRecCreationRequest = submitRecCreationRequest
    //The placeholder for the recommendation photo
    $scope.displayed_recommendation_photo = "/static/images/placeholder.png"

    //Upload the recommendation picture to the S3
    $scope.doUpload = function() {
        fileManager.uploadFile(event.target.files[0]).then(function(data) {
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

    //Submit the request to create the new Recommendation
    function submitRecCreationRequest() {
        //Only send the http request when all inputs are valid
        if ($scope.recCrtForm.$valid) {
            recManager.createNewRec({
                title: $scope.title,
                description: $scope.description,
                address_line_one: $scope.address_line_one,
                address_line_two: $scope.address_line_two,
                zip_code: $scope.zip_code,
                city_id: $scope.selected_city.id,
                recommendation_category_id: $scope.selected_recommendation_category.id,
                recommender_id: $scope.user.id,
                file_id: $scope.current_photo.id
            }).then(function(data) {
                //Display success message
                utils.requestEnd();
                $scope.addAlert('success', "Your recommendation has been successfully created!")
            }).catch(function(data) {
                utils.requestEnd();
                addAlert('danger', "Failed to create the new recommendation")
            })
        }
    }
})

//The controller for the profile editing partial
app.controller('editProfileController', function($scope, utils, fileManager, AuthService, alertFactory, $rootScope) {
    $scope.alerts = [];
    $scope.addAlert = addAlert;
    $scope.closeAlert = closeAlert;
    $scope.user = AuthService.getUser();
    //The placeholder text for the datepicker
    $scope.datepicker_placeholder = "Choose Your Birthday"
    $scope.dateOptions = {
        formatYear: 'yy',
        maxDate: new Date(2020, 5, 22)
    };

    //Display current user profile
    $scope.first_name = $scope.user.first_name
    $scope.last_name = $scope.user.last_name
    $scope.email = $scope.user.email
    if ($scope.user.birthday) {
        birthday = new Date($scope.user.birthday.date)
        $scope.dt = new Date()
        $scope.dt.setDate(birthday.getDate() + 1)
    }
    $scope.phone_number = $scope.user.phone_number

    $scope.displayed = $scope.user
    //Replace the profile photo if it is not a valid url
    utils.replaceInvalidImages($scope.displayed, 'profile_photo_url')

    $scope.submitEditProfileRequest = submitEditProfileRequest

    //Upload the given profile picture to S3 server
    $scope.doUpload = function() {
        fileManager.uploadFile(event.target.files[0]).then(function(data) {
            $scope.displayed.profile_photo_url = data.download_link
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

    //Submit the request to update profile.
    function submitEditProfileRequest() {
        if ($scope.recCrtForm.$valid) {
            AuthService.updateUser({
                user_id: $scope.user.id,
                first_name: $scope.first_name,
                last_name: $scope.last_name,
                phone_number: $scope.phone_number,
                email: $scope.email,
                //MomentJS will convert the date to the acceptable format
                birthday: $scope.dt ? moment($scope.dt).format("YYYY-MM-DD") : undefined,
                file_id: $scope.current_photo ? $scope.current_photo.id : undefined
            }).then(function(data) {
                utils.requestEnd();
                //clear the current photo in case of duplicate picture uploading
                $scope.current_photo = null
                //Send signal for navigation bar to update username and profile picture display
                $rootScope.$broadcast('updateUser');
                $scope.addAlert('success', "Your profile has been updated")
            }).catch(function(response) {
                utils.requestEnd();
                addAlert('danger', response.data.message)
            })
        }
    }
})