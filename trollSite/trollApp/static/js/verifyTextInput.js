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

function isValidInput(form) {
    var textInput = $(form).children('textarea').val().replace(/\s/g, '');

    if (!textInput) {
        displayMsg('Input is empty!');
        setTimeout(playTrollSong, 500);
        return false;
    } else {
        if ($(form).children('.error').next()[0]
                .tagName.toLowerCase() === 'br') {
            $(form).children('.error').next().remove();
        }

        $(form).children('.error').html('');
        return true;
    }
}
