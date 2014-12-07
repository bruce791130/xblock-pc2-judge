function Pc2JudgeEditBlock(runtime, element) {
  $(element).find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
    var edxdata = {
      problemtext: $(element).find('input[name=problemtext]').val(),
    };
    $.post(handlerUrl, JSON.stringify(edxdata)).done(function(response) {
      window.location.reload(false);
    });
  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}
