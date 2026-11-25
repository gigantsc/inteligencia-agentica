/**
 * Scroll-driven Mouse Swarm orchestrator for all sections below the Hero.
 * Additive by design: pending state is applied only after mouse-swarm loads.
 */
const PENDING_STYLE_ID = 'ms-scroll-pending-style';
const SWARM_COLORS = ['#ff4d00', '#ff9a5c', '#70c9f9', '#c9acff', '#8ee6ce'];

function isDecorativeOrScript(el) {
  if (!el || el.nodeType !== 1 || el.tagName === 'SCRIPT' || el.tagName === 'STYLE') return true;
  const cls = el.className && typeof el.className === 'string' ? el.className : '';
  return /\bpointer-events-none\b/.test(cls) && /\babsolute\b/.test(cls);
}

function roleForElement(el, sectionIdx, isFooter) {
  if (isFooter) return 'Footer';
  const tag = el.tagName;
  const txt = (el.textContent || '').trim();
  if (el.id === 'oferta' || /\bPLANO ANUAL\b|R\$497/.test(txt)) return 'Offer';
  if (/\bDEVOPS\b/i.test(txt)) return 'DevOps';
  if (/\bPROSPEC/i.test(txt)) return 'Sales';
  if (/\bSEO\b/i.test(txt)) return 'SEO';
  if (/\bCMO\b/i.test(txt)) return 'CMO';
  if (/\bBÔNUS\b|\bCINEMAKER\b|\bOMNIVOICE\b/i.test(txt)) return 'Bonus';
  if (tag === 'H2' || (el.querySelector && el.querySelector('h2'))) return 'Brief';
  if (/\bQUERO\b|\bTRAVAR\b/i.test(txt) && txt.length < 140) return 'Growth';
  const bySection = ['Copy', 'Agent', 'Bonus', 'Cases', 'Mentor', 'Offer', 'Pricing', 'FAQ', 'Decision'];
  return bySection[sectionIdx] || 'Agent';
}

function markZoneElement(el, zoneId, order, role, group, effect) {
  el.setAttribute('data-swarm-scroll', zoneId);
  el.setAttribute('data-swarm-order', String(order));
  if (role) el.setAttribute('data-swarm-role', role);
  if (group) el.setAttribute('data-swarm-group', group);
  if (effect) el.setAttribute('data-swarm-effect', effect);
}

