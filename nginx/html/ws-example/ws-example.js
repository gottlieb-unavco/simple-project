/**
 * Provide a simple interface on a reconnecting socket.
 * 
 * The caller provides an onmessage to be called on any
 * incoming traffic.
 * 
 * Return an object with one function: 
 * socket.send({
 *  ...
 * })
 * returns a Promise to send the message when the socket
 * is available
 * 
 * @param {function} onmessage 
 * @returns 
 */
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
    socket.onopen = function () {
      socketPromise.resolve(socket);
      retries = 0;
    };
    socket.onmessage = onmessage;
    socket.onerror = function () {
      console.log("Error");
      if (socketPromise) {
        socketPromise.reject();
      }
    }
    socket.onclose = function () {
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
      function (socket) {
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
   * Promise to send a message to the socket
   * @param {object} message JSON data for the message
   * @returns Promise that resolves when the message is sent
   */
  function send(message) {
    return awaitSocket().then(function (socket) {
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
    "created: " + item.timestamp + " / " +
    "archived: " + item.created_date
  ));
  return $('<li class="card latest popup-help">').append(
    $('<div class="card-header">').append(
      $('<span class="value">').text('' + item.value),
      ' - ',
      $('<span class="timestamp">').text('' + item.timestamp),
      ' - ',
      $delay,
      $('<div class="popup card">').append(
        $('<ul class="list-compact">').append(
          [
            ['Data Id', '' + item.data_id],
            ['Started', '' + item.timestamp],
            ['Received', '' + item.created_date],
            ['Provenance', $('<ul>').append(
              item.data_provenance.map(function(prov) {
                return $('<li>').append('' + prov);
              })
            )],
          ].map(function(row) {
            return $('<li>').append(
              $('<b>').append(row[0]),
              ': ',
              row[1]
            );
          })
        )
      )
    )
  );
}

// Copied from https://davidwalsh.name/javascript-debounce-function
// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
function debounce(func, wait, immediate) {
  let timeout;
  function fn(...args) {
    const context = this;
    function later() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    }
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) { func.apply(context, args); }
  }
  return fn;
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
    " texts " + getRandomItem(people) +
    " from " + getRandomItem(locations)
  );
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
  function sendToSocket(message) {
    ws.send(message);
    addStatusLine('out', message);
  }

  function sendOneMessage() {
    sendToSocket({
      action: 'send',
      value: makeMessageText(),
    });
  }

  var sendTimer = 0;
  function cancelMessages() {
    if (sendTimer) {
      clearInterval(sendTimer);
      sendTimer = 0;
    }
  }
  function sendMessages(count, rate) {
    cancelMessages();
    var remaining = count;
    var wait = 1000 / rate;
    sendTimer = setInterval(
      function () {
        sendOneMessage();
        remaining--;
        if (remaining <= 0) {
          cancelMessages();
        }
      },
      wait
    );
  }

  // Group for the main widget
  var $sendGroup = $('<div class="input-group">');
  var $send = $('<button class="btn btn-outline-primary" type="button">').text('Send');
  var $count = $('<input type="number" class="form-control" value="10">');
  var $rate = $('<input type="number" class="form-control" value="10">');
  $sendGroup.append(
    $send,
    $count,
    '<span class="input-group-text">@</span>',
    $rate,
    '<span class="input-group-text">/s</span>',
  );
  var $stop = $('<button type="button" class="btn btn-outline-danger">').text('Stop');

  $send.click(function () {
    sendMessages($count.val(), $rate.val());
  });
  $stop.click(cancelMessages);

  // Refresh function is debounced
  var debouncedRefresh = debounce(
    function () {
      sendToSocket({
        action: 'list',
      });
    },
    1000
  );

  var $refresh = $('<button type="button" class="btn btn-outline-secondary">').text('Refresh list');
  $refresh.click(debouncedRefresh);

  $form.append(
    $sendGroup,
    $refresh,
  );

  sendToSocket({
    action: 'list',
  });
}
