freeperControllers = angular.module 'freeperControllers', []

freeperControllers.controller 'AppCtrl', ['$scope', '$http', '$window', '$location', ($scope, $http, $window, $location) ->

  # If we don't have app_data yet, it means the app never loaded data from the backend.
  # Redirect to /sync to get data, which will then redirect to /auth if we don't have a facebook connection
  if not $scope.app_data?
    $location.path('/sync')
    return

  # Sort the array since python dictionaries are unsorted and generate history object
  history = []
  history_dates = Object.keys($scope.app_data.history)
  history_dates.sort()

  for history_timestamp in history_dates
    history.push [history_timestamp * 1000, $scope.app_data.history[history_timestamp]]

  # Convert object into lists since angularjs is bitchy when it comes to objects in templates
  new_friends = []
  lost_friends = []

  $.map $scope.app_data.new_friends, (val, index) =>
    new_friends.push([index, val])

  $.map $scope.app_data.lost_friends, (val, index) =>
    lost_friends.push([index, val])

  $scope.lost_friends = lost_friends
  $scope.new_friends = new_friends

  $scope.chartConfig = {
    options: {
      chart: {
        type: 'spline',
        backgroundColor: null,
      },
      credits: {
        enabled: false
      },
      legend: {
        enabled: false
      },
      yAxis: {
        title: {
            text: 'Friendcount'
        }
      },
    },

    series: [{
      name: 'Friends',
      data: history
    }],
    title: {
        text: 'Friends over time'
    },

    loading: false
    xAxis: {
      type: "datetime"
    }
  }
]

freeperControllers.controller 'AuthCtrl', ['$scope', '$routeParams', '$http', '$location', '$window', 'Facebook', \
                            'AccessToken', ($scope, $routeParams, $http, $location, $window, Facebook, AccessToken) ->
  $scope.status = 'Waiting for Authorization...'

  Facebook.FB (FB) ->
    FB.getLoginStatus (response) ->
      auth_dialog_url = 'https://www.facebook.com/dialog/oauth?client_id=371545839655510&redirect_uri=http://apps.facebook.com/freeper/&scope=manage_notifications'
      switch response.status
        # 'unknown' means the user did not give permissions to use the app or is not logged in.
        # redirecting to facebooks oauth dialog to force him to log in
        when 'not_authorized', 'unknown'
          top.location.href = auth_dialog_url
        when 'connected'
          FB.api '/me/permissions', (response) ->
            if 'manage_notifications' not of response.data[0]
              top.location.href = auth_dialog_url

          # to make sure we don't use a access token that is already expired, we generate a date object for the expiration time
          token_expires = new Date()
          token_expires.setSeconds token_expires.getSeconds() + response.authResponse.expiresIn

          AccessToken.set(response.authResponse.accessToken, token_expires)
          if not $scope.$$phase
            $scope.$apply ->
              $location.path '/' + $routeParams.redirectTo
          else
            $location.path '/' + $routeParams.redirectTo
]

freeperControllers.controller 'SyncCtrl', ['$scope', '$rootScope', '$location', '$http', '$window', 'AccessToken', \
        ($scope, $rootScope, $location, $http, $window, AccessToken) ->
  $scope.status = 'Syncing...'

  token = AccessToken.get (token) ->
    $http.post('api/friendlist/sync/', {'access_token': token})
    .success((response, status) ->
      if status == 200
        $rootScope.app_data = response
        $location.path '/app'
    )
]

freeperControllers.controller 'ResetCtrl', ['$scope', '$rootScope', '$http', '$location', 'AccessToken', \
      ($scope, $rootScope, $http, $location, AccessToken) ->
  $scope.status = 'Resetting changes...'

  token = AccessToken.get (token) ->
    $http.post('api/friendlist/reset/', {'access_token': token})
    .success((response, status) ->
      if status == 200
        $rootScope.app_data.lost_friends = {}
        $rootScope.app_data.new_friends = {}

        $location.path '/app'
    )
]