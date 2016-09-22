var app = angular.module('HairyDolphinsApp');

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