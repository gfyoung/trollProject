var randomIdIndex = 0;
var vanishTimeout = 1000;
var reappearTimeout = 1000;

function getIds() {
	return $.map($('pre'), function(para) {
		return '#' + para.id;
	});
}
function getRandomIdIndex() {
	return Math.floor(Math.random() * ids.length);
}

function makeIdVanish() {
	randomIdIndex = getRandomIdIndex();
	$(ids[randomIdIndex]).hide();
	setTimeout(makeIdReappear, reappearTimeout);
}

function makeIdReappear() {
	$(ids[randomIdIndex]).show();
	setTimeout(makeIdVanish, vanishTimeout);
}

$(document).ready(function() {
	ids = getIds();
	makeIdVanish();
});
