document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('.navbar a');
  const current = window.location.pathname.split('/').pop();
  links.forEach(link => {
    if (!link.getAttribute('href')) return;
    if (link.getAttribute('href') === current || (current === '' && link.getAttribute('href') === 'index.html')) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
});
