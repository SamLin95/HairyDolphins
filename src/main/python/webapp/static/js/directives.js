var app = angular.module('HairyDolphinsApp');

//The datepicker directive.
app.directive("datepicker", function() {
    return {
        restrict: "A",
        controller: ['$scope', '$filter', function($scope, $filter) {
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

//The directive required by file uploader
app.directive('customOnChange', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            //Allow value change event to be listened
            var onChangeHandler = scope.$eval(attrs.customOnChange);
            element.bind('change', onChangeHandler);
        }
    };
});

//The directive for chat panel to scroll the history to the bottom
app.directive('scrollBottom', function($timeout) {
    return {
        scope: {
            scrollBottom: "="
        },
        link: function(scope, element) {
            scope.$watchCollection('scrollBottom', function(newValue) {
                if (newValue) {
                    $timeout(function() {
                        $(element).scrollTop($(element)[0].scrollHeight)
                    }, 0)
                }
            });
        }
    }
})