var app = angular.module('HairyDolphinsApp');

//The factory wich provides functions to signin/signout, update user and
//get current user information
app.factory('AuthService',
    function($q, $timeout, $http, utils, $rootScope, $uibModal) {

        //current user information is stored in this variable
        var user = null;

        //Function map
        var factory = {
            isLoggedIn: isLoggedIn,
            login: login,
            logout: logout,
            loadCurrentUser: loadCurrentUser,
            getUser: getUser,
            openLoginModal: openLoginModal,
            openSignupModal: openSignupModal,
            updateUser: updateUser,
        }

        // return available functions for use in controllers
        return factory;

        //Get the current user stored
        function getUser() {
            return user;
        }

        //Check if the user has signed in
        function isLoggedIn() {
            if (user) {
                return true;
            } else {
                return false;
            }
        }

        //Signin the user with given username and password
        function login(username, password) {
            // create a new instance of deferred
            utils.requestStart();

            //Process should continue after the specified steps has been finished
            var deferred = $q.defer();

            // send a post request to the server
            $http({
                    method: 'POST',
                    url: '/auth/signin',
                    params: {
                        username: username,
                        password: password
                    }
                })
                // handle success
                .success(function(data, status) {
                    if (status === 200) {
                        //replace profile picture if invalid
                        utils.replaceInvalidImages(data, 'profile_photo_url')
                        //Store the user information
                        user = data;
                        deferred.resolve();
                    } else {
                        user = null;
                        deferred.reject();
                    }

                    utils.requestEnd();
                })
                // handle error
                .error(function(data) {
                    user = null;
                    deferred.reject();

                    utils.requestEnd();
                });



            // return promise object
            return deferred.promise;

        }

        //Logout he user who has been logged in
        function logout() {
            utils.requestStart();
            // create a new instance of deferred
            var deferred = $q.defer();

            // send a get request to the server
            $http.get('/auth/logout')
                // handle success
                .success(function(data) {
                    user = null;
                    deferred.resolve();
                    utils.requestEnd();
                })
                // handle error
                .error(function(data) {
                    user = null;
                    deferred.reject();
                    utils.requestEnd();
                });

            // return promise object
            return deferred.promise;

        }

        //Load the user who is currently logged in from backend
        function loadCurrentUser() {
            var deferred = $q.defer();

            $http.get('/auth/current_user')
                .success(function(data, status) {
                    if (status === 200) {
                        //replace profile picture if invalid
                        utils.replaceInvalidImages(data, 'profile_photo_url')
                        user = data;
                        deferred.resolve();
                    } else {
                        user = null;
                        deferred.reject();
                    }
                })
                .error(function(data) {
                    user = null;
                    deferred.reject();
                });

            return deferred.promise;
        }

        //Open the login modal
        function openLoginModal() {
            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                templateUrl: '/static/directives/login.html',
                controller: 'loginController',
                controllerAs: '$ctrl',
                size: 'sm'
            });

            //Jump to signup modal
            modalInstance.result.then(function(result) {
                if (result === 'signup') {
                    factory.openSignupModal();
                }
            });
        }

        //Open the signup modal
        function openSignupModal() {
            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                templateUrl: '/static/directives/signup.html',
                controller: 'signupController',
                controllerAs: '$ctrl',
                size: 'sm'
            });

            //Jump to login modal
            modalInstance.result.then(function(result) {
                if (result === 'login') {
                    factory.openLoginModal();
                }
            });
        }

        //Update the user profile
        function updateUser(params) {
            utils.requestStart()

            return $http({
                method: 'PUT',
                url: '/api/users/' + params.user_id,
                params: params
            }).then(function(data, status) {
                //replace the user profile photo if invalid
                utils.replaceInvalidImages(data.data, 'profile_photo_url')
                user = data.data
                return data.data
            })
        }

    });

//The factory which provides functions to display or close alerts.
app.factory('alertFactory', function() {
    var factory = {};

    factory.addAlert = addAlert;
    factory.closeAlert = closeAlert;

    //The controller which has the alerts, message type and message content are required
    function addAlert($ctrl, type, message) {
        //messsage can be a string or a json which has a key and a string.
        if (typeof message === 'string') {
            $ctrl.alerts.push({
                type: type,
                msg: message
            });
        } else {
            //For the non-string case. The key would be where the error happens and
            //message is the detail.
            Object.keys(message).forEach(function(key) {
                $ctrl.alerts.push({
                    type: type,
                    msg: key + " : " + message[key]
                });
            });
        }
    }

    //The function to close the chosen alert
    function closeAlert($ctrl, index) {
        $ctrl.alerts.splice(index, 1);
    }

    return factory;
})

