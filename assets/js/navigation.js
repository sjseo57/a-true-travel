document.querySelectorAll('.nav-works').forEach((nav) => {
  const toggle = nav.querySelector('.works-toggle');
  const close = () => {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    if (!open) toggle.blur();
  });
  document.addEventListener('pointerdown', (event) => {
    if (!nav.contains(event.target)) close();
  });
  nav.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      close();
      toggle.blur();
    }
  });
});
