function Pc2JudgeBlock(runtime, element) {
  

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}
