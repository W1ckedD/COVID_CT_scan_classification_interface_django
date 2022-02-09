const logSearchContainer = document.querySelector('#logSearch');
const btnLogSearch = document.querySelector('#btnLogSearch');

const logUsernameInput = document.querySelector('#log_username');
const logStartDateInput = document.querySelector('#log_start_date');
const logEndDateInput = document.querySelector('#log_end_date');
const successCheckbox = document.querySelector('#success');
const failureCheckbox = document.querySelector('#failure');
const AUTHCheckbox = document.querySelector('#AUTH');
const READCheckbox = document.querySelector('#READ');
const CREATECheckbox = document.querySelector('#CREATE');
const UPDATECheckbox = document.querySelector('#UPDATE');
const DELETECheckbox = document.querySelector('#DELETE');
const PREDICTCheckbox = document.querySelector('#PREDICT');

btnLogSearch.addEventListener('click', function () {
  logSearchContainer.classList.toggle('show');
});

const {
  log_username,
  success,
  failure,
  AUTH,
  READ,
  CREATE,
  UPDATE,
  DELETE,
  PREDICT,
  start_date,
  end_date,
} = Qs.parse(location.search, {
  ignoreQueryPrefix: true,
});

function prepopulateInputs() {
  if (log_username) {
    logUsernameInput.value = log_username;
  } else {
    logUsernameInput.value = '';
  }
  if (start_date) {
    logStartDateInput.value = start_date;
  } else {
    logStartDateInput.value = '';
  }
  if (end_date) {
    logEndDateInput.value = end_date;
  } else {
    logEndDateInput.value = '';
  }
  if (success) {
    successCheckbox.checked = true;
  } else {
    successCheckbox.checked = false;
  }
  if (failure) {
    failureCheckbox.checked = true;
  } else {
    failureCheckbox.checked = false;
  }
  if (AUTH) {
    AUTHCheckbox.checked = true;
  } else {
    AUTHCheckbox.checked = false;
  }
  if (READ) {
    READCheckbox.checked = true;
  } else {
    READCheckbox.checked = false;
  }
  if (CREATE) {
    CREATECheckbox.checked = true;
  } else {
    CREATECheckbox.checked = false;
  }
  if (UPDATE) {
    UPDATECheckbox.checked = true;
  } else {
    UPDATECheckbox.checked = false;
  }
  if (DELETE) {
    DELETECheckbox.checked = true;
  } else {
    DELETECheckbox.checked = false;
  }
  if (PREDICT) {
    PREDICTCheckbox.checked = true;
  } else {
    PREDICTCheckbox.checked = false;
  }
}

window.addEventListener('load', prepopulateInputs);
