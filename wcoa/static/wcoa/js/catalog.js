$( document ).ready(function() {
  var iframe_url = $('iframe').attr('src');
  var new_iframe_url = iframe_url + '#' + window.location.search;
  $('iframe').attr('src', new_iframe_url);
});
