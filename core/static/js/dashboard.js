const validation_term = document.querySelector('#validation_term');
const validation_input = document.querySelector('#validation');
const deleteAccountButton = document.querySelector('#btn_delete_account');
const deleteAccountForm = document.querySelector('#form_delete_account');

validation_input.addEventListener('input', function (event) {
  if (event.target.value === validation_term.value) {
    deleteAccountButton.disabled = false;
  } else {
    deleteAccountButton.disabled = true;
  }
});

deleteAccountForm.addEventListener('submit', function (event) {
  event.preventDefault();

  const deleteAccount = confirm(
    'با ادامه این فعالیت داده های شما از سرور پاک خواهد شد، آیا از تصمیم خود اطمینان دارید؟'
  );
  if (deleteAccount) {
    deleteAccountForm.submit();
  }
});
