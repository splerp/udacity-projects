
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

// When a particular genre is selected, only show that category.
$(document).on('click', '#genrecontainer li', function (event) {
	
	var genreName = $(this).attr("data-genre");
	var genreDescription = $(this).attr("data-description");
	
	// Hide all.
	$(".genre-section").css("display", "none");
	$("#genrecontainer li").attr("class", "");
	
	// Show relevant.
	$("#genre-" + genreName).css("display", "block");
	$(this).attr("class", "selected");
	
});

// Only run code when the entire page is loaded.
onload = onLoad;

function onLoad()
{
	// Hide all categories
	$(".genre-section").css("display", "none");
	
	// Only show the "All" category initially.
	$("#genre-All").css("display", "block");
	$("#genrecontainer li[data-genre='All']").attr("class", "selected");
}