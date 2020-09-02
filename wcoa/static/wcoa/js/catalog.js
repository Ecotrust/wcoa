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
$('#page_iframe').on('load', set_iframe_height);
