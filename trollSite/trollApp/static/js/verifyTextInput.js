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

function displayMsg(msg) {
	if($(".error").html() == ""){
		$(".error").after("<br>");
	}
	
	$(".error").html(msg);
}

$(document).ready(function() {
	$("form").submit(function(e) {
		var textInput = $("textarea").val().replace(/\s/g, "");
	
		if(!textInput){
			e.preventDefault();
			displayMsg("Input is empty!");
			setTimeout(playTrollSong, 500);
		}else{
			var formId = $("form > textarea")[0].id;
			
			switch(formId){
				case "suggestion":
					e.preventDefault();
					var csrfmiddlewaretoken = $("form > input[name='csrfmiddlewaretoken']")[0].value;
					$.ajax({
						url: "/trollApp/sendSuggestion",
						type: "POST",
						data: {
							"csrfmiddlewaretoken": csrfmiddlewaretoken,
							"suggestion": textInput
						}
					}).done(function(data) {
						displayMsg("The Troll Master thanks you!");
						$("textarea").val("");
					}).error(function() {
						displayMsg("Error! Please try sending again.");
					});
					break;
				case "customCode":
				default:
					break;
			}
		}
	});
});
