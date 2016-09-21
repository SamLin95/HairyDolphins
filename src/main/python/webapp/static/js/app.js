'use strict';

angular.module('HairyDolphinsApp', [])

.controller('mainController', function($scope) {

  $scope.message = "test";
  $scope.advisors = [
    {
      "name" = "Dun",
      "startDate" = "09/09/2016",
      "location" = "Italy"
    },
    {
      "name" = "Kevin",
      "startDate" = "05/04/2016",
      "location" = "Spain"

    },
    {
      "name" = "Sam",
      "startDate" = "02/06/2016",
      "location" = "Germany"
    }
  ];
});
