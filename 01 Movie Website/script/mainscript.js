 // Pause the video when the modal is closed
$(document).on("click",
			   ".hanging-close, .modal-backdrop, .modal",
			   function (event) {
	// Remove the src so the player itself gets removed,
	// as this is the only reliable way to
	// ensure the video stops playing in IE
	$("#trailer-video-container").empty();
});
// Start playing the video whenever the trailer modal is opened
$(document).on('click', '.movie-tile', function (event) {
	var trailerYouTubeId = $(this).attr('data-trailer-youtube-id');
	var sourceUrl = 'http://www.youtube.com/embed/' 
	+ trailerYouTubeId + '?autoplay=1&html5=1';
	$("#trailer-video-container").empty().append($("<iframe></iframe>", {
	  'id': 'trailer-video',
	  'type': 'text-html',
	  'src': sourceUrl,
	  'frameborder': 0
	}));
	
	var longDesc = $(this).attr('data-long-desc');
	
	$("#trailer-description-container").text(longDesc);
});

$(document).on('click', '#genrecontainer li', function (event) {
	
	var genreName = $(this).attr("data-genre");
	var genreDescription = $(this).attr("data-description");
	
	console.log("test - " + genreName);
	
	$("#genrecontainer li").attr("class", "");
	$(this).attr("class", "selected");
	
	// Hide all.
	$(".genre-section").css("display", "none");
	
	// Show relevant.
	$("#genre-" + genreName).css("display", "block");
	
});

onload = onLoad;

function onLoad()
{
	$(".genre-section").css("display", "none");
	
	$("#genre-All").css("display", "block");
}


/*
// Animate in the movies when the page loads
$(document).ready(function () {
  $('.genre-section').hide().first().show("fast", function showNext() {
	$(this).next("div").show("fast", showNext);
  });
});
*/