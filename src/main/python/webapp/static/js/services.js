var app = angular.module('HairyDolphinsApp');

app.factory('AuthService',
  function ($q, $timeout, $http, utils, $rootScope, $uibModal) {

    // create user variable
    var user = null;
    var factory = {
      isLoggedIn: isLoggedIn,
      login: login,
      logout: logout,
      loadCurrentUser: loadCurrentUser,
      getUser: getUser,
      openLoginModal : openLoginModal,
      openSignupModal : openSignupModal,
      updateUser: updateUser,
    }

    // return available functions for use in controllers
    return factory;

    function getUser() {
    	return user;
    }

    function isLoggedIn() {
    	if(user) {
			return true;
		} else {
			return false;
		}
    }

    function login(username, password) {
	    // create a new instance of deferred
	    utils.requestStart();

	    var deferred = $q.defer();

	    // send a post request to the server
	    $http({
	    	method: 'POST',
	    	url : '/auth/signin', 
	    	params: {
	    		username: username,
	    		password: password
	    	}
	    })
	    // handle success
	    .success(function (data, status) {
	    	if(status === 200){
	    		utils.replaceInvalidImages(data, 'profile_photo_url')
	        	user = data;
	        	deferred.resolve();
	    	} else {
	        	user = null;
	        	deferred.reject();
	        }

	        utils.requestEnd();
	    })
	    // handle error
	    .error(function (data) {
	      user = null;
	      deferred.reject();

	      utils.requestEnd();
	    });

	

	  // return promise object
	    return deferred.promise;

    }

    function logout() {
      utils.requestStart();
    	  // create a new instance of deferred
	  var deferred = $q.defer();

	  // send a get request to the server
	  $http.get('/auth/logout')
	    // handle success
	    .success(function (data) {
	      user = null;
	      deferred.resolve();
	      utils.requestEnd();
	    })
	    // handle error
	    .error(function (data) {
	      user = null;
	      deferred.reject();
	      utils.requestEnd();
	    });

	  // return promise object
	  return deferred.promise;

	}

	function loadCurrentUser() {
		var deferred = $q.defer();

		$http.get('/auth/current_user')
			.success(function (data, status) {
			    if(status === 200){
			        utils.replaceInvalidImages(data, 'profile_photo_url')
			        user = data;
			        deferred.resolve();
			    } else {
			      user = null;
			      deferred.reject();
			    }
		    })
		    .error(function (data) {
		        user = null;
		        deferred.reject();
	  	    });

	  	return deferred.promise;
	}

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
                factory.openSignupModal();
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
                factory.openLoginModal();
            }
        });
    }

    function updateUser(params){
    	utils.requestStart()

		return $http({
			method: 'PUT',
			url : '/api/users/' + params.user_id,
			params: params
		}).then(function(data, status){
			utils.replaceInvalidImages(data.data, 'profile_photo_url')
			user = data.data
			return data.data
		})
    }

});

app.factory('alertFactory', function() {
	var factory = {};

	factory.addAlert = addAlert;
	factory.closeAlert = closeAlert;

	function addAlert($ctrl, type, message){
		if(typeof message === 'string'){
                $ctrl.alerts.push({ type: type, msg: message });
        }
        else{
            Object.keys(message).forEach(function (key) {
                $ctrl.alerts.push({ type: type, msg: key + " : " + message[key]});
            });
        }
	}

	function closeAlert($ctrl, index) {
		$ctrl.alerts.splice(index, 1);
	}

	return factory;
})

