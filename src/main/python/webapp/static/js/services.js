var app = angular.module('HairyDolphinsApp');

app.factory('AuthService',
  ['$q', '$timeout', '$http',
  function ($q, $timeout, $http) {

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
	    var deferred = $q.defer();

	    // send a post request to the server
	    $http({
	    	method: 'POST',
	    	url : '/auth/signin', 
	    	params: {username: username, password: password}
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
	    })
	    // handle error
	    .error(function (data) {
	      user = null;
	      deferred.reject();
	    });

	  // return promise object
	  return deferred.promise;

    }

    function logout() {
    	  // create a new instance of deferred
	  var deferred = $q.defer();

	  // send a get request to the server
	  $http.get('/auth/logout')
	    // handle success
	    .success(function (data) {
	      user = null;
	      deferred.resolve();
	    })
	    // handle error
	    .error(function (data) {
	      user = null;
	      deferred.reject();
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