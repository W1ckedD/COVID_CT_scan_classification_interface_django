const publicCheckBox = document.getElementById('public-checkbox');
const usersCheckBox = document.getElementById('users-checkbox');

publicCheckBox.addEventListener('change', function(event) {
  if (event.target.checked) {
    usersCheckBox.checked = true;
    usersCheckBox.disabled = true;
  } else {
    usersCheckBox.disabled = false;
  }
})