document.addEventListener('DOMContentLoaded', function() {
    const questionsContainer = document.getElementById('questions-container');
    const addQuestionBtn = document.getElementById('add-question-btn');

    let questionIndex = questionsContainer.children.length + 1; // Start from the next index based on existing questions

    addQuestionBtn.addEventListener('click', function() {
        const questionHTML = `
            <div class="question-form border p-3 mb-3" id="question-form-${questionIndex}">
                <div class="d-flex align-items-center mb-2">
                    <div class="flex-grow-1">
                        <label for="question_${questionIndex}" class="form-label">Question ${questionIndex}</label>
                        <input type="text" class="form-control" id="question_${questionIndex}" name="questions[${questionIndex}][question]" required>
                    </div>
                    <button type="button" class="btn btn-danger btn-sm remove-question-btn ms-2">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
                <div class="mb-3">
                    <label for="option1_${questionIndex}" class="form-label">Option 1</label>
                    <input type="text" class="form-control" id="option1_${questionIndex}" name="questions[${questionIndex}][option1]" required>
                </div>
                <div class="mb-3">
                    <label for="option2_${questionIndex}" class="form-label">Option 2</label>
                    <input type="text" class="form-control" id="option2_${questionIndex}" name="questions[${questionIndex}][option2]" required>
                </div>
                <div class="mb-3">
                    <label for="option3_${questionIndex}" class="form-label">Option 3</label>
                    <input type="text" class="form-control" id="option3_${questionIndex}" name="questions[${questionIndex}][option3]" required>
                </div>
            </div>
        `;
        questionsContainer.insertAdjacentHTML('beforeend', questionHTML);

        // Add functionality to remove the question
        const removeBtn = questionsContainer.querySelector(`#question-form-${questionIndex} .remove-question-btn`);
        removeBtn.addEventListener('click', function() {
            this.closest('.question-form').remove();
        });

        questionIndex++; // Increment index for the next question
    });

    // Add functionality for existing questions to enable removal
    document.querySelectorAll('.remove-question-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            this.closest('.question-form').remove();
        });
    });
});
