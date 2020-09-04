$( document ).ready(function() {
  var iframe_url = $('iframe').attr('src');
  var new_iframe_url = iframe_url + '#' + window.location.search;
  $('iframe').attr('src', new_iframe_url);
});

var set_iframe_height = function() {
  var iframe = $('#page_iframe');
  var g_app = $('.g-app', iframe.contents());
  if ( g_app.length) {
    var search_row = $('.g-search-content-row', iframe.contents());
    if (search_row.length && search_row[0].scrollHeight < g_app[0].scrollHeight - 250) {
      iframe.height(search_row[0].scrollHeight + 250);
    }

    if (  iframe.height() < g_app[0].scrollHeight - 1 || iframe.height() > g_app[0].scrollHeight + 20) {
      var content_height = g_app[0].scrollHeight + 20;
      iframe.height(content_height);
    } else if ( iframe.width() < g_app[0].scrollWidth - 1 || iframe.width() > g_app[0].scrollWidth + 20){
      var content_width = g_app[0].scrollWidth + 20;
      iframe.width(content_width);
    }

  }
  setTimeout(set_iframe_height, 200);
}

var on_iframe_loaded = function(iframe_contents) {

}

var detect_iframe_load = function() {
  iframe_contents = $('#page_iframe').contents();
  if ($('body', iframe_contents).length > 0) {
    console.log('Iframe loaded.');
    on_iframe_loaded(iframe_contents);
  } else {
    setTimeout(detect_iframe_load, 500);
  }
}

var on_geoportal_search_loaded = function(iframe_contents) {
  $('div.g-entry-links > div > a', iframe_contents).addClass('iframed');
}

var detect_geoportal_search_load = function() {
  iframe_contents = $('#page_iframe').contents();
  if ($('.g-search-pane', iframe_contents).length > 0) {
    console.log('GeoPortal Search loaded.');
    on_geoportal_search_loaded(iframe_contents);
  } else {
    setTimeout(detect_geoportal_search_load, 500);
  }
}

$('#page_iframe').on('load', set_iframe_height);
// $('#page_iframe').on('load', detect_iframe_load);
$('#page_iframe').on('load', detect_geoportal_search_load);
