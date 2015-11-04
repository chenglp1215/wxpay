var viewPortScale;
viewPortScale = 0.5;
 
var detectBrowser = function(name) {
 if(navigator.userAgent.toLowerCase().indexOf(name) > -1) {
	 return true;
 } else {
	 return false;
 }
};

if(detectBrowser('ucbrowser')) {
 document.getElementById('viewport').setAttribute(
 'content', 'user-scalable=no, width=device-width, minimum-scale=0.5, initial-scale=' + viewPortScale);
} else if(detectBrowser('360browser')) {
 document.getElementById('viewport').setAttribute(
 'content', 'target-densitydpi=320,user-scalable=no, width=640, minimum-scale=1, initial-scale=1');
} else {
 document.getElementById('viewport').setAttribute(
 'content', 'target-densitydpi=320, user-scalable=no,width=640, minimum-scale=0.5, initial-scale=' + viewPortScale);
}

function set_content_height(){
  $('.content').css('min-height',$(window).height())
}
  