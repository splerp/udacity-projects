"use strict";

var $;
var window;

var likeButtonClass = "btn-success";
var dislikeButtonClass = "btn-danger";

// Helpers
function addToPoints(domElement, amount) {
    domElement.html(parseInt(domElement.html(), 10) + amount);
}

// Returns all posts.
function getAllPostElements() {
    return $(".blog-post");
}

// Deleting post functionality
getAllPostElements().each(function () {
    var group = $(this);

	// On click, displays a confirmation menu then removes the entry.
    $(".button-delete", group).click(function (e) {
        e.preventDefault();
        if (window.confirm("Are you sure you want to delete this entry?")) {
            $.post($(this).attr("href"));
            group.remove();
        }
    });
});

// Like / dislike button functionality \\

// Add click handler for like buttons.
function handleButtonClick(group, button, reactionName, selectedClass) {

    var key = group.attr("post-key");
    var buttonPressed = button;
    var pointsDiv = group.find(".points");

    // Remove existing classes from other button.
    button.parent().find("button").each(function () {
        if ($(this).get(0) !== button.get(0)) {
            if ($(this).hasClass(likeButtonClass)) {
                addToPoints(pointsDiv, -1);
            }
            if ($(this).hasClass(dislikeButtonClass)) {
                addToPoints(pointsDiv, 1);
            }
            $(this)
                .removeClass(likeButtonClass)
                .removeClass(dislikeButtonClass)
                .addClass("btn-default");
        }
    });

    if (buttonPressed.hasClass(selectedClass)) {
        // The button is already selected - unset the value.
        // Post the blog post reaction.
        $.post("/blog/react/" + key, {reaction_type: ""}, function (responseData) {
            if (responseData.success) {
                // Update the count locally.
                if (selectedClass === likeButtonClass) {
                    addToPoints(pointsDiv, -1);
                } else {
                    addToPoints(pointsDiv, 1);
                }

				// Update button classes.
                buttonPressed.removeClass(selectedClass);
                buttonPressed.addClass("btn-default");
            }

        });
    } else {
        // Post the blog post reaction.
        $.post("/blog/react/" + key, {reaction_type: reactionName}, function (responseData) {
            if (responseData.success) {
                // Update the count locally.
                if (selectedClass === likeButtonClass) {
                    addToPoints(pointsDiv, 1);
                } else {
                    addToPoints(pointsDiv, -1);
                }

				// Update button classes.
                buttonPressed.removeClass("btn-default");
                buttonPressed.addClass(selectedClass);
            }
        });
    }
}

// Set buttons to initial values.
function initialiseButtonStates() {
    getAllPostElements().each(function () {
        var group = $(this);
        var key = group.attr("post-key");

        // Set button default values.
        $.get("/blog/reactstatus/" + key, function (responseData) {
            if (responseData.success) {
                if (responseData.value === "like") {
                    group.find(".like-post")
                        .removeClass("btn-default")
                        .addClass("btn-success");
                }
                if (responseData.value === "dislike") {
                    group.find(".dislike-post")
                        .removeClass("btn-default")
                        .addClass(dislikeButtonClass);
                }
            }
        });

        // Add button listeners.
        $(this).find(".like-post").click(function () {
            handleButtonClick(group, $(this), "like", likeButtonClass);
        });

        $(this).find(".dislike-post").click(function () {
            handleButtonClick(group, $(this), "dislike", dislikeButtonClass);
        });
    });
}

initialiseButtonStates();