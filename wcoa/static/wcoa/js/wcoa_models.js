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
    var bitly_login = "wcoasupport",
        bitly_access_token = 'd46db74df0e396e4d52e82115ebdf3659f5115f5',
        long_url = self.getURL();

    var params = {
      "long_url" : long_url
    }

    $.ajax({
          url: "https://api-ssl.bitly.com/v4/shorten?",
          cache: false,
          dataType: "json",
          method: "POST",
          contentType: "application/json",
          beforeSend: function (xhr) {
              xhr.setRequestHeader("Authorization", "Bearer " + bitly_access_token);
          },
          data: JSON.stringify(params)
      }).done(function(response) {
        setTimeout(function(){
          $('.in #short-url')[0].value = response.link;
        }, 300);

      }).fail(function(data) {
          console.log(data);
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
