define('In_relation', ['In', 'In_ws'], function(IN, In_ws) {
  "use strict";
  
(function ($) {
  //
  
  IN.WSCommands.prototype.relation_notification_count = function(message) {
    var count = message.count;
    
    if (count == 0) {
	  var count_html = '<div class="count"></div>';
	} else {
	  var count_html = '<div class="count i-badge i-badge-notification i-badge-danger i-position-top-right i-text-truncate">' + count + '</div>';
	}
    $('.notification-count.relation-count .count').replaceWith(count_html);
  };
  
})(jQuery);
  
  return;
  
});
