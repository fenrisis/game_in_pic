// Get necessary elements from the DOM
const quizBox = document.getElementById('quiz-box');
const scoreBox = document.getElementById('score-box');
const resultBox = document.getElementById('result-box');
const timerBox = document.getElementById('timer-box');

// Function to activate the timer
const activateTimer = (time) => {
  // Format and display the initial timer value
  if (time.toString().length < 2) {
    timerBox.innerHTML = `<b>0${time}:00</b>`;
  } else {
    timerBox.innerHTML = `<b>${time}:00</b>`;
  }

  let minutes = time - 1;
  let seconds = 60;
  let displaySeconds;
  let displayMinutes;

  const timer = setInterval(() => {
    // Decrement seconds and minutes
    seconds--;
    if (seconds < 0) {
      seconds = 59;
      minutes--;
    }

    // Format minutes and seconds for display
    displayMinutes = minutes.toString().padStart(2, '0');
    displaySeconds = seconds.toString().padStart(2, '0');

    // Check if time is up and handle the end of the quiz
    if (minutes === 0 && seconds === 0) {
      timerBox.innerHTML = "<b>00:00</b>";
      setTimeout(() => {
        clearInterval(timer);
        alert('Time over');
        sendData();
      }, 500);
    }
    // Update the timer display
    timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`;
  }, 1000);
};

// Make an AJAX GET request to fetch quiz data
const fetchQuizData = () => {
  // Replace 'quiz-data-endpoint' with the actual endpoint URL to fetch quiz data
  fetch('quiz-data-endpoint')
    .then(response => response.json())
    .then(data => {
      const questions = data.questions;

      // Iterate over the questions and render them on the page
      questions.forEach(question => {
        quizBox.innerHTML += `
          <hr>
          <div class="mb-2">
            <b>${question.text}</b>
          </div>
        `;

        question.options.forEach(option => {
          quizBox.innerHTML += `
            <div>
              <input type="radio" class="ans" id="${question.id}-${option.id}" name="${question.id}" value="${option.id}">
              <label for="${question.id}">${option.text}</label>
            </div>
          `;
        });

        // Add image for the question
        if (question.image) {
          const img = document.createElement('img');
          img.src = question.image;
          img.alt = 'Question Image';
          quizBox.appendChild(img);
        }
      });

      // Activate the timer with the specified time
      activateTimer(data.time);
    })
    .catch(error => console.log(error));
};

// Handle form submission
const quizForm = document.getElementById('quiz-form');
quizForm.addEventListener('submit', e => {
  e.preventDefault();
  sendData();
});

const sendData = () => {
  const elements = [...document.getElementsByClassName('ans')];
  const data = {};

  // Collect the user's answers and build the data object
  elements.forEach(el => {
    if (el.checked) {
      data[el.name] = el.value;
    } else {
      if (!data[el.name]) {
        data[el.name] = null;
      }
    }
  });

  // Make an AJAX POST request to save the quiz and display the results
  fetch('save-quiz-endpoint', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(result => {
      // Display the score and results on the page
      scoreBox.innerHTML = `${result.passed ? 'Congratulations! ' : 'Ups..:( '}Your result is ${result.score.toFixed(2)}%`;

      result.answers.forEach(answer => {
        const resDiv = document.createElement('div');
        resDiv.classList.add('container', 'p-3', 'text-light', 'h6');

        if (answer.is_correct) {
          resDiv.classList.add('bg-success');
          resDiv.innerHTML = `${answer.question} - answered: ${answer.answer}`;
        } else {
          resDiv.classList.add('bg-danger');
          resDiv.innerHTML = `${answer.question} - answered: ${answer.answer} | correct answer: ${answer.correct_answer}`;
        }

        resultBox.append(resDiv);
      });

      // Hide the quiz form
      quizForm.classList.add('not-visible');
    })
    .catch(error => console.log(error));
};

// Fetch quiz data when the page loads
fetchQuizData();
