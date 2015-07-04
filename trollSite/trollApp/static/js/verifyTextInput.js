$(document).ready(function() {
	$("form").submit(function(e) {
		var textInput = $("textarea").html().replace(/\s/g, "");
		$("#error").empty();
		
		if(!textInput){
			e.preventDefault();
			$("#error").append("<div style='color:red'>Input is empty!</div><br>");
		}
	});
});