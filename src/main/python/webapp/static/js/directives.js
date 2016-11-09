var app = angular.module('HairyDolphinsApp');

app.directive("datepicker", function(){
  return {
    restrict: "A",
    controller: ['$scope', '$filter', function ($scope, $filter) {
        $scope.openDatePicker = function() {
            $scope.popup.opened = true;
        };

        $scope.popup = {
            opened: false
        };

        $scope.format = 'yyyy-MM-dd';
    }],
    templateUrl: "/static/directives/datepicker.html",
  }
});

app.directive('customOnChange', function() {
  return {
    restrict: 'A',
    link: function (scope, element, attrs) {
      var onChangeHandler = scope.$eval(attrs.customOnChange);
      element.bind('change', onChangeHandler);
    }
  };
});

app.directive('scrollBottom', function ($timeout) {
  return {
    scope: {
      scrollBottom: "="
    },
    link: function (scope, element) {
      scope.$watchCollection('scrollBottom', function (newValue) {
        if (newValue)
        {
          $timeout(function(){
            $(element).scrollTop($(element)[0].scrollHeight)
          }, 0)
        }
      });
    }
  }
})
