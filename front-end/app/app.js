'use strict';

angular.module('HairyDolphinsApp', [])

.controller('mainController', function() {
  var vm = this;
  vm.message = "hey"
  vm.computers = [
    {
      name: 'Mac',
      color: 'Silver',
      nerd: 7
    },
    {
      name: 'Dell',
      color: 'Black',
      nerd: 6
    },
    {
      name: 'Yoga',
      color: 'Pink',
      nerd: 1
    }
  ];
})
