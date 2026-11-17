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
