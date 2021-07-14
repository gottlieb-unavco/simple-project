
function getSocket(onmessage) {  
  var state = 'init';
  var localhost = "" + location.host;
  var wsURL = 'ws://' + localhost + '/example/ws/';
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

function timeDiff(t1, t2) {
  return (new Date(t2) - new Date(t1));
}

function createItem(item) {
  var delay = timeDiff(item.timestamp, item.created_date);
  var $delay = $('<span class="delay">').text("" + delay + "ms");
  $delay.prop('title', (
    "transmitted: " + item.timestamp + " " +
    "received: " + item.created_date
  ));
  return $('<li>').append(
    $('<span class="value">').text('' + item.value),
    $('<span class="timestamp">').text('' + item.timestamp),
    $delay,
  );
}
/**
 * Attach the socket API on top of the page elements
 */
 function attachSocket($form, $status, $latest) {
  var $connStatus = $('<div class="conn-status" />');
  $status.append($connStatus);
  var $responseStatus = $('<div class="resp-status" />');
  $status.append($responseStatus);

  function addStatusLine(desc, data) {
    var $statusLine = (
      $('<div class="status-line">')
      .addClass(desc)
      .text(JSON.stringify(data))
    );
    $('.status-line', $responseStatus).slice(0, -9).remove();
    $responseStatus.append($statusLine);
    // Scroll to the new line
    $statusLine.get(0).scrollIntoView(false);
  }

  function onmessage(message) {
    var response = JSON.parse(message.data);
    console.log(response);
    addStatusLine('in', response);
    if (response.status == 'ok') {
      // Text result
      if (response.result) {
        // Refresh the list
        setTimeout(() => $refresh.click(), 500);
      }
      // If row items returned, show them in the list
      if (response.items) {
        $latest.empty().append(
          response.items.map(createItem)
        );
      }
    }
  }
  var ws = getSocket(onmessage);
  var messageIdx = 1;

  function sendMessage(message) {
    ws.send(message);
    addStatusLine('out', message);
  }

  var $test = $('<button type="button">').text('Send a test message');
  $test.click(function() {
    var value = 'Message ' + messageIdx++;
    sendMessage({
      action: 'send',
      value: value,
    });
  });
  var $refresh = $('<button type="button">').text('Update latest');
  $refresh.click(function() {
    sendMessage({
      action: 'list',
    });
  });

  $form.after($test, $refresh, $status);
}
