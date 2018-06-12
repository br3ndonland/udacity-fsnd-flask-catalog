function signInCallback (authResult) {
  if (authResult['code']) {
    // Hide the sign-in button now that the user is authorized
    $('#signinButton').attr('style', 'display: none')
    // Send the one-time-use code to the server, if the server responds, write a 'login successful' message to the web page and then redirect back to the main restaurants page
    $.ajax({
      type: 'POST',
      url: '/gconnect?state={{ STATE }}',
      processData: false,
      data: authResult['code'],
      contentType: 'application/octet-stream; charset=utf-8',
      success: function (result) {
        // Handle or verify the server response if necessary.
        if (result) {
          $('#result').html('<h2 class="font-weight-light">Login Successful!</h2></br>' + result + '</br>Redirecting...')
          setTimeout(function () {
            window.location.href = "{{ url_for('home') }}"
          }, 1000)
        } else if (authResult['error']) {
          console.log('There was an error: ' + authResult['error'])
        } else {
          $('#result').html('Failed to make a server-side call. Check your configuration and console.')
        }
      }
    })
  }
}
