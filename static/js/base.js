// ======================================================================================================
// DROPDOWN MENU
// ======================================================================================================
$('.dropbtn').click(function () {
    const menu = document.querySelector('.dropdown-content');
    menu.style.display = menu.style.display === 'none' ? 'grid' : 'none';

    // Add an event listener to hide the dropdown when clicking outside
    document.addEventListener('click', function (event) {
        const isClickInsideDropdown = menu.contains(event.target);
        const isClickOnButton = event.target.classList.contains('dropbtn');

        if (!isClickInsideDropdown && !isClickOnButton) {
            menu.style.display = 'none';
        }
    });
});

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

    // Update question number
    $('#question-num').text((CURRENT_INDEX+1) + ' / ' + NUM_FLASHCARDS)
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
    const questionField = document.getElementById('question');
    const answerField = document.getElementById('answer');

    const q_codeSection = document.getElementById('q-code-section');
    const q_imageSection = document.getElementById('q-image-section');
    const q_codeType = document.getElementById('q-code-sel');
    const q_codeInput = document.getElementById('q-code-figure');
    const q_imageInput = document.getElementById('q-image-figure');

    const q_codeSelection = document.getElementById('q-code-selection');
    const q_imageSelection = document.getElementById('q-image-selection');
    const q_currentImage = document.getElementById('q-card-image');

    if (q_codeSelection || q_imageSelection){
        if (q_codeSelection.checked) {
            // Display only code input
            q_codeSection.style.display = 'block';
            q_imageSection.style.display = 'none';
            questionField.required = false;
            q_codeType.required = true;
            q_codeInput.required = true;
            q_imageInput.required = false;
        } else if (q_imageSelection.checked) {
            q_codeSection.style.display = 'none';
            q_imageSection.style.display = 'block';
            questionField.required = false;
            q_codeType.required = false;
            q_codeInput.required = false;
            
            if (q_currentImage) {
                q_imageInput.required = false;
            } else {
                q_imageInput.required = true;
            }

        } else {
            // Display neither code nor image input
            q_codeSection.style.display = 'none';
            q_imageSection.style.display = 'none';
            questionField.required = true;
            q_codeType.required = false;
            q_codeInput.required = false;
            q_imageInput.required = false;
        }
    }

    const a_codeSection = document.getElementById('a-code-section');
    const a_imageSection = document.getElementById('a-image-section');
    const a_codeType = document.getElementById('a-code-sel');
    const a_codeInput = document.getElementById('a-code-figure');
    const a_imageInput = document.getElementById('a-image-figure');

    const a_codeSelection = document.getElementById('a-code-selection');
    const a_imageSelection = document.getElementById('a-image-selection');
    const a_currentImage = document.getElementById('a-card-image');

    if (a_codeSelection || a_imageSelection) {
        if (a_codeSelection.checked) {
            // Display only code input
            a_codeSection.style.display = 'block';
            a_imageSection.style.display = 'none';
            answerField.required = false;
            a_codeType.required = true;
            a_codeInput.required = true;
            a_imageInput.required = false;
        } else if (a_imageSelection.checked) {
            a_codeSection.style.display = 'none';
            a_imageSection.style.display = 'block';
            answerField.required = false;
            a_codeType.required = false;
            a_codeInput.required = false;

            if (a_currentImage) {
                a_imageInput.required = false;
            } else {
                a_imageInput.required = true;
            }
            
        } else {
            // Display neither code nor image input
            a_codeSection.style.display = 'none';
            a_imageSection.style.display = 'none';
            answerField.required = true;
            a_codeType.required = false;
            a_codeInput.required = false;
            a_imageInput.required = false;
        }
    }   
});

function toggleQuestionFields(selectedType) {
    const questionField = document.getElementById('question');

    const codeSection = document.getElementById('q-code-section');
    const imageSection = document.getElementById('q-image-section');
    const codeType = document.getElementById('q-code-sel');
    const codeInput = document.getElementById('q-code-figure');
    const imageInput = document.getElementById('q-image-figure');

    const currentImage = document.getElementById('q-card-image');

    if (selectedType === 'code') {
        // Display only code input
        codeSection.style.display = 'block';
        imageSection.style.display = 'none';
        questionField.required = false;
        codeType.required = true;
        codeInput.required = true;
        imageInput.required = false;
    } else if (selectedType === 'image') {
        // Display only image input
        codeSection.style.display = 'none';
        imageSection.style.display = 'block';
        questionField.required = false;
        codeType.required = false;
        codeInput.required = false;
        
        // Require user to enter a image file if one doesn't exist
        if (currentImage === null) {
            imageInput.required = true;
        } else {
            imageInput.required = false;
        }

    } else {
        // Display neither code nor image input
        codeSection.style.display = 'none';
        imageSection.style.display = 'none';
        questionField.required = true;
        codeType.required = false;
        codeInput.required = false;
        imageInput.required = false;
    }
}

function toggleAnswerFields(selectedType) {
    const answerField = document.getElementById('answer');

    const codeSection = document.getElementById('a-code-section');
    const imageSection = document.getElementById('a-image-section');
    const codeType = document.getElementById('a-code-sel');
    const codeInput = document.getElementById('a-code-figure');
    const imageInput = document.getElementById('a-image-figure');

    const currentImage = document.getElementById('a-card-image');

    if (selectedType === 'code') {
        // Display only code input
        codeSection.style.display = 'block';
        imageSection.style.display = 'none';
        answerField.required = false;
        codeType.required = true;
        codeInput.required = true;
        imageInput.required = false;
    } else if (selectedType === 'image') {
        // Display only image input
        codeSection.style.display = 'none';
        imageSection.style.display = 'block';
        answerField.required = false;
        codeType.required = false;
        codeInput.required = false;

        // Require user to enter a image file if one doesn't exist
        if (currentImage === null){
            imageInput.required = true;
        } else {
            imageInput.required = false;
        }
        
    } else {
        // Display neither code nor image input
        codeSection.style.display = 'none';
        imageSection.style.display = 'none';
        answerField.required = true;
        codeType.required = false;
        codeInput.required = false;
        imageInput.required = false;
    }
}

// ======================================================================================================
// Autocomplete Search For Categories
// ======================================================================================================
$(function () {
    $("#search").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/autocomplete", // Flask endpoint URL
                dataType: "json",
                data: {
                    search: request.term
                },
                success: function (data) {
                    response(data.options);
                }
            });
        },
        minLength: 3, // Minimum characters before triggering autocomplete
    });
});