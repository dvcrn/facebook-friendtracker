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
  static_url = 'https://freepr.s3.amazonaws.com/'

  $routeProvider
    .when('/app/', {
      templateUrl: static_url + 'static/partials/app.html',
      controller: 'AppCtrl'
    })
    .when('/sync/', {
      templateUrl: static_url + 'static/partials/status.html',
      controller: 'SyncCtrl'
    })
    .when('/auth/:redirectTo/', {
      templateUrl: static_url + 'static/partials/status.html',
      controller: 'AuthCtrl'
    })
    .when('/reset/', {
      templateUrl: static_url + 'static/partials/status.html',
      controller: 'ResetCtrl'
    })
    .otherwise({
      redirectTo: '/auth/sync/'
    })

  $sceDelegateProvider.resourceUrlWhitelist([
    'self', static_url + '**', 'https://www.facebook.com/**']);
]