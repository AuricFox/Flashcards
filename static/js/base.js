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
    // Text area inputs
    const questionField = document.getElementById('question');
    const answerField = document.getElementById('answer');

    // Question Elements
    const qCodeSection = document.getElementById('q-code-section');
    const qImageSection = document.getElementById('q-image-section');
    const qCodeType = document.getElementById('q-code-sel');
    const qCodeInput = document.getElementById('q-code-figure');
    const qImageInput = document.getElementById('q-image-figure');
    const qCodeSelection = document.getElementById('q-code-selection');
    const qImageSelection = document.getElementById('q-image-selection');
    const qNone = document.getElementById('q-none-type');
    const qCurrentImage = document.getElementById('q-card-image');

    // Answer Elements
    const aCodeSection = document.getElementById('a-code-section');
    const aImageSection = document.getElementById('a-image-section');
    const aCodeType = document.getElementById('a-code-sel');
    const aCodeInput = document.getElementById('a-code-figure');
    const aImageInput = document.getElementById('a-image-figure');
    const aCodeSelection = document.getElementById('a-code-selection');
    const aImageSelection = document.getElementById('a-image-selection');
    const aNone = document.getElementById('a-none-type');
    const aCurrentImage = document.getElementById('a-card-image');

    // Add click event listener for question slection
    if (qCodeSelection && qImageSelection) {
        qCodeSelection.addEventListener('click', function () {
            toggleFields(qCodeSelection, qImageSelection, qCodeSection, qImageSection, questionField, qCodeType, qCodeInput, qImageInput, qCurrentImage);
        });

        qImageSelection.addEventListener('click', function () {
            toggleFields(qCodeSelection, qImageSelection, qCodeSection, qImageSection, questionField, qCodeType, qCodeInput, qImageInput, qCurrentImage);
        });

        qNone.addEventListener('click', function () {
            toggleFields(qCodeSelection, qImageSelection, qCodeSection, qImageSection, questionField, qCodeType, qCodeInput, qImageInput, qCurrentImage);
        });
    }

    // Add click event listeners for answer selection
    if (aCodeSelection && aImageSelection) {
        aCodeSelection.addEventListener('click', function () {
            toggleFields(aCodeSelection, aImageSelection, aCodeSection, aImageSection, answerField, aCodeType, aCodeInput, aImageInput, aCurrentImage);
        });

        aImageSelection.addEventListener('click', function () {
            toggleFields(aCodeSelection, aImageSelection, aCodeSection, aImageSection, answerField, aCodeType, aCodeInput, aImageInput, aCurrentImage);
        });

        aNone.addEventListener('click', function () {
            toggleFields(aCodeSelection, aImageSelection, aCodeSection, aImageSection, answerField, aCodeType, aCodeInput, aImageInput, aCurrentImage);
        });
    }
});

function toggleFields(codeSelection, imageSelection, codeSection, imageSection, field, codeType, codeInput, imageInput, currentImage) {
    if (codeSelection && imageSelection) {

        // User wants code elements
        if (codeSelection.checked) {
            toggleDisplay(codeSection, imageSection, 'code');
            setFieldRequirements(field, codeType, codeInput, imageInput, false, true, true, false);
        
        // User wants image elements
        } else if (imageSelection.checked) {
            toggleDisplay(codeSection, imageSection, 'image');
            setFieldRequirements(field, codeType, codeInput, imageInput, false, false, false, currentImage === null);
        
        // User wants no additional elements
        } else {
            toggleDisplay(codeSection, imageSection, 'none');
            setFieldRequirements(field, codeType, codeInput, imageInput, true, false, false, false);
        }
    }
}

function toggleDisplay(codeSection, imageSection, display) {
    // Toggle the display of the code and image inputs
    codeSection.style.display = display == 'code' ? 'block' : 'none';
    imageSection.style.display = display == 'image' ? 'block' : 'none';
}

function setFieldRequirements(field, codeType, codeInput, imageInput, reqField, reqCodeType, reqCodeInput, reqImageInput) {
    // Set what fields are required by the user when toggled

    field.required = reqField;              // Require question and/or answer fields
    codeType.required = reqCodeType;        // Require code type input
    codeInput.required = reqCodeInput;      // Require code block input
    imageInput.required = reqImageInput;    // Require image input
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