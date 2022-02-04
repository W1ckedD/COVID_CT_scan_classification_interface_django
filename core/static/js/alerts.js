const closeBtn = document.querySelector('#message div button.close');
const messageContainer = document.querySelector('#message');
closeBtn.addEventListener('click', function (event) {
  messageContainer.style.opacity = 0;
});

// setTimeout(() => {
//   messageContainer.style.opacity = 0;
// }, 5000);