//This factory provides all functions to get or search all different kinds of data
app.factory('searchHelper', function($q, $http, utils, AuthService) {
    var factory = {};

    //Function map
    factory.searchLocalAdvisors = searchLocalAdvisors;
    factory.getAdvisorDetail = getAdvisorDetail;
    factory.getRecDetail = getRecDetail;
    factory.searchUsers = searchUsers;
    factory.searchRecommendations = searchRecommendations;
    factory.searchUserContacts = searchUserContacts;
    factory.searchMessageHistory = searchMessageHistory;
    factory.getCityOptions = getCityOptions;
    factory.getRecommendationCategoryOptions = getRecommendationCategoryOptions;

    //The function to search for recommendations with search criteria
    function searchRecommendations(params) {
        utils.requestStart()

        return $http({
            method: 'GET',
            url: '/api/recommendations',
            params: params
        }).then(function(data, status) {
            recommendations = data.data

            //To modify returned data to adapt to the front end
            data.data.forEach(function(recommendation) {
                utils.replaceInvalidImages(recommendation, 'primary_picture')

                //Concatenate the address
                if (recommendation.address_line_one) {
                    recommendation.complete_address = recommendation.address_line_one +
                        (recommendation.address_line_two ? ' ' + recommendation.address_line_two : '') + ', ' +
                        recommendation.city.label + ', ' +
                        recommendation.city.state.label + ', ' +
                        recommendation.city.state.country.label + ', ' +
                        recommendation.zip_code
                }

                //Replace recommender's profile pictures
                if (recommendation.entity_recommendations) {
                    recommendation.entity_recommendations.forEach(function(entity_recommendation) {
                        utils.replaceInvalidImages(entity_recommendation.entity, 'profile_photo_url')
                    })

                    //The orignal recommender should also be in the list
                    recommendation.recommenders = [recommendation.recommender].concat(recommendation.entity_recommendations.map(function(entity_recommendation) {
                        return entity_recommendation.entity
                    }))
                } else {
                    recommendation.recommenders = [recommendation.recommender]
                }

                //Replace all local advisors' profile pictures inside meetup list
                if (recommendation.local_advisor_profiles) {
                    recommendation.local_advisor_profiles.forEach(function(local_advisor_profile) {
                        utils.replaceInvalidImages(local_advisor_profile.entity[0], 'profile_photo_url')
                    })
                }

            })

            return data.data
        }, function(data) {
            return []
        })
    }

    //Get a local advisor with the id
    function getAdvisorDetail(params) {
        utils.requestStart()

        return $http({
            method: 'GET',
            url: '/api/users/' + params.id,
            params: params
        }).then(function(data, status) {
            utils.replaceInvalidImages(data.data, 'profile_photo_url')

            //Replace reviewers' profile pictures if invalid
            if (data.data.local_advisor_profile.reviews) {
                data.data.local_advisor_profile.reviews.forEach(function(review) {
                    utils.replaceInvalidImages(review.reviewer, 'profile_photo_url')
                })
            }

            //Relpace the provided recommendatons' pictures if invalid
            if (data.data.local_advisor_profile.recommendations) {
                data.data.local_advisor_profile.recommendations.forEach(function(recommendation) {
                    utils.replaceInvalidImages(recommendation, 'primary_picture')
                })
            }

            return data.data
        }, function(data) {
            return []
        })
    }

    //The function to get a local recommendation with id
    function getRecDetail(params) {
        utils.requestStart()

        return $http({
            method: 'GET',
            url: '/api/recommendations/' + params.id,
            params: params
        }).then(function(data, status) {
            recommendation = data.data

            utils.replaceInvalidImages(data.data, 'primary_picture')

            //Replace reviewers' profile pictures if invalid
            if (data.data.reviews) {
                data.data.reviews.forEach(function(review) {
                    utils.replaceInvalidImages(review.reviewer, 'profile_photo_url')
                })
            }

            //Replace recommenders' profile pictures if invalid
            if (data.data.entity_recommendations) {
                data.data.entity_recommendations.forEach(function(entity_recommendation) {
                    utils.replaceInvalidImages(entity_recommendation.entity, 'profile_photo_url')
                })

                //The orignal recommender should also be in the list
                data.data.recommenders = [data.data.recommender].concat(data.data.entity_recommendations.map(function(entity_recommendation) {
                    return entity_recommendation.entity
                }))
            } else {
                data.data.recommenders = [data.data.recommender]
            }

            //Replace all local advisors' profile pictures inside meetup list
            if (data.data.local_advisor_profiles) {
                data.data.local_advisor_profiles.forEach(function(local_advisor_profile) {
                    utils.replaceInvalidImages(local_advisor_profile.entity[0], 'profile_photo_url')
                })
            }

            //Concatenate the address
            data.data.complete_address = recommendation.address_line_one +
                (recommendation.address_line_two ? ' ' + recommendation.address_line_two : '') + ', ' +
                recommendation.city.label + ', ' +
                recommendation.city.state.label + ', ' +
                recommendation.city.state.country.label + ', ' +
                recommendation.zip_code

            //Get the geo location of the recommendation using its complete address
            return $http({
                method: 'GET',
                url: 'https://maps.googleapis.com/maps/api/geocode/json',
                params: {
                    address: data.data.complete_address,
                }
            }).then(function(response) {
                data.data.geo = response.data.results[0].geometry.location
                return data.data
            })
        }, function(data) {
            return []
        })
    }

    //The function to search local advisors with given criteria, which returns a list of local advisors
    function searchLocalAdvisors(params) {
        utils.requestStart()
        //The role should be contraint to be local adviser
        params.role_id = 2

        return $http({
            method: 'GET',
            url: '/api/users',
            params: params
        }).then(function(data, status) {
            data.data.forEach(function(user) {
                //Replace the profile picture of each local advisor
                utils.replaceInvalidImages(user, 'profile_photo_url')

                if (user.local_advisor_profile) {
                    user.local_advisor_profile.recommendations.forEach(function(recommendation) {
                        utils.replaceInvalidImages(recommendation, 'primary_picture')
                    })
                }
            })

            return data.data
        }, function(data) {
            return []
        })
    }

    //Search users with the given criteria.
    function searchUsers(params) {
        return $http({
            method: 'GET',
            url: '/api/users',
            params: params
        }).then(function(data, status) {
            //Replace the profile picture of each user
            data.data.forEach(function(user) {
                utils.replaceInvalidImages(user, 'profile_photo_url')
            })

            return data.data
        }, function(data) {
            return []
        })
    }

    //Get a user's contacts with the id of the user
    function searchUserContacts() {
        utils.requestStart()

        //Load the user first to make sure the user has logged in
        return AuthService.loadCurrentUser()
            .then(function() {
                current_user_id = AuthService.getUser().id
                return $http({
                    method: 'GET',
                    url: '/api/users/' + current_user_id,
                    params: {
                        //we only want contacts
                        request_fields: ['contacts']
                    }
                }).then(function(data, status) {
                    return data.data.contacts
                }, function(data) {
                    return []
                })
            }, function() {
                utils.requestEnd()
                return []
            })
    }

    //Get the message history between the logged in user and the other user
    function searchMessageHistory(other_user_id) {
        utils.requestStart()

        //Load the user first to make sure the user has logged in
        return AuthService.loadCurrentUser()
            .then(function() {
                current_user_id = AuthService.getUser().id
                return $http({
                    method: 'GET',
                    url: '/api/messages',
                    params: {
                        bidirect_user_one: current_user_id,
                        bidirect_user_two: other_user_id
                    }
                }).then(function(data, status) {
                    return data.data
                }, function(data) {
                    return []
                })
            }, function() {
                utils.requestEnd()
                return []
            })
    }

    //Get all city options
    function getCityOptions() {
        utils.requestStart()

        return $http({
            method: 'GET',
            url: '/api/cities',
        }).then(function(data, status) {
            return data.data
        }, function(data) {
            return []
        })
    }

    //Get all recommendation category options
    function getRecommendationCategoryOptions() {
        utils.requestStart()

        return $http({
            method: 'GET',
            url: '/api/recommendation_categories',
        }).then(function(data, status) {
            return data.data
        }, function(data) {
            return []
        })
    }

    return factory;
})

