var leftIndex = 0;
var rightIndex = 0;
var srcs = [
	"/static/images/trollFace1.jpg",
	"/static/images/trollFace2.jpg",
	"/static/images/trollFace3.jpg",
	"/static/images/trollFace4.jpg"
];

function rotate(){
	var frequency = 500;
	leftIndex = (leftIndex + 1)%srcs.length;
	rightIndex = (rightIndex + 3)%srcs.length;
	
	$("#rightRotatingFace").attr({"src" : srcs[leftIndex]});
	$("#leftRotatingFace").attr({"src" : srcs[rightIndex]});
	setTimeout('rotate()', frequency);
}

$(document).ready(function() {
	rotate();
});
