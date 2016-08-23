"use strict";

// Used when calling the API.
var apiName = "snakesandladdersendpoints";

var gameArea;
var gameBoard;
var gameState;
var playerObjects;
var joinGameButton;
var playTurnButton;
var startGameButton;

var currentGameState;
var currentPlayerData;
var currentPlayerTurnName;

// Called from google api client.js when loaded.
function onLoad() {

    console.log("Loading 1");

    // Referencing API path, attempt to load API.
	var rootPath = "//" + window.location.host + "/_ah/api";
	gapi.client.load(apiName, 'v1', function() {
	    // On completed loading.

        console.log("Loading 2");
	    initialiseData();

	    setInterval(refreshData, 1500);

        // Add button listeners.
        joinGameButton.click(function () {
            joinGame();
        });

        playTurnButton.click(function () {
            playTurn();
        });

        startGameButton.click(function () {
            startGame();
        });

	}, rootPath);
}

function sendAPIRequest(endPoint, data, callback)
{
    var request = window["gapi"]["client"][apiName][endPoint](data);
    request.execute(function(response) {

        if(!response.success)
        {
            console.log("Something bad happened :o 'Apic' fail, amirite?");
            console.log(response.events)
        }
        refreshData(callback, response);
    });
}

function initialiseData()
{
    gameArea = $("#game-area");
    gameBoard = $("#game-board");
    gameState = $("#game-state");
    joinGameButton = $("#button-join-game");
    playTurnButton = $("#button-play-turn");
    startGameButton = $("#button-next-game-state");

    refreshData();
}

function refreshData(callback, response)
{
    setTimeout(function(){
        $.get("/games/" + gameKey + "/getdata", function (responseData) {

            if (responseData.success) {

                currentGameState = responseData.game_state;
                currentPlayerTurnName = responseData.current_player_name;
                currentPlayerData = responseData.player_data;


                refreshUI();
            }

            if(callback != null)
            {
                callback(response);
            }
        });
    }, 200);

    // All elements that should be updated when api is called.
}

function refreshUI()
{
    gameState.html("Game is currently: " + currentGameState);

    // Check if they're already in the game and enable / disable the Join button.
    joinGameButton.prop("disabled", false);
    currentPlayerData.forEach(function(playerData, index, array) {
        if(playerData.name == playerName)
        {
            joinGameButton.prop("disabled", true);
        }
    });

    playTurnButton.prop("disabled", currentPlayerTurnName != playerName);

    var coloursToChooseFrom = ["blue", "red", "yellow", "green", "grey", "purple"];

    // Remove any existing players.
    $("#game-board .player-token").remove();

    currentPlayerData.forEach(function(playerData, index, array) {

        var thingToMove = $(document.createElement("div"));
        thingToMove.addClass("player-token");

        $("#game-board").append(thingToMove);

        var numSquaresX = 10;
        var numSquaresY = 10;
        var boardWidth = 460;
        var boardHeight = 420;

        var counterSize = 15;

        var squareSizeX = Math.floor(boardWidth / numSquaresX);
        var squareSizeY = Math.floor(boardHeight / numSquaresY);

        var thingXPos = (playerData.position - 1) % numSquaresX;
        var thingYPos = Math.floor((playerData.position - 1) / numSquaresX);

        console.log("POS " + playerData.position + ". Moving to tile pos " + thingXPos + ", " + thingYPos);

        var finalPosX = (thingXPos * squareSizeX) + Math.floor(squareSizeX / 2);
        var finalPosY = (thingYPos * squareSizeY) + Math.floor(squareSizeY / 2);

        thingToMove.css({ backgroundColor: coloursToChooseFrom[index % coloursToChooseFrom.length]});
        if(thingYPos % 2 == 0)
        {
            thingToMove.css({ left: "" + (finalPosX - counterSize/2) + "px", right: "auto", bottom: "" + (finalPosY - counterSize/2) + "px"});
        }
        else
        {
            thingToMove.css({ left: "auto",  right: "" + (finalPosX - counterSize/2) + "px", bottom: "" + (finalPosY - counterSize/2) + "px"});
        }
    });
}

function joinGame()
{
    console.log("Loading 3");

    sendAPIRequest("joinGame", {"game_name": gameName, "player_name": playerName}, function() {
        console.log("Loading 4");
    })
}

function playTurn()
{
    sendAPIRequest("playTurn", {"game_name": gameName, "player_name": playerName}, function() {
        console.log("Loading 4b");
    })
}

// TODO Hide button if not owner of game, or add check on api side
function startGame()
{

    sendAPIRequest("startGame", {"game_name": gameName}, function(response) {
        console.log("Game started! Success: " + response.success);


    })
}


// Set button default values.
/*$.get("/blog/reactstatus/" + key, function (responseData) {
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
});*/