//This factory collects some helper functions that are not categorized
app.factory('utils', function($q, $timeout, $rootScope, $http) {
    var factory = {};

    factory.requestStart = requestStart;
    factory.requestEnd = requestEnd;
    factory.fillFallbackList = fillFallbackList;
    factory.replaceInvalidImages = replaceInvalidImages;

    //Start the spinner
    function requestStart() {
        $rootScope.isLoading = true
    }

    //Stop the spinner
    function requestEnd() {
        $rootScope.isLoading = false
    }

    //Replace invalid picture urls with fallback placeholder image
    function replaceInvalidImages(imageHolder, imageCol) {
        //Only the promise list can achieve our goal
        promises = []

        //If a json hash is given, we are still able to handle it
        if (Array.isArray(imageHolder)) {
            for (var i = 0; i < imageHolder.length; i++) {
                promises.push(valdiateImageUrl(imageHolder[i], imageCol))
            }
        } else {
            promises.push(valdiateImageUrl(imageHolder, imageCol))
        }


        $q.all(promises)
    }

    //The helper function to replace the value with some key with placeholder image if it is invalid in
    //a json hash
    function valdiateImageUrl(imageHolder, imageCol) {
        var d = $q.defer();

        replacement = "/static/images/placeholder.png"

        $timeout(function() {
            //first check if the value is empty
            if (!imageHolder[imageCol]) {
                imageHolder[imageCol] = replacement
                d.resolve()
            } else {
                //Then try to use http request to load this resource
                if (imageHolder[imageCol].indexOf('s3.amazonaws.com/hairydolphins') === -1) {
                    $http.get(imageHolder[imageCol])
                        .error(function() {
                            $http.get($rootScope.s3url + imageHolder[imageCol])
                                .success(function() {
                                    imageHolder[imageCol] = $rootScope.s3url + imageHolder[imageCol]
                                    d.resolve()
                                }).error(function() {
                                    imageHolder[imageCol] = replacement
                                    d.resolve()
                                })
                        })
                }
            }
        }, 1000, false);

        return d.promise;
    }

    /*
    	fallback list is a list which will at least have a certain size of elements. When the list
    	is not filled, all elements are empty. To fill this list, empty element will be filled first,
    	and then new element can be appended.
    */
    function fillFallbackList(fillList, fallbackSize) {
        list = []

        //Form a list of required size filled with empty elements
        for (i = 0; i < fallbackSize; i++) {
            list = list.concat({})
        }

        if (fillList != null) {
            //The size of the fill list can be greater or less than the required size
            if (fillList.length > fallbackSize) {
                //Fill the empty slot when the required size is not attained
                for (i = 0; i < fallbackSize; i++) {
                    list[i] = fillList[i]
                }

                //When the size is attained, we can simply concatenate remainning elements to the list
                for (i = fallbackSize; i < fillList.length; i++) {
                    list = list.concat(fillList[i])
                }
            } else {
                for (i = 0; i < fillList.length; i++) {
                    list[i] = fillList[i]
                }
            }
        }

        return list;

    }

    return factory
})