app.factory('searchHelper', function($q, $http, utils, AuthService) {
	var factory = {};

	factory.searchLocalAdvisors = searchLocalAdvisors;
	factory.getAdvisorDetail = getAdvisorDetail;
	factory.getRecDetail = getRecDetail;
	factory.searchUsers = searchUsers;
	factory.searchRecommendations = searchRecommendations;
	factory.searchUserContacts = searchUserContacts;
	factory.searchMessageHistory = searchMessageHistory;
	factory.getCityOptions = getCityOptions;
	factory.getRecommendationCategoryOptions = getRecommendationCategoryOptions;


	function searchRecommendations(params) {
		utils.requestStart()

		return $http({
			method: 'GET',
			url : '/api/recommendations',
			params: params
		}).then(function(data, status){
			recommendations = data.data

			data.data.forEach(function(recommendation){
				utils.replaceInvalidImages(recommendation, 'primary_picture')

				if(recommendation.address_line_one) {
					recommendation.complete_address = recommendation.address_line_one
			        + (recommendation.address_line_two? ' ' + recommendation.address_line_two:'') + ', '
			        + recommendation.city.label + ', '
			        + recommendation.city.state.label + ', '
			        + recommendation.city.state.country.label + ', '
			        + recommendation.zip_code
		    	}

		        if(recommendation.entity_recommendations) {
			        recommendation.entity_recommendations.forEach(function(entity_recommendation){
						utils.replaceInvalidImages(entity_recommendation.entity, 'profile_photo_url')
					})

					recommendation.recommenders = [recommendation.recommender].concat(recommendation.entity_recommendations.map(function(entity_recommendation){
		    			return entity_recommendation.entity
		    		}))
		  		} else {
		  			recommendation.recommenders = [recommendation.recommender]
		  		}

		  		if(recommendation.local_advisor_profiles) {
					recommendation.local_advisor_profiles.forEach(function(local_advisor_profile){
						utils.replaceInvalidImages(local_advisor_profile.entity[0], 'profile_photo_url')
					})
				}

		    })

			return data.data
		}, function(data) {
			return []
		})
	}

	function getAdvisorDetail(params) {
		utils.requestStart()

		return $http({
			method: 'GET',
			url: '/api/users/' + params.id,
			params: params
		}).then(function(data, status) {
			utils.replaceInvalidImages(data.data, 'profile_photo_url')

			if(data.data.local_advisor_profile.reviews) {
				data.data.local_advisor_profile.reviews.forEach(function(review){
					utils.replaceInvalidImages(review.reviewer, 'profile_photo_url')
				})
			}

			if(data.data.local_advisor_profile.recommendations) {
				data.data.local_advisor_profile.recommendations.forEach(function(recommendation){
					utils.replaceInvalidImages(recommendation, 'primary_picture')
				})
			}

			return data.data
		}, function(data) {
			return []
		})
	}


	function getRecDetail(params) {
		utils.requestStart()

		return $http({
			method: 'GET',
			url: '/api/recommendations/' + params.id,
			params: params
		}).then(function(data, status) {
			recommendation = data.data
			
			utils.replaceInvalidImages(data.data, 'primary_picture')

			if(data.data.reviews) {
				data.data.reviews.forEach(function(review){
					utils.replaceInvalidImages(review.reviewer, 'profile_photo_url')
				})
			}

			if(data.data.entity_recommendations) {
				data.data.entity_recommendations.forEach(function(entity_recommendation){
					utils.replaceInvalidImages(entity_recommendation.entity, 'profile_photo_url')
				})

				data.data.recommenders = [data.data.recommender].concat(data.data.entity_recommendations.map(function(entity_recommendation){
		    		return entity_recommendation.entity
		    	}))
			} else {
				data.data.recommenders = [data.data.recommender]
			}

			if(data.data.local_advisor_profiles) {
				data.data.local_advisor_profiles.forEach(function(local_advisor_profile){
					utils.replaceInvalidImages(local_advisor_profile.entity[0], 'profile_photo_url')
				})
			}

			data.data.complete_address = recommendation.address_line_one
		        + (recommendation.address_line_two? ' ' + recommendation.address_line_two:'') + ', '
		        + recommendation.city.label + ', '
		        + recommendation.city.state.label + ', '
		        + recommendation.city.state.country.label + ', '
		        + recommendation.zip_code

			return $http({
				method: 'GET',
				url : 'https://maps.googleapis.com/maps/api/geocode/json',
				params : {
					address : data.data.complete_address,
					key : 'AIzaSyCe4fuOg-Njod6WBo8P6UPeWhOaOdErsgE'
				}
			}).then(function(response) {
				data.data.geo = response.data.results[0].geometry.location
				return data.data
			})
		}, function(data) {
			return []
		})
	}

	function searchLocalAdvisors(params) {
		utils.requestStart()
		params.role_id = 2

		return $http({
	    	method: 'GET',
	    	url : '/api/users', 
	    	params: params
	    }).then(function(data, status){
	    	data.data.forEach(function(user){
				utils.replaceInvalidImages(user, 'profile_photo_url')

				if(user.local_advisor_profile) {
					user.local_advisor_profile.recommendations.forEach(function(recommendation){
						utils.replaceInvalidImages(recommendation, 'primary_picture')
					})
				}
			})

	    	return data.data
	    }, function(data) {
	    	return []
	    })
	}

	function searchUsers(params) {
		return $http({
	    	method: 'GET',
	    	url : '/api/users', 
	    	params: params
	    }).then(function(data, status){
	    	data.data.forEach(function(user){
				utils.replaceInvalidImages(user, 'profile_photo_url')
			})

	    	return data.data
	    }, function(data) {
	    	return []
	    })
	}

	function searchUserContacts() {
		utils.requestStart()

		return AuthService.loadCurrentUser()
		.then(function(){
			current_user_id = AuthService.getUser().id
			return $http({
		    	method: 'GET',
		    	url : '/api/users/' + current_user_id, 
		    	params: {
		    		request_fields : ['contacts']
		    	}
		    }).then(function(data, status){
		    	return data.data.contacts
		    }, function(data) {
		    	return []
		    })
		}, function(){
			utils.requestEnd()
			return []
		})
	}

	function searchMessageHistory(other_user_id) {
		utils.requestStart()

		return AuthService.loadCurrentUser()
		.then(function(){
			current_user_id = AuthService.getUser().id
			return $http({
		    	method: 'GET',
		    	url : '/api/messages',
		    	params: {
		    		bidirect_user_one : current_user_id,
		    		bidirect_user_two : other_user_id
		    	}
		    }).then(function(data, status){
		    	return data.data
		    }, function(data) {
		    	return []
		    })
		}, function(){
			utils.requestEnd()
			return []
		})
	}

	function getCityOptions() {
		utils.requestStart()

		return $http({
			method: 'GET',
			url : '/api/cities',
		}).then(function(data, status){
			return data.data
		}, function(data) {
			return []
		})
	}

	function getRecommendationCategoryOptions() {
		utils.requestStart()

		return $http({
			method: 'GET',
			url : '/api/recommendation_categories',
		}).then(function(data, status){
			return data.data
		}, function(data) {
			return []
		})
	}

	return factory;
})

