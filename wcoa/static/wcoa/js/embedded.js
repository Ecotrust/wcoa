/**
 * Assuming that this file is only loaded in an iframe (DLP)
 * Open all links in new tab
 */

$(document).ready(function () {
  $("a").attr("target","_blank");
});
