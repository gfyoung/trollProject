var playVideo = false;
var playVideoProb = 0.1;
var alertVideoProb = 0.05;

var changeFontSizeProb = 0.1;
var fontSizeMultiplier = 10;
var fontSize = 16;

$(document).ready(function() {
	$("a.menuLink").hover(
		function() {
			if(Math.random() < playVideoProb) {
				playVideo = true;
				$.ajax({
					url: "/trollApp/playTrollSong",
					type: "GET"
				});
			}else{
				playVideo = false;
			}
		},
		function() {
			if(playVideo && Math.random() < alertVideoProb) {
				alert("Who knew hovering over a link was so perilous? :P");
			}
		}
	);
	
	$("a.download").hover(
		function() {
			fontSize = $("a.download#" + this.id).css("font-size").replace("px", "");
			
			if(Math.random() < changeFontSizeProb) {
				$("a.download#" + this.id).css("font-size", fontSize * fontSizeMultiplier + "px");
			}
		},
		function() {
			$("a.download#" + this.id).css("font-size", fontSize + "px");
		}
	);
});
