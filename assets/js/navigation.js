document.querySelectorAll('.nav-works').forEach((nav) => {
  const toggle = nav.querySelector('.works-toggle');
  const menu = nav.querySelector('.works-menu');
  const show = () => {
    menu.hidden = false;
    toggle.setAttribute('aria-expanded', 'true');
  };
  const close = () => {
    nav.classList.remove('is-open');
    menu.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    if (open) show();
    else {
      close();
      toggle.blur();
    }
  });
  nav.addEventListener('mouseenter', show);
  nav.addEventListener('mouseleave', () => {
    if (!nav.classList.contains('is-open') && !nav.contains(document.activeElement)) close();
  });
  nav.addEventListener('focusin', show);
  nav.addEventListener('focusout', (event) => {
    if (!nav.classList.contains('is-open') && !nav.contains(event.relatedTarget)) close();
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
