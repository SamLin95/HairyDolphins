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

app.factory('searchHelper', function($q, $http, utils) {
	var factory = {};

	factory.searchLocalAdvisors = searchLocalAdvisors;

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

	return factory;
})

app.factory('utils', function($q, $timeout, $rootScope, $http) {
	var factory = {};

	factory.requestStart = requestStart;
	factory.requestEnd = requestEnd;
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

	return factory

})