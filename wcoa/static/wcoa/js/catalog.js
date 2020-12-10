$( document ).ready(function() {
  var iframe_url = $('iframe').attr('src');
  if (iframe_url.indexOf('?') >= 0 && iframe_url.toLowerCase().indexOf('esdsl=') >= 0 && window.location.search.toLowerCase().indexOf('esdsl=') >= 0) {
    split_url = iframe_url.split('?');
    url_query = split_url.pop(split_url.length-1);
    url_root = split_url.join('?'); // does it make sense that there'd be more than 1 '?'? No, but this should work, too.
    split_search = window.location.search.split('?');
    var new_iframe_url = merge_esdsl_queries(url_root, url_query, split_search[split_search.length - 1])
  } else {
    var new_iframe_url = iframe_url + window.location.search;
  }
  $('iframe').attr('src', new_iframe_url);
});

var merge_esdsl_queries = function(url, query1, query2) {
  var query1_list = query1.split('&');
  var esdsl1 = '';
  for (var i = 0; i < query1_list.length; i++) {
    if (query1_list[i].toLowerCase().indexOf('esdsl=') >= 0){
      var esdsl1_raw = query1_list.pop(i);
      esdsl1 = esdsl1_raw.split('esdsl=')[1];
      break;
    }
  }
  var query2_list = query2.split('&');
  var esdsl2 = '';
  for (var i = 0; i < query2_list.length; i++) {
    if (query2_list[i].toLowerCase().indexOf('esdsl=') >= 0){
      var esdsl2_raw = query2_list.pop(i);
      esdsl2 = esdsl2_raw.split('esdsl=')[1];
      break;
    }
  }
  if (esdsl1.length > 0 && esdsl2.length > 0) {
    var query_json = {'query':{"bool":{"must":[]}}};
    var query1_json = JSON.parse(decodeURIComponent(esdsl1));
    var query2_json = JSON.parse(decodeURIComponent(esdsl2));
    var query_json_list = [query1_json, query2_json];
    for (var query_idx = 0; query_idx < query_json_list.length; query_idx++) {
      query = query_json_list[query_idx];
      if (query.query.hasOwnProperty('bool') && query.query.bool.hasOwnProperty('must')) {
        for (var filter_idx = 0; filter_idx < query.query.bool.must.length; filter_idx++) {
          query_json.query.bool.must.push(query.query.bool.must[filter_idx]);
        }
      } else {
        query_json.query.bool.must.push(query.query);
      }
    }
    var esdsl_merge = JSON.stringify(query_json);
  } else {
    var esdsl_merge = esdsl1 + esdsl2;
  }
  var query_string = [query1_list.join('&'), query2_list.join('&'), 'esdsl='+encodeURIComponent(esdsl_merge)].join('&');
  return url + '?' + query_string;
}

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

  $('div.g-item-title a:contains("/")', iframe_contents).each(function(){
    label = $(this).html();
    path = label.split('/');
    if (path[path.length-1].toLowerCase() == 'layers' && path.length > 1){
      var out = path[path.length-2] + " (" + path[path.length - 1] + ")";
    } else {
      var out = path[path.length-1];
    }
    out = out.split('_').join(' ');
    $(this).html(out);
  })

  // Fix WEB Link:
  var web_link = $('a:contains("WEB")',iframe_contents);
  web_link.attr("href", function() {
    if ($(this).attr("href").indexOf(window.location.pathname) < 0) {
      return window.location.origin + window.location.pathname + $(this).attr("href");
    }
    return $(this).attr("href");
  });
}

var detect_iframe_load = function() {
  iframe_contents = $('#page_iframe').contents();
  if ($('body', iframe_contents).length == 0) {
    setTimeout(detect_iframe_load, 500);
  }
}

var assign_iframed_classes = function(iframe_contents) {
  $('body', iframe_contents).addClass('iframed');
  if ($('div.g-entry-links > div', iframe_contents).length > 0){
    $('div.g-entry-links > div', iframe_contents).addClass('iframed');
  } else {
    setTimeout(assign_iframed_classes, 500);
  }
}

var customize_initial_content = function(iframe_contents) {
  // Hide Approval Status Facet
  $('span.dijitTitlePaneTextNode:contains("Approval Status")', iframe_contents).parents('div.g-filter-collapse').hide();
}

var on_geoportal_search_loaded = function(iframe_contents) {
  assign_iframed_classes(iframe_contents);
  customize_initial_content(iframe_contents);
  handle_zero_results(iframe_contents);
  quarter_second_loop();
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
