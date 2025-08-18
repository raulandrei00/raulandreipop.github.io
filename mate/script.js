document.addEventListener('DOMContentLoaded', function() {
  const cta = document.getElementById('call-to-action');
  if (cta) {
    cta.addEventListener('click', function() {
      window.location.href = "mailto:raul.pop@example.com?subject=Înscriere curs demonstrativ";
    });
    cta.style.cursor = "pointer";
    cta.setAttribute('title', 'Trimite un email pentru înscriere!');
  }
});