$( document ).ready(function() {
  var iframe_url = $('iframe').attr('src');
  var new_iframe_url = iframe_url + window.location.search;
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

var quarter_second_loop = function() {

  iframe_contents = $('#page_iframe').contents();
  $('.g-item-actions', iframe_contents).children('div.dropdown').each(function(){
    if (!$(this).is(':first-child')) {
      $(this).parent().prepend($(this));
    }
  });
  $('.g-item-actions', iframe_contents).children('a:contains("Download (HTTP)")').each(function(){
    $(this).html('Download');
  });
  $('.g-item-actions', iframe_contents).children('a:contains("Website")').remove();
  setTimeout(quarter_second_loop, 250);
}

var detect_iframe_load = function() {
  iframe_contents = $('#page_iframe').contents();
  if ($('body', iframe_contents).length == 0) {
    setTimeout(detect_iframe_load, 500);
  }
}

var assign_iframed_classes = function() {
  $('body', iframe_contents).addClass('iframed');
  if ($('div.g-entry-links > div', iframe_contents).length > 0){
    $('div.g-entry-links > div', iframe_contents).addClass('iframed');
  } else {
    setTimeout(assign_iframed_classes, 500);
  }
}

var on_geoportal_search_loaded = function(iframe_contents) {
  assign_iframed_classes(iframe_contents);
  handle_zero_results(iframe_contents);
  quarter_second_loop();
  // Hide Approval Status Facet
  $('span.dijitTitlePaneTextNode:contains("Approval Status")', iframe_contents).parents('div.g-filter-collapse').hide();
}

var detect_geoportal_search_load = function() {
  iframe_contents = $('#page_iframe').contents();
  if ($('.g-search-pane', iframe_contents).length > 0) {
    on_geoportal_search_loaded(iframe_contents);
  } else {
    setTimeout(detect_geoportal_search_load, 500);
  }
}

var handle_zero_results = function(iframe_contents) {
  if ($('.g-paging-count', iframe_contents).length > 0 && $('.g-paging-count', iframe_contents).html().indexOf('null') >= 0) {
    var zero_count_html = '0 items found. <a href="/geoportal/">View All Records</a>';
    $('.g-paging-count', iframe_contents).html(zero_count_html);
  }
}

$('#page_iframe').on('load', set_iframe_height);
// $('#page_iframe').on('load', detect_iframe_load);
$('#page_iframe').on('load', detect_geoportal_search_load);
