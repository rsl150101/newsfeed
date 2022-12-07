const modal = document.querySelector(".modal");
const questionAdd = document.querySelector(".question-add");
const questionSubmit = document.querySelector(
  ".question-add-form input[type=submit]"
);
const questionCancel = document.querySelector(
  ".question-add-form input[type='button']"
);

const handleQuestionAdd = () => {
  modal.classList.toggle("show");
};

questionAdd.addEventListener("click", handleQuestionAdd);
questionCancel.addEventListener("click", handleQuestionAdd);
