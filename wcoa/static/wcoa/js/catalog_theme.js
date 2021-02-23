var customize_initial_content = function(iframe_contents) {
  // Hide Approval Status Facet
  $('span.dijitTitlePaneTextNode:contains("Approval Status")', iframe_contents).parents('div.g-filter-collapse').hide();
  $('div.g-search-pane-left', iframe_contents).css('display', 'none');
  $('div.search-box div.input-group', iframe_contents).css('display', 'none');
  $('div.search-box', iframe_contents).css('min-height', '30px');
  $('div.g-search-pane-right', iframe_contents).css('width', '100%');
}