function buildZones() {
  const sections = [...document.querySelectorAll('main > section')].slice(1);
  const footer = document.querySelector('footer');
  const containers = [
    ...sections.map((sec, idx) => ({ el: sec, idx, isFooter: false })),
    ...(footer ? [{ el: footer, idx: sections.length, isFooter: true }] : [])
  ];

  const zones = [];
  const createZone = (id) => {
    const z = { id, elements: [], started: false, status: 'pending', reveal: null };
    zones.push(z);
    return z;
  };

  for (const { el, idx, isFooter } of containers) {
    const container = el.querySelector(':scope > div[class*="max-w-"]') || el.firstElementChild;
    if (!container) continue;

    const baseId = isFooter ? 'footer' : `sec${idx + 2}`;
    let defaultZone = null;
    const getDefaultZone = () => defaultZone || (defaultZone = createZone(baseId));

    const directChildren = [...container.children].filter((ch) => !isDecorativeOrScript(ch));

    for (const child of directChildren) {
      const cls = child.className && typeof child.className === 'string' ? child.className : '';
      const isGrid = /\bgrid\b/.test(cls) && child.children.length >= 2;
      const faqItems = child.querySelectorAll(':scope > .faq-item');

      if (isGrid) {
        const cards = [...child.children].filter((c) => !isDecorativeOrScript(c));
        if (cards.length > 3) {
          // Multi-row grids (arsenal/bonuses): split into 3-card row zones
          for (let start = 0, row = 1; start < cards.length; start += 3, row++) {
            const rowCards = cards.slice(start, start + 3);
            const targetZone = row === 1 && defaultZone ? defaultZone : createZone(`${baseId}-row${row}`);
            if (row === 1 && defaultZone) {
              // Rename defaultZone id consistently if header preceded row 1
              targetZone.id = `${baseId}-row1`;
              targetZone.elements.forEach((prevEl) => prevEl.setAttribute('data-swarm-scroll', targetZone.id));
            }
            const grp = `${targetZone.id}-g`;
            rowCards.forEach((card) => {
              const order = targetZone.elements.length + 1;
              markZoneElement(card, targetZone.id, order, roleForElement(card, idx, isFooter), grp, null);
              targetZone.elements.push(card);
            });
          }
          defaultZone = null;
        } else {
          const z = getDefaultZone();
          const useGroup = cards.length === 2;
          const grp = useGroup ? `${z.id}-cmp` : null;
          cards.forEach((card, cIdx) => {
            const order = z.elements.length + 1;
            const isHighlight = useGroup && cIdx === 1;
            markZoneElement(
              card,
              z.id,
              order,
              roleForElement(card, idx, isFooter),
              grp,
              isHighlight ? 'drag' : null
            );
            z.elements.push(card);
          });
        }
      } else if (faqItems.length > 0) {
        const z = getDefaultZone();
        [...faqItems].forEach((item, fIdx) => {
          const order = z.elements.length + 1;
          const grp = `${z.id}-faq${Math.floor(fIdx / 2) + 1}`;
          markZoneElement(item, z.id, order, 'FAQ', grp, null);
          z.elements.push(item);
        });
      } else {
        // Section header, carousel wrapper (.overflow-hidden), featured card, pricing card, CTA, or dots
        const z = getDefaultZone();
        const order = z.elements.length + 1;
        const hasFeaturedCard =
          el.id === 'oferta' ||
          /\bmax-w-\[(560|960)px\]/.test(cls) ||
          /QUERO|TRAVAR/.test(child.textContent || '');
        markZoneElement(
          child,
          z.id,
          order,
          roleForElement(child, idx, isFooter),
          null,
          hasFeaturedCard && order > 1 ? 'drag' : null
        );
        z.elements.push(child);
      }
    }
  }

  return zones.filter((z) => z.elements.length > 0);
}

function injectPendingStyle() {
  if (document.getElementById(PENDING_STYLE_ID)) return;
  const style = document.createElement('style');
  style.id = PENDING_STYLE_ID;
  style.textContent =
    '[data-swarm-pending]{opacity:0;transform:translateY(12px);filter:blur(2px)}';
  document.head.appendChild(style);
}

/**
 * Initializes scroll-triggered cursor swarm animations for all sections below the Hero.
 * @returns {{ zones: Array, getStatus: () => Array<{id: string, count: number, status: string}> }}
 */
