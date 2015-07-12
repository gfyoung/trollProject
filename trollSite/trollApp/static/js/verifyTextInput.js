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
		var textInput = $("textarea").val().replace(/\s/g, "");
		debugger;
		
		if(!textInput){
			e.preventDefault();
			setTimeout(playTrollSong, 500);
			
			if($(".error").html() == ""){
				$(".error").html("Input is empty!").after("<br>");
			}
		}
	});
});
