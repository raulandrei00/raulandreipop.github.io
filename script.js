document.addEventListener('DOMContentLoaded', function() {
  const icon = document.querySelector('.menu-icon');
  const menuList = document.getElementById('menu-list');
  icon.addEventListener('click', function(e) {
    menuList.classList.toggle('show');
    e.stopPropagation();
  });
  document.addEventListener('click', function() {
    menuList.classList.remove('show');
  });
});

