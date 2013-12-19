$(document).foundation()
app = angular.module 'freeperApp', ['ngRoute', 'highcharts-ng', 'freeperControllers', 'facebook-ng']

app.run ['$rootScope', '$window', 'Facebook', ($rootScope, $window, Facebook2) ->
  $rootScope.$ = $;
]

app.factory 'AccessToken', ['$location', ($location) ->
  token = null
  token_expires = new Date()

  return {
    get: (callback) =>
      if @token? and @token_expires > new Date()
        callback @token
      else
        $location.path('/auth')

    set: (token, expires) =>
      @token = token
      @token_expires = expires
  }
]

app.config ['$routeProvider', '$sceDelegateProvider', ($routeProvider, $sceDelegateProvider) ->
  $routeProvider
    .when('/app/', {
      templateUrl: 'static/partials/app.html',
      controller: 'AppCtrl'
    })
    .when('/sync/', {
      templateUrl: 'static/partials/status.html',
      controller: 'SyncCtrl'
    })
    .when('/auth/:redirectTo/', {
      templateUrl: 'static/partials/status.html',
      controller: 'AuthCtrl'
    })
    .when('/reset/', {
      templateUrl: 'static/partials/status.html',
      controller: 'ResetCtrl'
    })
    .otherwise({
      redirectTo: '/auth/sync/'
    })

  $sceDelegateProvider.resourceUrlWhitelist(['self', 'https://freepr.s3.amazonaws.com/*']);
]