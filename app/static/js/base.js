// ======================================================================================================
// DROPDOWN MENU
// ======================================================================================================
$('.dropbtn').click(function () {
    const menu = document.querySelector('.dropdown-element');
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

// Display window prompt
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
    $('#question-num').text((CURRENT_INDEX + 1) + ' / ' + NUM_FLASHCARDS)
};

// Advance to the next flashcard on the page
function showNextFlashcard() {showFlashcard(CURRENT_INDEX + 1);};
// Advance to the previous flashcard on the page
function showPreviousFlashcard() {showFlashcard(CURRENT_INDEX - 1);};

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
};

// ======================================================================================================
// ADD_FLASHCARD AND EDIT_FLASHCARD PAGE
// ======================================================================================================
document.addEventListener('DOMContentLoaded', function () {
    // Define element selectors
    const selectors = {
        question: {
            field: 'question',
            codeSection: 'q-code-section',
            imageSection: 'q-image-section',
            codeType: 'q_code_type',
            codeInput: 'q_code_example',
            imageInput: 'q_image_example',
            codeSelection: 'q-code-selection',
            imageSelection: 'q-image-selection',
            noneSelection: 'q-none-type',
            currentImage: 'q-card-image'
        },
        answer: {
            field: 'answer',
            codeSection: 'a-code-section',
            imageSection: 'a-image-section',
            codeType: 'a_code_type',
            codeInput: 'a_code_example',
            imageInput: 'a_image_example',
            codeSelection: 'a-code-selection',
            imageSelection: 'a-image-selection',
            noneSelection: 'a-none-type',
            currentImage: 'a-card-image'
        }
    };

    // Initialize form elements
    initializeForm(selectors.question);
    initializeForm(selectors.answer);
});

function initializeForm(config) {
    const elements = getElements(config);

    if (elements.codeSelection && elements.imageSelection) {
        // Set initial display
        toggleFields(elements);

        // Add event listeners
        elements.codeSelection.addEventListener('click', () => toggleFields(elements));
        elements.imageSelection.addEventListener('click', () => toggleFields(elements));
        elements.noneSelection.addEventListener('click', () => toggleFields(elements));
    }
}

function getElements(config) {
    return {
        field: document.getElementById(config.field),
        codeSection: document.getElementById(config.codeSection),
        imageSection: document.getElementById(config.imageSection),
        codeType: document.getElementById(config.codeType),
        codeInput: document.getElementById(config.codeInput),
        imageInput: document.getElementById(config.imageInput),
        codeSelection: document.getElementById(config.codeSelection),
        imageSelection: document.getElementById(config.imageSelection),
        noneSelection: document.getElementById(config.noneSelection),
        currentImage: document.getElementById(config.currentImage)
    };
}

function toggleFields(elements) {
    if (elements.codeSelection.checked) {
        toggleDisplay(elements.codeSection, elements.imageSection, 'code');
        setFieldRequirements(elements, false, true, true, false);
    } else if (elements.imageSelection.checked) {
        toggleDisplay(elements.codeSection, elements.imageSection, 'image');
        setFieldRequirements(elements, false, false, false, !elements.currentImage);
    } else {
        toggleDisplay(elements.codeSection, elements.imageSection, 'none');
        setFieldRequirements(elements, true, false, false, false);
    }
}

function toggleDisplay(codeSection, imageSection, display) {
    codeSection.style.display = display === 'code' ? 'block' : 'none';
    imageSection.style.display = display === 'image' ? 'block' : 'none';
}

function setFieldRequirements(elements, reqField, reqCodeType, reqCodeInput, reqImageInput) {
    elements.field.required = reqField;
    elements.codeType.required = reqCodeType;
    elements.codeInput.required = reqCodeInput;
    elements.imageInput.required = reqImageInput;
}

// ======================================================================================================
// Autocomplete Search For Categories
// ======================================================================================================
$(function () {
    $(".search").autocomplete({
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