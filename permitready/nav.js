/* PermitReady — mobile hamburger nav injection */
(function () {
    function init() {
        var nav = document.querySelector('.nav-container');
        if (!nav) return;
        if (nav.querySelector('.nav-toggle')) return; // already injected (index.html)

        var btn = document.createElement('button');
        btn.className = 'nav-toggle';
        btn.setAttribute('aria-label', 'Open menu');
        btn.setAttribute('aria-expanded', 'false');
        btn.innerHTML = '<span></span><span></span><span></span>';

        var links = nav.querySelector('.nav-links');
        if (!links) return;
        nav.insertBefore(btn, links);

        btn.addEventListener('click', function () {
            var open = links.classList.toggle('nav-open');
            btn.classList.toggle('nav-toggle--open', open);
            btn.setAttribute('aria-expanded', String(open));
            btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
        });

        links.addEventListener('click', function (e) {
            if (e.target.tagName === 'A') {
                links.classList.remove('nav-open');
                btn.classList.remove('nav-toggle--open');
                btn.setAttribute('aria-expanded', 'false');
                btn.setAttribute('aria-label', 'Open menu');
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
