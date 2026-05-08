// vanilla javascript "on ready" solution from https://www.sitepoint.com/jquery-document-ready-plain-javascript/

var callback = function(){
  // Handler when the DOM is fully loaded
  app.viewModel.toggleLayers = function() {
      app.viewModel.showLayers(!app.viewModel.showLayers());
      if (app.viewModel.showLayers()) {
        $('#left-panel').css('bottom', '25px');
        // $('body.template-visualize #left-panel.panel.collapsible').each(function() { this.style.setProperty('height', 'unset', 'important');});
      } else {
        $('#left-panel').css('bottom', 'unset');
        // $('body.template-visualize #left-panel.panel.collapsible.collapsed').each(function() { this.style.setProperty('height', '45px', 'important');});
      }
      app.updateUrl();
      //if toggling layers during default pageguide, then correct step 4 position
      //self.correctTourPosition();
      //throws client-side error in pageguide.js for some reason...
  };

  app.viewModel.mapLinks.getURL = function() {
      if (window.location.hostname == "localhost") {
        return window.location.protocol + '//portal.westcoastoceans.org' + app.viewModel.currentURL();
      } else {
        return window.location.origin + app.viewModel.currentURL();
      }
  };

  app.viewModel.mapLinks.useShortURL = function() {
    var self = app.viewModel.mapLinks;
    var long_url = self.getURL();

    $.ajax({
      type: "POST",
      url: "/url_shortener/",  
      data: {
          "url": long_url,
          "csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()  
      },
      success: function(response) {
          $('#short-url')[0].value = response.shortened_url;
      },
      error: function(xhr, status, error) {
          console.log("Error shortening URL:", error);
      }
    });

  };
};

if (
    document.readyState === "complete" ||
    (document.readyState !== "loading" && !document.documentElement.doScroll)
) {
  callback();
} else {
  document.addEventListener("DOMContentLoaded", callback);
}
