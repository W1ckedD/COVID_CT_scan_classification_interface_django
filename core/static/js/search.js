const searchContainer = document.querySelector('#search');
const btnSearch = document.querySelector('#btnSearch');

const nameInput = document.querySelector('#name');
const usernameInput = document.querySelector('#username');
const ownerNameInput = document.querySelector('#owner_name');
const posCheckbox = document.querySelector('#pos');
const negCheckbox = document.querySelector('#neg');
const tbdCheckbox = document.querySelector('#tbd');

btnSearch.addEventListener('click', function () {
  searchContainer.classList.toggle('show');
});

const { name, username, owner_name, pos, neg, tbd } = Qs.parse(
  location.search,
  {
    ignoreQueryPrefix: true,
  }
);

function prepopulateInputs() {
  if (name) {
    nameInput.value = name;
  } else {
    nameInput.value = '';
  }
  if (username) {
    usernameInput.value = username;
  } else {
    usernameInput.value = '';
  }
  if (owner_name) {
    ownerNameInput.value = owner_name;
  } else {
    ownerNameInput.value = '';
  }
  if (pos) {
    posCheckbox.checked = true;
  } else {
    posCheckbox.checked = false;
  }
  if (neg) {
    negCheckbox.checked = true;
  } else {
    negCheckbox.checked = false;
  }
  if (tbd) {
    tbdCheckbox.checked = true;
  } else {
    tbdCheckbox.checked = false;
  }
}

window.addEventListener('load', prepopulateInputs);