/**
 * Kinetic scroll-reveal choreography for all sections below the Hero.
 * 100% additive: nothing is hidden by static CSS before this module loads.
 */
const FX_STYLE_ID = 'ia-scroll-fx-style';

const FX_CSS = `
html, body { overflow-x: clip; }
[data-ia-fx][data-fx-state="wait"] {
  opacity: 0 !important;
  will-change: transform, opacity, filter;
}
[data-ia-fx="fade-up"][data-fx-state="wait"] {
  transform: translate3d(0, 34px, 0) !important;
  filter: blur(5px) !important;
}
[data-ia-fx="from-left"][data-fx-state="wait"] {
  transform: translate3d(-48px, 0, 0) rotate(-0.8deg) !important;
  filter: blur(4px) !important;
}
[data-ia-fx="from-right"][data-fx-state="wait"] {
  transform: translate3d(48px, 0, 0) rotate(0.8deg) !important;
  filter: blur(4px) !important;
}
[data-ia-fx="zoom-in"][data-fx-state="wait"] {
  transform: translate3d(0, 22px, 0) scale(0.9) !important;
  filter: blur(4px) !important;
}
[data-ia-fx="shake-pop"][data-fx-state="wait"] {
  transform: translate3d(0, 18px, 0) scale(0.94) !important;
  filter: blur(4px) !important;
}

[data-ia-fx="fade-up"][data-fx-state="shown"] {
  opacity: 1 !important;
  transform: none !important;
  filter: blur(0) !important;
  transition:
    opacity 720ms cubic-bezier(0.22, 1, 0.36, 1) var(--ia-fx-delay, 0ms),
    transform 720ms cubic-bezier(0.22, 1, 0.36, 1) var(--ia-fx-delay, 0ms),
    filter 720ms cubic-bezier(0.22, 1, 0.36, 1) var(--ia-fx-delay, 0ms) !important;
}
[data-ia-fx="from-left"][data-fx-state="shown"],
[data-ia-fx="from-right"][data-fx-state="shown"] {
  opacity: 1 !important;
  transform: none !important;
  filter: blur(0) !important;
  transition:
    opacity 760ms cubic-bezier(0.22, 1, 0.36, 1) var(--ia-fx-delay, 0ms),
    transform 760ms cubic-bezier(0.22, 1, 0.36, 1) var(--ia-fx-delay, 0ms),
    filter 760ms cubic-bezier(0.22, 1, 0.36, 1) var(--ia-fx-delay, 0ms) !important;
}
[data-ia-fx="zoom-in"][data-fx-state="shown"] {
  opacity: 1 !important;
  transform: none !important;
  filter: blur(0) !important;
  transition:
    opacity 700ms cubic-bezier(0.16, 1, 0.3, 1) var(--ia-fx-delay, 0ms),
    transform 700ms cubic-bezier(0.16, 1, 0.3, 1) var(--ia-fx-delay, 0ms),
    filter 700ms cubic-bezier(0.16, 1, 0.3, 1) var(--ia-fx-delay, 0ms) !important;
}
[data-ia-fx="shake-pop"][data-fx-state="shown"] {
  animation: ia-fx-shake-pop 860ms cubic-bezier(0.22, 1, 0.36, 1) var(--ia-fx-delay, 0ms) both;
}
@keyframes ia-fx-shake-pop {
  0%   { opacity: 0; transform: translate3d(0, 18px, 0) scale(0.94); filter: blur(4px); }
  58%  { opacity: 1; transform: translate3d(0, -2px, 0) scale(1.02); filter: blur(0); }
  70%  { opacity: 1; transform: translate3d(-3px, 0, 0) rotate(-1.2deg); filter: blur(0); }
  80%  { opacity: 1; transform: translate3d(3px, 0, 0) rotate(1deg); filter: blur(0); }
  90%  { opacity: 1; transform: translate3d(-1px, 0, 0) rotate(-0.5deg); filter: blur(0); }
  100% { opacity: 1; transform: none; filter: none; }
}
`;

