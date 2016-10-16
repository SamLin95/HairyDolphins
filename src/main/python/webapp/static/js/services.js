var app = angular.module('HairyDolphinsApp');

app.factory('AuthService',
  ['$q', '$timeout', '$http', 'utils',
  function ($q, $timeout, $http, utils, $rootScope) {

    // create user variable
    var user = null;

    // return available functions for use in controllers
    return ({
      isLoggedIn: isLoggedIn,
      login: login,
      logout: logout,
      loadCurrentUser: loadCurrentUser,
      getUser: getUser,
    });

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

}]);

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
	factory.searchRecommendations = searchRecommendations;
	factory.searchUserContacts = searchUserContacts;
	factory.searchMessageHistory = searchMessageHistory;

	function searchRecommendations(params) {
		utils.requestStart()

		return $http({
			method: 'GET',
			url : '/api/recommendations',
			params: {
				request_fields: [
					'recommendation_category',
					'recommendation_photos',
					'recommender',
					'reviews',
					'title'
				]
			}
		}).then(function(data, status){
			return data.data
		}, function(data) {
			return []
		})
	}


	function searchLocalAdvisors(params) {
		utils.requestStart()
		params.role_id = 2;

		return $http({
	    	method: 'GET',
	    	url : '/api/users', 
	    	params: params
	    }).then(function(data, status){
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

// app.factory('sharedSearch', function($rootScope) {
// 	var sharedSearch = {};
//
// 	searchHelper.sharedSearch({
// 		keyword:
// 	})
// });