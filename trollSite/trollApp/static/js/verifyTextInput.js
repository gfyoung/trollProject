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

function isValidString(form, validString, infoMsg) {
    if (!validString) {
        displayMsg(infoMsg);
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

function isValidInput(form) {
    var textInput = $(form).children('textarea').val().replace(/\s/g, '');
    return isValidString(form, textInput, 'Input is empty!');
}

function isValidEmailAddress(address) {
    // Allows for email address field to be optional,
    // as it will not be empty if the input has the
    // 'required' descriptor inside the tag
    if (!address) {
        return true;
    }

    var isValidEmailAddress = false;
    var pattern = /[!?'":#/~`\[\]{}\-\+=|\(\)\^%]/;

    if (!pattern.match(address)) {
        var atComponents = address.split('@');
        isValidEmailAddress = atComponents.length == 2 ||
            atComponents[atComponents.length - 1].split(/\./).length > 1;
    }

    return isValidEmailAddress;
}

function isValidSender(form) {
    var senderEmail = $(form).children('.info[name=sender]').val();
    return isValidString(form, isValidEmailAddress(
        senderEmail), 'Invalid sender email!');
}

function isValidReceiver(form) {
    var receiverEmail = $(form).children('.info[name=receiver]').val();
    return isValidString(form, isValidEmailAddress(
        receiverEmail), 'Invalid receiver email!');
}
