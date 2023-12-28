// ======================================================================================================
// FLASH MESSAGES [ERRORS, WARNINGS, INFO]
// ======================================================================================================
// Automatically hide flash messages after 5 seconds (adjust as needed)
setTimeout(function () {
    $('.flash-message').fadeOut('slow');
}, 5000);

// ======================================================================================================
// HOME PAGE
// ======================================================================================================
// Flip the display card when clicked
$('.flip-flashcard').click(function () {
    const cardContent = document.getElementById('card-content-flip');
    cardContent.style.transform = cardContent.style.transform === 'rotateY(180deg)' ? 'rotateY(0deg)' : 'rotateY(180deg)';
});

// Flip the display card after a certain time interval
setInterval(function () {
    const cardContent = document.getElementById('card-content-flip');

    // Rotate card if one is present in the loaded page
    if (cardContent) {
        cardContent.style.transform = cardContent.style.transform === 'rotateY(180deg)' ? 'rotateY(0deg)' : 'rotateY(180deg)';
    }

}, 3000);

// Animate cards by swapping them from front to back
document.addEventListener('DOMContentLoaded', function () {
    const cardSlides = document.querySelectorAll('.card-content-slide');
    let currentSlide = 0;

    function showNextSlide() {
        // Animate the cards if present in the loaded page
        if (cardSlides && cardSlides.length > 0) {
            cardSlides[currentSlide].classList.remove('active-card');
            currentSlide = (currentSlide + 1) % cardSlides.length;
            cardSlides[currentSlide].classList.add('active-card');
        }
    }

    // Animate the cards if present in the loaded page
    if (cardSlides && cardSlides.length > 0) {
        setInterval(showNextSlide, 5000);
    }
});

// ======================================================================================================
// MANAGE FLASHCARD PAGE
// ======================================================================================================
// Confirm deletion of the queried question before deleting it
document.querySelectorAll('.delete-cell').forEach(function (element) {
    element.addEventListener('click', function () {
        confirmDelete(element.dataset.question);
    });
});

function confirmDelete(element) {
    var question = element;
    var result = confirm("Are you sure you want to delete this flashcard?");
    if (result) {
        window.location.href = "delete_flashcard/" + encodeURIComponent(question);
    }
};

// ======================================================================================================
// FLASHCARD PAGE
// ======================================================================================================
var CURRENT_INDEX = 0;
var NUM_FLASHCARDS = $('.flashcard').length;
var CARD_ARRAY = Array.from({ length: NUM_FLASHCARDS }, (_, index) => index);

// Rotate flashcard when clicked
$('.flashcard').click(function () {
    var id = $(this).attr('id') + '-content';
    const cardContent = document.getElementById(id);
    cardContent.style.transform = cardContent.style.transform === 'rotateY(180deg)' ? 'rotateY(0deg)' : 'rotateY(180deg)';
});

function showFlashcard(index) {
    // Ensure the index is a valid number
    if (isNaN(index) || index >= NUM_FLASHCARDS) {
        // Go back to the beginning
        showFlashcard(0);
        return;
    }
    else if (index < 0){
        // Go back to the end
        showFlashcard(NUM_FLASHCARDS - 1);
        return;
    }

    CURRENT_INDEX = index;
    var id = '#flashcard-' + CARD_ARRAY[CURRENT_INDEX];

    // Hide everything except current flashcard
    $('.flashcard').hide();
    $(id).show();
};

// Advance to the next flashcard on the page
function showNextFlashcard() {
    showFlashcard(CURRENT_INDEX + 1);
};

// Advance to the previous flashcard on the page
function showPreviousFlashcard() {
    showFlashcard(CURRENT_INDEX - 1);
};

function shuffleFlashcards() {
    // Shuffle the flashcards array
    flashcards = shuffleArray(CARD_ARRAY);
    // Show the first flashcard in the shuffled order
    showFlashcard(0);
};

// Fisher-Yates shuffle algorithm
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
};

// ======================================================================================================
// Validate Entered Text
// ======================================================================================================
function validateText(id) {
    // Validate text to ensure it only contains letters and numbers
    var textarea = document.getElementById(id);
    var pattern = /^[a-zA-Z0-9\s]+$/;

    if (!pattern.test(textarea.value)) {
        textarea.setCustomValidity("Only letters and numbers are allowed");
    } else {
        textarea.setCustomValidity("");
    }
}

// ======================================================================================================
// ADD_FLASHCARD AND EDIT_FLASHCARD PAGE
// ======================================================================================================

document.addEventListener('DOMContentLoaded', function () {
    const codeSection = document.getElementById('code-section');
    const imageSection = document.getElementById('image-section');
    const codeType = document.getElementById('code-sel');
    const codeInput = document.getElementById('code-ex');
    const imageInput = document.getElementById('image-ex');

    const codeSelection = document.getElementById('code-selection');
    const imageSelection = document.getElementById('image-selection');

    if (codeSelection || imageSelection){
        if (codeSelection.checked) {
            // Display only code input
            codeSection.style.display = 'block';
            imageSection.style.display = 'none';
            codeType.required = true;
            codeInput.required = true;
            imageInput.required = false;
        } else if (imageSelection.checked) {
            codeSection.style.display = 'none';
            imageSection.style.display = 'block';
            codeType.required = false;
            codeInput.required = false;
            imageInput.required = true;
        } else {
            // Display neither code nor image input
            codeSection.style.display = 'none';
            imageSection.style.display = 'none';
            codeType.required = false;
            codeInput.required = false;
            imageInput.required = false;
        }
    }
    
});

function toggleFields(selectedType) {
    const codeSection = document.getElementById('code-section');
    const imageSection = document.getElementById('image-section');
    const codeType = document.getElementById('code-sel');
    const codeInput = document.getElementById('code-ex');
    const imageInput = document.getElementById('image-ex');

    if (selectedType === 'code') {
        // Display only code input
        codeSection.style.display = 'block';
        imageSection.style.display = 'none';
        codeType.required = true;
        codeInput.required = true;
        imageInput.required = false;
    } else if (selectedType === 'image') {
        // Display only image input
        codeSection.style.display = 'none';
        imageSection.style.display = 'block';
        codeType.required = false;
        codeInput.required = false;
        imageInput.required = true;
    } else {
        // Display neither code nor image input
        codeSection.style.display = 'none';
        imageSection.style.display = 'none';
        codeType.required = false;
        codeInput.required = false;
        imageInput.required = false;
    }
}