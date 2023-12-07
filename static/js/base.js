// Flashcard functions

var currentFlashcardIndex = 0;

function showFlashcard(index) {
    var flashcardContent = document.getElementById("flashcard-content");

    // Ensure the index is within bounds
    if (index >= 0 && index < flashcards.length) {
        var currentFlashcard = flashcards[index];

        // Update the content of the flashcard
        flashcardContent.innerHTML = `
            <h2>${currentFlashcard[0]}</h2>
            <p>${currentFlashcard[1]}</p>
            <!-- Add more elements as needed -->
        `;

        currentFlashcardIndex = index;
    } else {
        // Optionally, handle out-of-bounds case
        flashcardContent.innerHTML = "<p>No more flashcards.</p>";
    }
}

function showNextFlashcard() {
    showFlashcard(currentFlashcardIndex + 1);
}

function showPreviousFlashcard() {
    showFlashcard(currentFlashcardIndex - 1);
}

function shuffleFlashcards() {
    // Shuffle the flashcards array
    flashcards = shuffleArray(flashcards);

    // Show the first flashcard in the shuffled order
    showFlashcard(0);
}

// Fisher-Yates shuffle algorithm
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Show the first flashcard when the page loads
showFlashcard(0);