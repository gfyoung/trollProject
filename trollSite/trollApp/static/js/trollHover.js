var playVideo = false;
var playVideoProb = 0.1;
var alertVideoProb = 0.05;

$(document).ready(function() {
	$("a").hover(
		function() {
			if(Math.random() < playVideoProb) {
				playVideo = true;
				$.ajax({
					type: "GET",
					url: "/trollApp/playTrollSong"
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
	)
});