const deleteForm = document.querySelector('#delete_form');
deleteForm.addEventListener('submit', function (event) {
  event.preventDefault();
  const deleteSample = confirm('آیا از تصمیم خود اطمینان دارید؟');
  if (deleteSample) {
    event.target.submit();
  }
});
