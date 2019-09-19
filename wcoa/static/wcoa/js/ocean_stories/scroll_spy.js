// var _ = require('lodash');

/**
 * Binds a scroll listener to window.
 * Calls callback with selector index whenever scroll position
 * transitions between sections.
 *
 * @param {array} selector jQuery selector defining page sections
 * @return {Object} with off() method.
 */
// module.exports = function(containerSelector, sectionSelector, callback) {
scrollSpy = function(containerSelector, sectionSelector, callback) {
  var container = $(containerSelector);
  // var container = '.content';
  var sections = container.find(sectionSelector);
  // var sections = $(container).find("a.anchor[id^='section-']");
  var currentIndex;
  var offset = 0;

  function handleScroll() {
    // Get container scroll position
    var scrollTop = $(this).scrollTop();

    var sectionIndex = -1;
    for (var i = sections.length-1; i >= 0; i--) {
      if (scrollTop >= $(sections[i]).offset().top + offset){
        sectionIndex = i;
        break;
      }
    }

    // var sectionIndex = _.findLastIndex(sections, function(s){
    //   return scrollTop >= $(s).offset().top + offset;
    // })

    if (sectionIndex < 0) {
      sectionIndex = 0;
    }
    if (sectionIndex !== currentIndex) {
      $(sections[currentIndex]).removeClass('active');
      $(sections[sectionIndex]).addClass('active');
      currentIndex = sectionIndex;
      callback(currentIndex);
      // return mapEngine.goToSection(currentIndex);
    }
  }

  function handleResize() {
    offset = -$( this ).height() / 2;
    handleScroll();
  }

  handleResize.call(window)
  $(window).resize(handleResize);
  $(window).scroll(handleScroll);
}
