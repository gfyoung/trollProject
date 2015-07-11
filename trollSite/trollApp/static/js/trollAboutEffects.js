var ids = ["#redText", "#orangeText", "#greenText"];
var randomIdIndex = 0;
var vanishTimeout = 10000;
var reappearTimeout = 1000;

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
	makeIdVanish();
});