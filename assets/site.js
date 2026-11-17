// Core navigation and page content work without JavaScript.
// On the homepage, indicate when the selected-work anchor is active.
const projectLink = document.querySelector('nav a[href="./index.html#projects"]');
if (projectLink && /(?:\/|\/index\.html)$/.test(location.pathname)) {
  const update = () => {
    if (location.hash === '#projects') projectLink.setAttribute('aria-current', 'location');
    else projectLink.removeAttribute('aria-current');
  };
  addEventListener('hashchange', update);
  update();
}

const fileSearch = document.querySelector('[data-file-search]');
if (fileSearch) {
  const files = [...document.querySelectorAll('[data-repo-file]')];
  const count = document.querySelector('[data-file-count]');
  fileSearch.addEventListener('input', () => {
    const query = fileSearch.value.trim().toLowerCase();
    let visible = 0;
    files.forEach(file => {
      file.hidden = !file.querySelector('a').textContent.toLowerCase().includes(query);
      if (!file.hidden) visible += 1;
    });
    count.textContent = `${visible} of ${files.length} files`;
  });
}

const motionToggle = document.querySelector('[data-motion-toggle]');
if (motionToggle) {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let enabled = true;
  try { enabled = localStorage.getItem('portfolio-motion') !== 'off'; } catch (_) { /* Storage is optional. */ }
  const updateMotion = () => {
    const active = enabled && !reduceMotion.matches;
    document.body.classList.toggle('matrix-off', !active);
    motionToggle.setAttribute('aria-pressed', String(active));
    motionToggle.textContent = reduceMotion.matches ? '[ motion: reduced ]' : `[ motion: ${active ? 'on' : 'off'} ]`;
    motionToggle.disabled = reduceMotion.matches;
  };
  motionToggle.hidden = false;
  motionToggle.addEventListener('click', () => {
    enabled = !enabled;
    try { localStorage.setItem('portfolio-motion', enabled ? 'on' : 'off'); } catch (_) { /* Storage is optional. */ }
    updateMotion();
  });
  reduceMotion.addEventListener('change', updateMotion);
  updateMotion();
}

const printResume = document.querySelector('[data-print-resume]');
if (printResume) {
  printResume.hidden = false;
  printResume.addEventListener('click', () => window.print());
}
