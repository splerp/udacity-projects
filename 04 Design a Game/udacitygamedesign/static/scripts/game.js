"use strict";

// Used when calling the API.
var apiName = "snakesandladdersendpoints";

var gameArea;
var gameBoard;
var context;
var gameState;
var joinGameButton;
var playTurnButton;
var startGameButton;

var currentGameState;
var currentPlayerData;
var currentPlayerTurnName;

var gameOwner = "";

var turnInfoText = "";

// Called from google api client.js when loaded.
function onLoad() {

    console.log("Loading 1");

    // Referencing API path, attempt to load API.
	var rootPath = "//" + window.location.host + "/_ah/api";
	window.gapi.client.load(apiName, 'v1', function() {
	    // On completed loading.

        console.log("Loading 2");
	    initialiseData();

	    setInterval(refreshData, 1000);

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
    var request = window.gapi.client[apiName][endPoint](data);
    request.execute(function(response) {

        if(!response.success)
        {
            console.log("Something bad happened :o 'Apic' fail, amirite?");
            console.log(response.events);
        }
        refreshData(callback, response);
    });
}

function initialiseData()
{
    gameArea = $("#game-area");
    gameBoard = $("#game-board");
	context = gameBoard.get(0).getContext("2d");
	
    gameState = $("#game-state");
    joinGameButton = $("#button-join-game");
    playTurnButton = $("#button-play-turn");
    startGameButton = $("#button-next-game-state");

    refreshData();
}

function drawGameBoard()
{
	var snakes = gameBoardData.snakes;
	var ladders = gameBoardData.ladders;
	
	var lineWidth = 6;
	var circleEndRadius = 6;
	var ladderColour = "#fc0";
	var snakeColour = "#f00";
	
	
	context.clearRect(0, 0, 460, 420);
	
	// Ladders.
	ladders.forEach(function(ladder, index, array) {
		
		var ladderStartPos = getPosFromTileIndex(ladder[0]);
		var ladderEndPos = getPosFromTileIndex(ladder[1]);
		
		context.beginPath();
		context.fillStyle = ladderColour;
		context.arc(ladderStartPos[0], ladderStartPos[1], circleEndRadius, 0, 2 * Math.PI);
		context.fill();
		
		context.fillStyle = null;
		
		context.beginPath();
		context.lineWidth = lineWidth;
		context.strokeStyle = ladderColour;
		
		context.moveTo(ladderStartPos[0],ladderStartPos[1]);
		context.lineTo(ladderEndPos[0],ladderEndPos[1]);
		context.stroke();
		
	});
	
	// Snakes.
	snakes.forEach(function(snake, index, array) {

		var snakeStartPos = getPosFromTileIndex(snake[0]);
		var snakeEndPos = getPosFromTileIndex(snake[1]);

		context.beginPath();
		context.fillStyle = snakeColour;
		context.arc(snakeStartPos[0], snakeStartPos[1], circleEndRadius, 0, 2 * Math.PI);
		context.fill();

		context.fillStyle = null;

		context.beginPath();
		context.lineWidth = lineWidth;
		context.strokeStyle = snakeColour;

		context.moveTo(snakeStartPos[0],snakeStartPos[1]);
		context.lineTo(snakeEndPos[0],snakeEndPos[1]);
		context.stroke();
	});

	// Players.
	var coloursToChooseFrom = ["blue", "green", "grey", "purple", "orange"];
	var playerRadius = 12;

	currentPlayerData.forEach(function(player, index, array) {

		var playerPos = getPosFromTileIndex(player.position);

		context.beginPath();
		context.fillStyle = coloursToChooseFrom[index % coloursToChooseFrom.length];
		context.arc(playerPos[0], playerPos[1], playerRadius, 0, 2 * Math.PI);
		context.fill();
	});
}

function refreshData(callback, response)
{
	// Wait a short period of time, then get data.
    setTimeout(function(){
        $.get("/games/" + gameKey + "/getdata", function (responseData) {

            if (responseData.success) {

				// Set current data.
                currentGameState = responseData.game_state;
				
                currentPlayerTurnName = responseData.current_player_name;
                currentPlayerData = responseData.player_data;
				
				gameOwner = responseData.owner;

                refreshUI();
				drawGameBoard();
            }

            if(callback != null)
            {
                callback(response);
            }
        });
    }, 200);

    // All elements that should be updated when api is called.
}

function updatePlayerInfo(state)
{
	switch(state)
	{
		case "created":
			gameState.html("Waiting for players to join.");
			break;
		
		case "playing":
			if(playerName == currentPlayerTurnName)
			{
				gameState.html("Your turn!");
			}
			else
			{
				gameState.html("Waiting for " + currentPlayerTurnName + "...");
			}
			
			break;
		
		case "cancelled":
			gameState.html("This game has been cancelled.");
			break;
		
		case "complete":
			gameState.html("Game has been won!");
			break;
	}
}

function refreshUI()
{
	updatePlayerInfo(currentGameState);

    // Check if they're already in the game and enable / disable the Join button.
    joinGameButton.prop("disabled", false);
    currentPlayerData.forEach(function(playerData, index, array) {
        if(playerData.name == playerName)
        {
            joinGameButton.prop("disabled", true);
        }
    });

    playTurnButton.prop("disabled", currentGameState != "playing" || currentPlayerTurnName != playerName);
	startGameButton.prop("disabled", currentGameState != "created" || currentPlayerData.length < 2 || gameOwner != playerName);
	
	// Remove any existing player list entries.
    $("#game-players-list").empty();
	$("#game-players-list").append($(document.createElement("p")).html("" + currentPlayerData.length + " players."));
	
    currentPlayerData.forEach(function(playerData, index, array) {

        var thingToMove = $(document.createElement("div"));
        thingToMove.addClass("game-player");
		
		if(playerData.name == currentPlayerTurnName)
		{
			thingToMove.addClass("current-player");
		}

        $("#game-players-list").append(thingToMove);
		thingToMove.append($(document.createElement("h3")).html(playerData.name));
		thingToMove.append($(document.createElement("p")).html("At pos " + playerData.position));
    });
	
	$("#game-players-list").append($(document.createElement("p")).html(turnInfoText));
}

function getPosFromTileIndex(tileIndex)
{
	var numSquaresX = 10;
	var numSquaresY = 10;
	var boardWidth = 460;
	var boardHeight = 420;

	var squareSizeX = Math.floor(boardWidth / numSquaresX);
	var squareSizeY = Math.floor(boardHeight / numSquaresY);

	var thingXPos = (tileIndex - 1) % numSquaresX;
	var thingYPos = Math.floor((tileIndex - 1) / numSquaresX);

	var finalPosX = (thingXPos * squareSizeX) + Math.floor(squareSizeX / 2);
	var finalPosY = (boardHeight - squareSizeY) - (thingYPos * squareSizeY) + Math.floor(squareSizeY / 2);

	// Reverse every second row.
	if(thingYPos % 2 != 0)
	{
		finalPosX = boardWidth - finalPosX;
	}
	
	return [finalPosX, finalPosY];
}

function joinGame()
{
    console.log("Loading 3");

    sendAPIRequest("joinGame", {"game_name": gameName, "player_name": playerName}, function() {
        
    })
}

function playTurn()
{
    sendAPIRequest("playTurn", {"game_name": gameName, "player_name": playerName}, function(response) {
        
		// Turn played. Use their roll and any special events.
		
		turnInfoText = "You rolled " + response.roll + ".";
		JSON.parse(response.events).forEach(function(anEvent, index, array) {
			turnInfoText += "<br />" + anEvent;
		});
		
    })
}

// TODO Hide button if not owner of game, or add check on api side
function startGame()
{

    sendAPIRequest("startGame", {"game_name": gameName}, function(response) {
        console.log("Game started! Success: " + response.success);


    })
}
