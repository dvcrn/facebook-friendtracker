

class Freeper
  constructor: ->
  doSomething: () ->
    FB.getLoginStatus((response) ->
      if response.status != 'connected'
        console.info('you are not authenticated')
        return

      console.info(response);
      FB.api('/me/friends', (data) ->
        console.info(data.data)
      );

      $.post '/api/friendlist/get/',
        access_token: response.authResponse.accessToken
        (data) ->
          console.info(data);
    );
    """
    FB.login((auth_response) ->
      if auth_response.authResponse
        FB.api('/me/friends', (data) ->
          console.info(data.data)
          #$.post '/api/friendlist/save/',
            #data: JSON.stringify(data.data)
        );
      else
        console.info("You didn't authenticate")
    );
    """

window.Freeper = new Freeper()
window.fbAsyncInit = ->
  FB.init 
    appId: 371545839655510
    status: true
    cookie: true
    xfbml: true
    oauth: true

  window.Freeper.doSomething()