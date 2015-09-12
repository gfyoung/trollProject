var playVideoEmptyInputProb = 0.5;

function playTrollSong() {
	if (Math.random() < playVideoEmptyInputProb) {
		alert('Did you think you could troll me by sending an empty request?');
		alert('Think again! :P');

		$.ajax({
			type: 'GET',
			url: '/trollApp/playTrollSong'
		});
	}
}

function displayMsg(msg) {
	if ($('.error').html() == '') {
		$('.error').after('<br>');
	}

	$('.error').html('<b>ERROR:</b> ' + msg);
}

$(document).ready(function() {
	$('form').submit(function(e) {
		var textInput = $('textarea').val().replace(/\s/g, '');

		if (!textInput) {
			e.preventDefault();
			displayMsg('Input is empty!');
			setTimeout(playTrollSong, 500);
		}
	});
});
