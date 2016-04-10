var app = angular.module('thing', [
  'ui.router',
  'ngResource',
]);

app.constant('LIB_ROOT', 'static/app/');

app.run(function($rootScope) {
  console.log('configuring root scope');
  $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
    console.log('$stateChangeStart: ' + fromState.name + ' -> ' + toState.name, toParams);
  });
  $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
    console.log('$stateChangeSuccess: ' + fromState.name + ' -> ' + toState.name);
  });
  $rootScope.$on('$stateChangeError', function(event, toState, toParams, fromState, fromParams, error) {
    console.log('$stateChangeError: ' + fromState.name + ' -> ' + toState.name, error);
    console.error(error.stack);
  });
});

app.config(function($stateProvider, LIB_ROOT) {
  'use strict';

  $stateProvider
    .state('null', {
      url: '',
      onEnter: function($state) {
        $state.go('root');
      }
    })
    .state('root', {
      url: '/',
      templateUrl: LIB_ROOT + 'Main.tpl.html',
    });
   //$stateProvider .state('widgets', {
   //   //url: '/widgets',
   // });
   $stateProvider .state('widgetsList', {
      url: '/widgets/all',
      templateUrl: LIB_ROOT + 'WidgetList.tpl.html',
      controller: 'WidgetListCtrl',
      resolve: {
        widgets: function(resources) {
          return resources.widgets.query().$promise;
        },
      }
    });
  $stateProvider  .state('widgetsEdit', {
      url: '/widgets/:id',
      templateUrl: LIB_ROOT + 'Widget.tpl.html',
      controller: 'WidgetCtrl',
      resolve: {
        widget: function($stateParams, resources) {
          if ('id' in $stateParams && $stateParams.id !== '') {
            return resources.widgets.get({ id: $stateParams.id }).$promise;
          } else {
            return {
              name: '',
              data: ''
            }
          }
        },
      }
    })
});
