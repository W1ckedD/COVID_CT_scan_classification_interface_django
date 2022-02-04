const searchContainer = document.querySelector('#search');

const btnSearch = document.querySelector('#btnSearch');

btnSearch.addEventListener('click', function () {
  searchContainer.classList.toggle('show');
});
