"use strict";

// Called from google api client.js when loaded.
function init() {

    // Referencing API path, attempt to load API.
	var rootpath = "//" + window.location.host + "/_ah/api";
	gapi.client.load('helloworldendpoints', 'v1', loaded, rootpath);
}

// When API is loaded, start.
function loaded () {

	enableButtons ();
}

function enableButtons () {
	// Set the onclick action for the first button
	var btn = document.getElementById("input_greet_generically");
	btn.onclick= function(){greetGenerically();};
	
	// Update the button label now that the button is active
	btn.value="Click me for a generic greeting";
	
	// Set the onclick action for the second button
	btn = document.getElementById("input_greet_by_name");
	btn.onclick=function(){greetByName();};
	
	// Update the button label now that the button is active
	btn.value="Click me for a personal greeting";
}

function greetGenerically () {

	// Call the sayHello() function.
	var request = gapi.client.helloworldendpoints.sayHello();
	request.execute(sayHelloCallback);
}

function greetByName () {
	// Get the name from the name_field element
	var name = document.getElementById("name_field").value;
	
	// Call the sayHelloByName() function.
	var request = gapi.client.helloworldendpoints.sayHelloByName({'name': name});
	request.execute(sayHelloCallback);
}

// Callback for API response.
function sayHelloCallback (response) {
	alert(response.greeting);	
}



