const navbarToggler = document.querySelector('#navbar-toggler');
const sidebar = document.querySelector('#sidebar');
navbarToggler.addEventListener('click', function () {
  sidebar.classList.toggle('sidebar-open');
});
