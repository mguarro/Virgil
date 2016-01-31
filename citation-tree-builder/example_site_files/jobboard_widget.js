(function () {
  "use-strict"
  var jQuery;

// sources of jQuery ordered from the most prefered to the least prefered
  var sources = [
    "https://code.jquery.com/jquery-1.11.3.min.js",
    "https://www.oxfordjournals.org/resource/js/jquery.min.js",
    "https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"
  ]

  // function to load jQuery from a given source
  //   also sets handlers for onload/onerror
  function tryLoadjQuery(uri) {
    // console.log('Trying to retrieve jQuery from: ' + uri);
    var jquery_script = document.createElement('script');
    jquery_script.setAttribute("type","text/javascript");
    jquery_script.setAttribute("src", uri);

    // when jQuery loads, rename it to avoid clashes
    if (jquery_script.readyState) {
      jquery_script.onreadystatechange = function () { // For old versions of IE
        if (this.readyState == 'complete' || this.readyState == 'loaded') {
            scriptLoadedHandler();
        }
      }
      jquery_script.onerror = scriptNotLoadedHandler;
    } else {
      // if we load from the first source -- proceede
      jquery_script.onload = scriptLoadedHandler;
      // else try anther source...
      jquery_script.onerror = scriptNotLoadedHandler;
    }


    var widget = document.querySelectorAll('.jobboard-widget')[0];
    // var widget = document.getElementsByClassName("jobboard-widget")[0];
    widget.insertBefore(jquery_script, widget.firstChild);
  }

  /******** Called once jQuery has loaded ******/

  function scriptLoadedHandler() {
    // Restore $ and window.jQuery to their previous values and store the
    // new jQuery in our local jQuery variable
    jQuery = window.jQuery.noConflict(true);
    // Call our main function
    // console.log('using jQuery version: ' + jQuery.fn.jquery);
    main();
  }

  function scriptNotLoadedHandler() {
    if (sources.length > 0) {
      // remove the first element
      var uri = sources.shift()
      tryLoadjQuery(uri);
    } else {
      console.log('jQuery > 1.5.0 not loaded...');
    }
  }


  // The jQuery version on the window is too old or undefined; load new one
  if (!window.jQuery || (window.jQuery.fn.jquery < "1.5.1")) {
    scriptNotLoadedHandler();
  } else {
    // The jQuery version on the window is suitable - use it
    jQuery = window.jQuery;
    main();
  }


  /******** Our main function ********/
  function main() {
    if(!jQuery){ return; }

    var timer;

    jQuery(document).ready(function($) {

      // auto-scrolling
      function setup_scrolling(widget) {
        if ($(widget).hasClass('flag-setup-done')) {
          return;
        }
        // mark that widget is processed
        $(widget).addClass('flag-setup-done');

        // Scrolling loop functions
        function rotate_jobs(widget) {
          var job_list = $(widget).find(".jt_job_list");
          var jobs = job_list.find(".jt_job");
          var first_job = jobs.first();
          job_list.append(first_job.clone());
          first_job.animate({"opacity": 0}, 400, function() {
              // console.log('sliding up job ' + first_job.text());
              first_job.slideUp({
                "duration": 400,
                "complete": function() {
                  first_job.remove();
                  clearTimeout(timer);
                  timer = setTimeout(function() {rotate_jobs(widget);}, 4000);
                }
              });
          });
        }

        function start_rotate(widget) {
          clearTimeout(timer);
          timer = setTimeout(function() {rotate_jobs(widget);}, 4000);
          $(widget).find('.jt_job_list').css('overflow', 'hidden');
        }

        function stop_rotate(widget) {
          clearTimeout(timer);
          $(widget).find('.jt_job_list').css('overflow', 'auto');
        }

        // pause when mouse is over
        widget.mouseenter(function() {
          stop_rotate(this);
        });

        // continue when mouse leaves
        widget.mouseleave(function() {
          start_rotate(this);
        });
        // return the fun
        return start_rotate;
      }

      // Data loading
      // http://stackoverflow.com/a/11267937
      function crossDomainAjax (url, successCallback, failCallback) {

        // IE8 & 9 only Cross domain JSON GET request
        if ('XDomainRequest' in window && window.XDomainRequest !== null) {

          var xdr = new XDomainRequest(); // Use Microsoft XDR
          xdr.open('get', url);
          xdr.onload = function () {
            successCallback(xdr.responseText); // internal function
          };
          xdr.onerror = failCallback;
          xdr.send();
        }

        // IE7 and lower can't do cross domain
        else if (navigator.userAgent.indexOf('MSIE') != -1 &&
                 parseInt(navigator.userAgent.match(/MSIE ([\d.]+)/)[1], 10) < 8) {
         return false;
        }

        // Do normal jQuery AJAX for everything else
        else {
          $.ajax({
            url: url,
            cache: false,
            dataType: 'html',
            type: 'GET',
            async: true, // must be set to false
            success: function (data, success, request) {
                successCallback(data);
            },
            error: function (request, status, error) {
              failCallback(request, status, error);
            }
          });
        }
      }

      // get the placeholder for the widget
      $('.jobboard-widget').each(function() {
        var widget = $(this);
        var code = widget.find('.code').text();
        var branded = widget.find('.branded').text();
        branded = (branded === "true")
        var header = widget.find('.widgetHead');
        // widget body
        var body = $('<div class="widgetBody"></div>');
        // footer shows a link to all jobs
        var footer = widget.find('.widgetFoot');
        if (!branded) {
          footer.html('');
        }
        // define success and failure functions
        call_successful = function(data) {
          // console.log('call successful');
          var list = $('<div class="jt_job_list">');
          $(data).find('.jt_job').each(function () {
            var row = $('<div class="jt_job">');
            row.append($(this).find('.jt_job_position'));
            row.append($(this).find('.jt_job_location'));
            list.append(row);
          });
          body.append(list);
          //
          if ($(body).find('.jt_job').size() > 0) {
            if (branded) {
              body.append($(data).find(".jt_alljobs"));
              body.find(".jt_alljobs a").addClass("oupViewAll");
            } else {
              footer.html($(data).find(".jt_alljobs"));
            }
            var start_fn = setup_scrolling(widget);
            if (start_fn) {
              start_fn(widget);
            }
          } else {
            body.append('<p>No relevant jobs found.</p>');
            body.append($(data).find(".jt_alljobs"));
            body.addClass("noJobs");
          }
          var link = $(data).find(".jt_alljobs a").attr('href');
          var wrapper = $('<a></a>');
          wrapper.attr('href', link);
          wrapper.addClass('taglineLink');
          header.wrapInner(wrapper);
          // put it all together
          widget.html(header);
          widget.append(body);
          widget.append(footer);
          // set up fixed height to avoid resizing widget when jode added
          // during job rotation
          list.css('height', list.height());
        }

        call_unsuccessful = function(request, status, error) {
          // console.log('call unsuccessful');
          body.html('<p>No relevant jobs found.</p>');
          body.addClass("noJobs");
          // put it all together
          widget.html(header);
          widget.append(body);
          widget.append(footer);
        }

        // get data
        var jobs_url = '//www.oxfordjournals.org/distrib/jobs/html.cfm?code=' + code
        crossDomainAjax(jobs_url, call_successful, call_unsuccessful);

      }); // for each widget

    });
  }
})();