function isDecorativeOrScript(el) {
  if (!el || el.nodeType !== 1 || el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return true;
  const cls = el.className && typeof el.className === 'string' ? el.className : '';
  return /\bpointer-events-none\b/.test(cls) && /\babsolute\b/.test(cls);
}

function injectFxStyle() {
  if (document.getElementById(FX_STYLE_ID)) return;
  const style = document.createElement('style');
  style.id = FX_STYLE_ID;
  style.textContent = FX_CSS;
  document.head.appendChild(style);
}

function collectTargets() {
  const sections = [...document.querySelectorAll('main > section')].slice(1);
  const footer = document.querySelector('footer');
  const containers = [
    ...sections.map((sec) => ({ el: sec, isFooter: false })),
    ...(footer ? [{ el: footer, isFooter: true }] : [])
  ];

  const items = [];
  const register = (el, fx, delayMs = 0) => {
    el.setAttribute('data-ia-fx', fx);
    if (delayMs > 0) {
      el.style.setProperty('--ia-fx-delay', `${delayMs}ms`);
    }
    items.push({ el, fx, delayMs, state: 'init' });
  };

  for (const { el, isFooter } of containers) {
    const container = el.querySelector(':scope > div[class*="max-w-"]') || el.firstElementChild;
    if (!container) continue;

    const children = [...container.children].filter((ch) => !isDecorativeOrScript(ch));

    for (const child of children) {
      const cls = child.className && typeof child.className === 'string' ? child.className : '';
      const isGrid = /\bgrid\b/.test(cls) && child.children.length >= 2;
      const faqItems = child.querySelectorAll(':scope > .faq-item');

      if (isGrid) {
        const cards = [...child.children].filter((c) => !isDecorativeOrScript(c));
        if (cards.length === 2) {
          register(cards[0], 'from-left', 80);
          register(cards[1], 'from-right', 200);
          const innerCta = cards[1].querySelector('a[href="#oferta"]');
          if (innerCta) register(innerCta, 'shake-pop', 360);
        } else {
          // 3-column or multi-row grids: left / center-up / right per row
          const colFx = ['from-left', 'fade-up', 'from-right'];
          cards.forEach((card, idx) => {
            const col = idx % 3;
            register(card, colFx[col], col * 120);
          });
        }
      } else if (faqItems.length > 0) {
        [...faqItems].forEach((item, idx) => {
          register(item, idx % 2 === 0 ? 'from-left' : 'from-right', (idx % 2) * 80);
        });
      } else if (el.id === 'oferta') {
        if (/\bmax-w-\[560px\]/.test(cls)) {
          register(child, 'shake-pop', 120);
        } else if (child.classList.contains('text-center') && child.querySelector('h2')) {
          register(child, 'fade-up', 0);
        } else {
          register(child, 'fade-up', 220);
        }
      } else if (child.classList.contains('overflow-hidden') && child.querySelector('#testimonialTrack')) {
        // Target outer overflow-hidden wrapper with unscaled fade-up so #testimonialTrack width stays exact
        register(child, 'fade-up', 80);
      } else if (/\bmax-w-\[960px\]/.test(container.className || '') || child.querySelector('.border-\\[var\\(--orange\\)\\]')) {
        register(child, 'zoom-in', 100);
      } else if (
        !isFooter &&
        (/Prompts são para amadores/i.test(child.textContent || '') ||
          (/QUERO MEUS FUNCIONÁRIOS/i.test(child.textContent || '') && !child.querySelector('h2')))
      ) {
        register(child, 'shake-pop', 140);
      } else {
        register(child, 'fade-up', 0);
      }
    }
  }

  return items;
}

/**
 * Initializes kinetic scroll-entrance animations for all sections below the Hero.
 * @returns {{ items: Array, getSummary: () => { total: number, shown: number, waiting: number, byFx: Record<string, number> } }}
 */
export function initScrollChoreography() {
  injectFxStyle();
  const items = collectTargets();
  if (!items.length) {
    return {
      items: [],
      getSummary: () => ({ total: 0, shown: 0, waiting: 0, byFx: {} })
    };
  }

  let observer = null;
  let scrollAttached = false;
  let rafId = 0;

  const cleanupIfDone = () => {
    if (items.every((item) => item.state !== 'wait' && item.state !== 'init')) {
      if (observer) {
        observer.disconnect();
        observer = null;
      }
      if (scrollAttached) {
        window.removeEventListener('scroll', scheduleCheck);
        window.removeEventListener('hashchange', scheduleCheck);
        scrollAttached = false;
      }
    }
  };

  const revealItem = (item, instant = false) => {
    if (item.state !== 'wait' && item.state !== 'init') return;
    if (observer) observer.unobserve(item.el);

    if (instant) {
      item.state = 'settled';
      item.el.setAttribute('data-fx-state', 'settled');
    } else {
      item.state = 'shown';
      // Force layout read when transitioning from wait -> shown so CSS transition fires reliably
      void item.el.offsetWidth;
      item.el.setAttribute('data-fx-state', 'shown');
      const settleMs = item.delayMs + (item.fx === 'shake-pop' ? 920 : 820);
      window.setTimeout(() => {
        if (item.el.getAttribute('data-fx-state') === 'shown') {
          item.state = 'settled';
          item.el.setAttribute('data-fx-state', 'settled');
        }
      }, settleMs);
    }

    cleanupIfDone();
  };

  const checkPending = () => {
    const vh = window.innerHeight || document.documentElement.clientHeight;
    const atBottom =
      window.scrollY + vh >= document.documentElement.scrollHeight - 40;

    for (const item of items) {
      if (item.state !== 'wait') continue;
      const rect = item.el.getBoundingClientRect();
      if (rect.bottom <= 0) {
        revealItem(item, true);
      } else if (atBottom || (rect.top <= vh * 0.98 && rect.bottom > 0)) {
        revealItem(item, false);
      }
    }
  };

  function scheduleCheck() {
    if (rafId) return;
    rafId = window.requestAnimationFrame(() => {
      rafId = 0;
      checkPending();
    });
  }

  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const match = items.find((i) => i.el === entry.target);
          if (match && match.state === 'wait') {
            revealItem(match, false);
          }
        }
      },
      { rootMargin: '0px 0px -2% 0px', threshold: 0.04 }
    );
  }

  const vh = window.innerHeight || document.documentElement.clientHeight;
  const atBottom =
    window.scrollY + vh >= document.documentElement.scrollHeight - 40;
  const initialReveal = [];

  for (const item of items) {
    const rect = item.el.getBoundingClientRect();
    if (rect.bottom <= 0) {
      item.state = 'settled';
      item.el.setAttribute('data-fx-state', 'settled');
    } else if (atBottom || (rect.top < vh * 0.98 && rect.bottom > 0)) {
      item.state = 'wait';
      item.el.setAttribute('data-fx-state', 'wait');
      initialReveal.push(item);
    } else {
      item.state = 'wait';
      item.el.setAttribute('data-fx-state', 'wait');
      if (observer) observer.observe(item.el);
    }
  }

  initialReveal.forEach((item) => revealItem(item, false));

  if (items.some((item) => item.state === 'wait')) {
    window.addEventListener('scroll', scheduleCheck, { passive: true });
    window.addEventListener('hashchange', scheduleCheck, { passive: true });
    scrollAttached = true;
  }

  return {
    items,
    getSummary: () => {
      const byFx = {};
      let shown = 0;
      let waiting = 0;
      for (const item of items) {
        byFx[item.fx] = (byFx[item.fx] || 0) + 1;
        if (item.state === 'wait') waiting++;
        else shown++;
      }
      return { total: items.length, shown, waiting, byFx };
    }
  };
}
