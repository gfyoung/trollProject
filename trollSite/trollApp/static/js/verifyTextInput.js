var playVideoEmptyInputProb = 0.5;

function playTrollSong() {
	if(Math.random() < playVideoEmptyInputProb) {
		alert("Did you think you could troll me by sending an empty request?");
		alert("Think again! :P");
		
		$.ajax({
			type: "GET",
			url: "/trollApp/playTrollSong"
		});
	}
}

$(document).ready(function() {
	$("form").submit(function(e) {
		var textInput = $("textarea").html().replace(/\s/g, "");
		$(".error").empty();

		if(!textInput){
			e.preventDefault();
			$(".error").html("Input is empty!").after("<br>");
			
			setTimeout(playTrollSong, 500);
		}
	});
});