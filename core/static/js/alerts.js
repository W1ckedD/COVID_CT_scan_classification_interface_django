const closeBtn = document.querySelector('#message div button.close');

closeBtn.addEventListener('click', function (event) {
  const messageContainer = event.target.parentElement.parentElement.parentElement;
  messageContainer.style.opacity = 0;
});
