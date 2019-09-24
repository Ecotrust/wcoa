var pkry = $('.packery-container').packery({
  itemSelector: '.home-item',
  gutter: 10,
  isOriginLeft: false,
  // initLayout: false,
});

var searchForm = document.querySelector('#search-form');
searchForm.addEventListener('submit', function(event) {
  event.preventDefault();
  var searchText = "*";
  if (document.querySelector('#search-text') && document.querySelector('#search-text').value.length > 0) {
  	searchText = document.querySelector('#search-text').value;
  }
  window.location.href = 'http://portal.westcoastoceans.org/discover/#?text='+searchText;
});

$(document).ready(function() {
  var recordCountCallback = function(numFound) {
    $('#record-count').html(numFound);
  }
  solr.getRecordCount(recordCountCallback);
});
