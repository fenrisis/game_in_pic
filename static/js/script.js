document.addEventListener('DOMContentLoaded', function() {
    // Get the game form and user input field
    const gameForm = document.getElementById('game-form');
    const userInput = document.getElementById('user-input');
  
    // Add event listener to the game form
    gameForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Prevent form submission
  
      // Get the user input value
      const answer = userInput.value;
  
      // Make an AJAX request to the server to check the answer
      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/play');
      xhr.setRequestHeader('Content-Type', 'application/json');
  
      // Define the callback function for when the response is received
      xhr.onload = function() {
        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          handleResponse(response);
        }
      };
  
      // Send the request with the user input as JSON
      xhr.send(JSON.stringify({ user_input: answer }));
    });
  
    // Function to handle the server response
    function handleResponse(response) {
      // Get the result from the response
      const result = response.result;
  
      // Update the UI based on the result
      if (result === 'Correct') {
        alert('Congratulations! Your answer is correct!');
      } else {
        alert('Sorry, your answer is incorrect. Please try again.');
      }
    }
  });
  