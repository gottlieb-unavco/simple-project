function makeButton() {
    return $('<button type="button" class="btn btn-light"><i></i></button>');
}

function getSocket(onmessage) {  
  var state = 'init';
  var localhost = "" + location.host;
  var wsURL = 'ws://' + localhost + '/ws/example/';
  var socket = null;

  /**
   * Create a new websocket
   */
  function createSocket() {
    console.log(wsURL);
    socket = new WebSocket(wsURL);
    socket.onopen = function() {
      state = 'open';
    };
    socket.onmessage = onmessage;
    socket.onerror = function() {
      console.log("Error");
      state = 'error';
    }
    socket.onclose = function() {
      console.log("Closing");
      var wasError = (state == 'error');
      state = 'closed';
      socket = null;
      if (!wasError) {
        setTimeout(createSocket, 15000);
      }
    };
    return socket;
  }

  function send(message) {
    if (!socket || socket.readyState == socket.CLOSED) {
      console.log('Reloading socket');
      createSocket();
    }
    console.log('Send message');
    socket.send(JSON.stringify(message));
  }

  createSocket();
  return {
    createSocket: createSocket,
    send: send,
  };
}

function createItem(item) {
  return $('<li>').append(
    $('<span class="value">').text('' + item.value),
    $('<span class="created_date">').text('' + item.created_date),
    $('<span class="datetime">').text('' + item.datetime),
  );
}

/**
 * Attach the socket API on top of the page elements
 */
function attachSocket($form, $latest) {
  var $status = $('<div class="ws-status" />');
  function onmessage(message) {
    var response = JSON.parse(message.data);
    console.log(response);
    $test.prop('disabled', false);
    if (response.status == 'ok') {
      if (response.result) {
        $status.text(response.result);
        $refresh.click();
      }
      if (response.items) {
        $latest.prepend(
          response.items.map(createItem)
        );
      }
    }
  }
  var ws = getSocket(onmessage);
  var messageIdx = 1;
  var $test = $('<button type="button">').text('Send a test message');
  $test.click(function() {
    $test.prop('disabled', true);
    ws.send({
      action: 'send',
      value: 'Message ' + messageIdx++,
    });
  });
  var $refresh = $('<button type="button">').text('Load recent');
  $refresh.click(function() {
    ws.send({
      action: 'list',
    });
  });

  $form.after($test, $refresh, $status);
  $form.hide();
}