//The factory to provide socket service
app.factory('socketService', function(socketFactory) {
    //TODO: add read message service logic.
    var mySocket = socketFactory();
    mySocket.forward('message');
    return mySocket;
});

//The factory to upload file to the backend
app.factory('fileManager', function($q, $timeout, utils, $http) {
    var factory = {};

    factory.uploadFile = uploadFile

    function uploadFile(file_to_upload) {
        utils.requestStart()

        //The file needs to be uploaded through a form
        fd = new FormData()
        fd.append("photo", file_to_upload)

        return $http({
            method: 'POST',
            url: '/api/files',
            headers: {
                'Content-Type': undefined
            },
            data: fd
        }).then(function(data, status) {
            return data.data
        }, function(data) {
            return []
        })
    }

    return factory
})

//The factory which provides functions to create, edit or remove recommendations
app.factory('recManager', function($q, $timeout, utils, $http) {
    var factory = {};

    factory.createNewRec = createNewRec

    //The function to create a new recommendation
    function createNewRec(params) {
        utils.requestStart()

        return $http({
            method: 'POST',
            url: '/api/recommendations',
            params: params
        }).then(function(data, status) {
            return data.data
        })
    }

    return factory
})

//The factory which provides functions to create, update entities in the database
app.factory('dbUpdater', function($q, $timeout, utils, $http, AuthService) {
    var factory = {};

    //Function map
    factory.createNewReview = createNewReview
    factory.createNewEntityRecommendation = createNewEntityRecommendation
    factory.createNewLocalAdvisorProfileRec = createNewLocalAdvisorProfileRec
    factory.markMessagesAsRead = markMessagesAsRead

    //The function to create a new review
    function createNewReview(params) {
        utils.requestStart()

        return $http({
            method: 'POST',
            url: '/api/reviews',
            params: params
        }).then(function(data, status) {
            //replace the profile picture of the reviewer if invalid
            utils.replaceInvalidImages(data.data.reviewer, 'profile_photo_url')
            return data.data
        })
    }

    //The function for a user to recommend a recommendation
    function createNewEntityRecommendation(params) {
        utils.requestStart()

        return $http({
            method: 'POST',
            url: '/api/entity_recommendations',
            params: params
        }).then(function(data, status) {
            //replace the profile picture of the recommender if invalid
            utils.replaceInvalidImages(data.data.entity, 'profile_photo_url')
            return data.data
        })
    }

    //The function for a local advisor to provide a recommendation
    function createNewLocalAdvisorProfileRec(params) {
        utils.requestStart()

        return $http({
            method: 'POST',
            url: '/api/local_advisor_profile_recommendations',
            params: params
        }).then(function(data, status) {
            //replace the profile picture of the local advisor if invalid
            utils.replaceInvalidImages(data.data.entity, 'profile_photo_url')
            return data.data
        })
    }

    //The function which sends request to mark messages among given messages whose receiver matches
    //the given user id as read
    function markMessagesAsRead(messages) {
        utils.requestStart()

        return $http({
            method: 'PUT',
            url: '/api/messages',
            params: {
                receiver_id: AuthService.getUser().id,
                messages_to_mark: messages
            }
        }).then(function(data, status) {
            return data.data
        })
    }

    return factory
})
