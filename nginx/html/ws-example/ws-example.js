function getSocket(onmessage) {  
  var state = 'init';
  var localhost = "" + location.host;
  var wsURL = 'ws://' + localhost + '/example/ws/';
  // Promise that returns a socketPromise socket
  var socketPromise = null;

  // Base retry timeout
  var retryBaseTimeout = 4000;
  // How much to back off each repeated retry
  var retryBackoff = 2;
  // How many retries we've done
  var retries = 0;

  /**
   * Create a promise of a new socket
   * @returns Promise returning the socket when it becomes available
   */
  function createSocketPromise() {
    console.log(wsURL);
    socketPromise = $.Deferred();
    var socket = new WebSocket(wsURL);
    socket.onopen = function() {
      socketPromise.resolve(socket);
      retries = 0;
    };
    socket.onmessage = onmessage;
    socket.onerror = function() {
      console.log("Error");
      if (socketPromise) {
        socketPromise.reject();
      }
    }
    socket.onclose = function() {
      console.log("Closing");
      var wasError = (state == 'error');      
      if (socketPromise) {
        socketPromise.reject();
        socketPromise = null;
      }
    };
    return socketPromise;
  }

  /**
   * Return a promise of a working socket. Mainly reconnects if a stale
   * socket is found.
   * @returns Promise returning the socket when it becomes available
   */
  function awaitSocket() {
    // No working promise, create a new one
    if (!socketPromise) {
      return createSocketPromise();
    }
    return socketPromise.then(
      // Got a socket, but it may be stale
      function(socket) {
        if (!socket || socket.socketPromiseState == socket.CLOSED) {
          console.log('Reloading socket');
          return createSocket();
        }
        return socket;         
      },
      // Error = socket is closed, try recreating
      createSocketPromise,
    )
  }

  /**
   * Send a message to the socket
   * @param {object} message JSON data for the message
   */
  function send(message) {
    awaitSocket().then(function(socket) {
      socket.send(JSON.stringify(message));
    });
  }

  // Start up a connection on initialization
  createSocketPromise();

  // Just return the send API
  return {
    send: send,
  };
}

/**
 * Return the difference between 2 times (Dates or Strings)
 * @param {Date, String} t1 
 * @param {Date, String} t2 
 * @returns difference in ms
 */
function timeDiff(t1, t2) {
  return (new Date(t2) - new Date(t1));
}

/**
 * Create a list item for the "latest" list
 * @param {object} item an item record returned from the 'list' API
 * @returns jQuery
 */
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


var people = [
  'Homer', 'Marge', 'Bart', 'Lisa', 'Maggie', 'Moe', 'Barney', 
  'Carl', 'Lenny', 'Mr. Burns', 'Bumblebee Man', 'McBain',
];
var locations = [
  '642 Evergreen Terrace', "Moe's Bar", 'Springfield Elementary',
  'Springfield Nuclear Power Plant', 'Capital City',
];
function getRandomItem(list) {
  return list[Math.floor(Math.random() * list.length)];
}
function makeMessageText() {
  return (
    "" + getRandomItem(people) +
    " calling " + getRandomItem(people) +
    " from " + getRandomItem(locations)
  );
}

/**
 * UUID4 quick and dirty version
 * @see https://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid/2117523#2117523
 * @returns String
 */
function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function makeDataId() {
  return "example:ws/" + uuidv4();
}

/**
 * Attach the socket API on top of the page elements
 * 
 * @param {jQuery} $form container for the form (buttons)
 * @param {jQuery} $status container for the websocket status
 * @param {jQuery} $archive container for the archive data
 */
 function attachSocket($form, $status, $archive) {
  var $socketStatus = $('<div class="socket-status" />');
  $status.append($socketStatus);

  /**
   * Log a line of status from the websocket
   * @param {String} desc 
   * @param {object} data 
   */
  function addStatusLine(desc, data) {
    var $statusLine = (
      $('<div class="status-line">')
      .addClass(desc)
      .text(JSON.stringify(data))
    );
    $('.status-line', $socketStatus).slice(0, -9).remove();
    $socketStatus.append($statusLine);
    // Scroll to the new line
    $statusLine.get(0).scrollIntoView(false);
  }

  /**
   * Handle a message from the socket
   * @param {object} message 
   */
  function onmessage(message) {
    var response = JSON.parse(message.data);
    console.log(response);
    addStatusLine('in', response);
    if (response.status == 'ok') {
      // Text result
      if (response.result) {
        // Trigger a list refresh shortly after we run a command
        setTimeout(() => $refresh.click(), 500);
      }
      // Archive items go in the list
      if (response.items) {
        $archive.empty().append(
          response.items.map(createItem)
        );
      }
    }
  }
  var ws = getSocket(onmessage);

  /**
   * Send a message on the socket
   * @param {object} message 
   */
  function sendMessage(message) {
    ws.send(message);
    addStatusLine('out', message);
  }

  var $test = $('<button type="button">').text('Send a test message');
  $test.click(function() {
    sendMessage({
      action: 'send',
      value: makeDataId(),
    });
  });
  var $refresh = $('<button type="button">').text('Refresh list');
  $refresh.click(function() {
    sendMessage({
      action: 'list',
    });
  });

  $form.append($test, $refresh);

  sendMessage({
    action: 'list',
  });
}