export function initScrollSwarm({ createSwarmReveal, narrow = false, track = () => {} } = {}) {
  if (typeof createSwarmReveal !== 'function') {
    throw new TypeError('createSwarmReveal function is required');
  }

  const zones = buildZones();
  if (!zones.length) {
    return { zones: [], getStatus: () => [] };
  }

  injectPendingStyle();

  const clearPending = (zone) => {
    zone.elements.forEach((el) => el.removeAttribute('data-swarm-pending'));
  };

  let observer = null;
  let scrollAttached = false;
  let rafId = 0;

  const cleanupListenersIfDone = () => {
    if (zones.every((z) => z.started)) {
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

  const unobserveZone = (zone) => {
    if (!observer) return;
    observer.unobserve(zone.elements[0]);
    const last = zone.elements[zone.elements.length - 1];
    if (last !== zone.elements[0]) observer.unobserve(last);
  };

  const revealInstant = (zone, reason = 'revealed-instant') => {
    if (zone.started) return;
    zone.started = true;
    zone.status = reason;
    unobserveZone(zone);
    clearPending(zone);
    cleanupListenersIfDone();
  };

  const runZone = (zone) => {
    if (zone.started) return;
    zone.started = true;
    zone.status = 'running';
    unobserveZone(zone);

    const lastRect = zone.elements[zone.elements.length - 1].getBoundingClientRect();
    if (lastRect.bottom < 0) {
      zone.status = 'revealed-instant';
      clearPending(zone);
      cleanupListenersIfDone();
      return;
    }

    try {
      const reveal = createSwarmReveal({
        root: document,
        selector: `[data-swarm-scroll="${zone.id}"]`,
        cursors: narrow ? 7 : 12,
        interval: narrow ? 150 : 170,
        colors: SWARM_COLORS,
        botEvery: 4,
        cursorSize: 15,
        cursorSpeed: 500,
        labels: [],
        selection: true,
        typeText: false,
        autoScroll: false,
        forceMotion: true,
        onComplete: ({ reason, total }) => {
          clearPending(zone);
          zone.status = reason || 'complete';
          track({ swarm_action: reason, swarm_zone: zone.id, swarm_items: total });
          window.setTimeout(() => {
            try {
              reveal.destroy();
            } catch (e) {}
          }, 450);
        },
        onError: (err) => {
          console.warn('[page-swarm] zona interrompida:', zone.id, err);
          clearPending(zone);
          zone.status = 'error';
          window.setTimeout(() => {
            try {
              reveal.destroy();
            } catch (e) {}
          }, 450);
        }
      });

      zone.reveal = reveal;
      reveal.start();
      // Remove pending attribute synchronously after start() applies data-ms-hidden
      clearPending(zone);
      track({ swarm_action: 'start', swarm_zone: zone.id, swarm_items: reveal.getState().total });
    } catch (err) {
      console.warn('[page-swarm] falha ao iniciar zona:', zone.id, err);
      clearPending(zone);
      zone.status = 'error';
    }

    cleanupListenersIfDone();
  };

  const checkPendingZones = () => {
    const vh = window.innerHeight || document.documentElement.clientHeight;
    const atBottom =
      window.scrollY + vh >= document.documentElement.scrollHeight - 40;

    for (const zone of zones) {
      if (zone.started) continue;
      const firstRect = zone.elements[0].getBoundingClientRect();
      const lastRect = zone.elements[zone.elements.length - 1].getBoundingClientRect();

      if (lastRect.bottom <= 0) {
        revealInstant(zone);
      } else if (atBottom || (firstRect.top <= vh * 0.94 && lastRect.bottom > 0)) {
        runZone(zone);
      }
    }
  };

  function scheduleCheck() {
    if (rafId) return;
    rafId = window.requestAnimationFrame(() => {
      rafId = 0;
      checkPendingZones();
    });
  }

  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const zoneId = entry.target.getAttribute('data-swarm-scroll');
          const zone = zones.find((z) => z.id === zoneId);
          if (zone && !zone.started) runZone(zone);
        }
      },
      { rootMargin: '0px 0px -6% 0px', threshold: 0.01 }
    );
  }

  const vh = window.innerHeight || document.documentElement.clientHeight;
  for (const zone of zones) {
    const firstRect = zone.elements[0].getBoundingClientRect();
    const lastRect = zone.elements[zone.elements.length - 1].getBoundingClientRect();

    if (lastRect.bottom <= 0) {
      zone.started = true;
      zone.status = 'skipped-above';
    } else if (firstRect.top < vh * 0.94 && lastRect.bottom > 0) {
      runZone(zone);
    } else {
      zone.elements.forEach((el) => el.setAttribute('data-swarm-pending', ''));
      if (observer) {
        observer.observe(zone.elements[0]);
        const last = zone.elements[zone.elements.length - 1];
        if (last !== zone.elements[0]) observer.observe(last);
      }
    }
  }

  if (zones.some((z) => !z.started)) {
    window.addEventListener('scroll', scheduleCheck, { passive: true });
    window.addEventListener('hashchange', scheduleCheck, { passive: true });
    scrollAttached = true;
  }

  return {
    zones,
    getStatus: () =>
      zones.map((z) => ({
        id: z.id,
        count: z.elements.length,
        status: z.status
      }))
  };
}
