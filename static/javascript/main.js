document.addEventListener('DOMContentLoaded', function() {
    const questionsContainer = document.getElementById('questions-container');
    const addQuestionBtn = document.getElementById('add-question-btn');

    let questionIndex = 1; // Start from 1 because one form is already there

    addQuestionBtn.addEventListener('click', function() {
        questionIndex++;
        const questionHTML = `
            <div class="question-form">
                <div class="mb-3">
                    <label for="question_${questionIndex}" class="form-label">Question ${questionIndex}</label>
                    <input type="text" class="form-control" id="question_${questionIndex}" name="questions[${questionIndex}][question]">
                </div>
                <div class="mb-3">
                    <label for="option1_${questionIndex}" class="form-label">Option 1</label>
                    <input type="text" class="form-control" id="option1_${questionIndex}" name="questions[${questionIndex}][option1]">
                </div>
                <div class="mb-3">
                    <label for="option2_${questionIndex}" class="form-label">Option 2</label>
                    <input type="text" class="form-control" id="option2_${questionIndex}" name="questions[${questionIndex}][option2]">
                </div>
                <div class="mb-3">
                    <label for="option3_${questionIndex}" class="form-label">Option 3</label>
                    <input type="text" class="form-control" id="option3_${questionIndex}" name="questions[${questionIndex}][option3]">
                </div>
            </div>
        `;
        questionsContainer.insertAdjacentHTML('beforeend', questionHTML);
    });
});
