var app = angular.module('thing', [
  'ui.router',
  'ngResource',
  'ngStorage',
]);

app.constant('LIB_ROOT', 'static/app/');

// Log state changes
app.run(function($rootScope) {
  $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
    console.log('$stateChangeStart: ' + fromState.name + ' -> ' + toState.name, toParams);
  });
  $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
    console.log('$stateChangeSuccess: ' + fromState.name + ' -> ' + toState.name);
  });
  $rootScope.$on('$stateChangeError', function(event, toState, toParams, fromState, fromParams, error) {
    console.log('$stateChangeError: ' + fromState.name + ' -> ' + toState.name + '(', toParams, ')\n', error);
    console.error(error.stack);
  });
});

// Handle state redirects by hooking into UI Router
app.run(function($rootScope, $state) {
  $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
    if ('redirect' in toState) {
      event.preventDefault();
      $state.go(toState.redirect, toParams);
    }
  });
});

// Configure navigation
app.config(function(
  $stateProvider,
  LIB_ROOT
) {
  'use strict';

  $stateProvider
    .state('app', {
      url: '',
      templateUrl: LIB_ROOT + 'root.tpl.html',
      redirect: 'app.table',
    })
    .state('app.root', {
      url: '/',
      onEnter: function($state) {
        $state.go('app.table');
      }
    })
    .state('app.table', {
      url: '/table',
      template: '<div ui-view></div>',
      redirect: 'app.table.list',
    })
    .state('app.table.list', {
      url: '/all',
      templateUrl: LIB_ROOT + 'TableList.tpl.html',
      controller: 'TableListCtrl',
      resolve: {
        tables: function(TableListService) {
          return TableListService.tables;
        },
      }
    })
    .state('app.table.view', {
      url: '/:name',
      templateUrl: LIB_ROOT + 'TableView.tpl.html',
      controller: 'TableCtrl',
      resolve: {
        tables: function(TableListService) {
          return TableListService.tables;
        },
        table: function($stateParams, resources) {
          return resources.table.get({ name: $stateParams.name }).$promise;
        },
      }
    })
  ;
});