app.factory('utils', function($q, $timeout, $rootScope, $http) {
	var factory = {};

	factory.requestStart = requestStart;
	factory.requestEnd = requestEnd;
	factory.fillFallbackList = fillFallbackList;
	factory.replaceInvalidImages = replaceInvalidImages;

	function requestStart() {
		$rootScope.isLoading = true
	}

	function requestEnd() {
		$rootScope.isLoading = false
	}

	function replaceInvalidImages(imageHolder, imageCol) {
		promises = []

		if(Array.isArray(imageHolder)) {
			for(var i = 0; i < imageHolder.length; i++) {
				promises.push(valdiateImageUrl(imageHolder[i], imageCol))
			}
		} else {
			promises.push(valdiateImageUrl(imageHolder, imageCol))
		}


		$q.all(promises)
	}

	function valdiateImageUrl(imageHolder, imageCol)
	{
		var d = $q.defer();

		replacement = "/static/images/placeholder.png"

		$timeout(function(){
			if(!imageHolder[imageCol]) {
					imageHolder[imageCol] = replacement
					d.resolve()
			} else {
				if(imageHolder[imageCol].indexOf('s3.amazonaws.com/hairydolphins') === -1) {
					$http.get(imageHolder[imageCol])
					.error(function() {
							$http.get($rootScope.s3url + imageHolder[imageCol])
							.success(function(){
								imageHolder[imageCol] =$rootScope.s3url + imageHolder[imageCol]
								d.resolve()
							}).error(function(){
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
	function fillFallbackList(fillList, fallbackSize)
	{
		list = []

		for(i = 0; i < fallbackSize; i++)
		{
			list = list.concat({})
		}

		if(fillList.length > fallbackSize)
		{
			for(i = 0; i < fallbackSize; i++)
			{
				list[i] = fillList[i]
			}

			for(i = fallbackSize; i < fillList.length; i++)
			{
				list = list.concat(fillList[i])
			}
		}
		else
		{
			for(i = 0 ; i < fillList.length; i++)
			{
				list[i] = fillList[i]
			}
		}

		return list;

	}

	return factory
})

app.factory('socketService', function (socketFactory) {
  return socketFactory();
});

app.factory('fileManager', function($q, $timeout, utils, $http) {
	var factory = {};

	factory.uploadFile = uploadFile

	function uploadFile(file_to_upload) {
		utils.requestStart()
		
		fd = new FormData()
		fd.append("photo", file_to_upload)

		return $http({
			method: 'POST',
			url : '/api/files',
			headers: {'Content-Type': undefined },
			data: fd
		}).then(function(data, status){
			return data.data
		}, function(data) {
			return []
		})
	}

	return factory
})

app.factory('recManager', function($q, $timeout, utils, $http) {
	var factory = {};

	factory.createNewRec = createNewRec

	function createNewRec(params) {
		utils.requestStart()

		return $http({
			method: 'POST',
			url : '/api/recommendations',
			params: params
		}).then(function(data, status){
			return data.data
		})
	}

	return factory
})

app.factory('reviewManager', function($q, $timeout, utils, $http) {
	var factory = {};

	factory.createNewReview = createNewReview
	factory.createNewEntityRecommendation = createNewEntityRecommendation
	factory.createNewLocalAdvisorProfileRec = createNewLocalAdvisorProfileRec

	function createNewReview(params) {
		utils.requestStart()

		return $http({
			method: 'POST',
			url : '/api/reviews',
			params: params
		}).then(function(data, status){
			utils.replaceInvalidImages(data.data.reviewer, 'profile_photo_url')
			return data.data
		})
	}

	function createNewEntityRecommendation(params) {
		utils.requestStart()

		return $http({
			method: 'POST',
			url : '/api/entity_recommendations',
			params: params
		}).then(function(data, status){
			utils.replaceInvalidImages(data.data.entity, 'profile_photo_url')
			return data.data
		})
	}

	function createNewLocalAdvisorProfileRec(params) {
		utils.requestStart()

		return $http({
			method: 'POST',
			url : '/api/local_advisor_profile_recommendations',
			params: params
		}).then(function(data, status){
			utils.replaceInvalidImages(data.data.entity, 'profile_photo_url')
			return data.data
		})
	}

	return factory
})