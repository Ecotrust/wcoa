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
