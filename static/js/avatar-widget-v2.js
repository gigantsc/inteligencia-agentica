/**
 * Interactive falling-from-ceiling Avatar widget v2 (Hermes Assistant).
 * Features:
 * - LGPD consent checkbox in the Nome + E-mail lead form
 * - Mobile walking mode seated flush on top of the fixed mobile CTA bar
 * - Compact attention-grabbing mini callout pill on mobile (big bubble closed)
 */
const STYLE_ID = 'ia-avatar-style';
const ROOT_ID = 'iaAvatarRoot';

const DEFAULT_CONFIG = {
  basePath: '/static/images/avatar/',
  channelUrl: 'https://chat.whatsapp.com/HcdMbPrvi0O3jmd62vmB5n',
  channelLabel: 'Participar do Canal',
  whatsappNumber: '5547984331647',
  enableListmonk: true,
  listmonkEndpoint: '/api/subscription',
  listmonkListUuid: '7b9cdf5f-ee62-45cf-98ce-4b1753c8554c',
};

const CRITICAL_FRAMES = [
  'fall-drop.webp',
  'fall-land.webp',
  'fall-getup.webp',
  'fall-dizzy.webp',
  'wave-1.webp',
  'wave-2.webp',
  'wave-3.webp',
  'breathe-0.webp',
];

const WALK_FRAMES = [
  ...Array.from({ length: 8 }, (_, i) => `walk-left-${i}.webp`),
  ...Array.from({ length: 8 }, (_, i) => `walk-right-${i}.webp`),
];

const EXTRA_FRAMES = [
  'blink.webp',
  ...Array.from({ length: 8 }, (_, i) => `breathe-${i}.webp`),
  ...Array.from({ length: 8 }, (_, i) => `talk-${i}.webp`),
  ...Array.from({ length: 6 }, (_, i) => `approve-${i}.webp`),
  ...WALK_FRAMES,
];

const DESKTOP_MESSAGES = [
  'Opa, cheguei! 👋 Quer receber bastidores, automações e novidades no nosso canal oficial?',
  'Ficou com dúvida sobre os agentes ou quer ajuda para escolher? Clica em mim que te conecto no WhatsApp!',
];

const MINI_CALLOUTS = [
  'Oi! 👋',
  'Precisa de ajuda?',
  'Clique aqui! ✨',
  'Entrar no canal 🚀',
];

const WIDGET_CSS = `
#${ROOT_ID} {
  position: fixed;
  right: 20px;
  bottom: 18px;
  z-index: 45;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
  pointer-events: none;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}
#${ROOT_ID} * { box-sizing: border-box; }
#iaAvatarBubble, #iaAvatarFormModal, #iaAvatarSpriteWrap, #iaAvatarRestore, #iaAvatarMiniCallout {
  pointer-events: auto;
}
#iaAvatarBubble[hidden],
#iaAvatarFormModal[hidden],
#iaAvatarRestore[hidden],
#iaAvatarMiniCallout[hidden],
#iaAvatarSpriteWrap[hidden] {
  display: none !important;
}
#iaAvatarBubble {
  position: relative;
  width: 304px;
  max-width: calc(100vw - 24px);
  padding: 13px 15px 14px;
  border-radius: 16px;
  background: rgba(14, 14, 20, 0.94);
  -webkit-backdrop-filter: blur(16px);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 77, 0, 0.45);
  box-shadow: 0 18px 42px rgba(0, 0, 0, 0.65), 0 0 24px rgba(255, 77, 0, 0.14);
  color: #f3f4f6;
  font-size: 13px;
  line-height: 1.45;
  transform-origin: bottom right;
  animation: ia-av-pop 280ms cubic-bezier(0.22, 1, 0.36, 1) both;
}
#iaAvatarBubble::after {
  content: '';
  position: absolute;
  right: 46px;
  bottom: -7px;
  width: 12px;
  height: 12px;
  background: rgba(14, 14, 20, 0.94);
  border-right: 1px solid rgba(255, 77, 0, 0.45);
  border-bottom: 1px solid rgba(255, 77, 0, 0.45);
  transform: rotate(45deg);
}
.ia-av-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 6px;
}
.ia-av-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #ff7a3d;
}
.ia-av-dot {
  width: 6px;
  height: 6px;
  border-radius: 999px;
  background: #22c55e;
  box-shadow: 0 0 8px #22c55e;
}
.ia-av-close {
  width: 22px;
  height: 22px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.06);
  color: #9ca3af;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: color 150ms, border-color 150ms, background 150ms;
}
.ia-av-close:hover {
  color: #fff;
  border-color: rgba(255, 77, 0, 0.6);
  background: rgba(255, 77, 0, 0.16);
}
#iaAvatarBubbleText {
  margin: 0 0 11px 0;
  color: #e5e7eb;
}
.ia-av-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.ia-av-btn-primary, .ia-av-btn-secondary {
  flex: 1 1 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 11px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  text-decoration: none;
  cursor: pointer;
  transition: filter 160ms, transform 160ms, border-color 160ms;
}
.ia-av-btn-primary {
  background: #ff4d00;
  color: #ffffff;
  border: 1px solid #ff4d00;
}
.ia-av-btn-primary:hover { filter: brightness(1.1); transform: translateY(-1px); }
.ia-av-btn-secondary {
  background: rgba(255, 255, 255, 0.06);
  color: #f3f4f6;
  border: 1px solid rgba(255, 255, 255, 0.16);
}
.ia-av-btn-secondary:hover {
  border-color: rgba(255, 77, 0, 0.6);
  background: rgba(255, 77, 0, 0.12);
}

#iaAvatarMiniCallout {
  position: fixed;
  left: 0;
  bottom: calc(var(--ia-av-ground, 69px) + 104px);
  z-index: 46;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(14, 14, 20, 0.96);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  border: 1.5px solid rgba(255, 77, 0, 0.82);
  box-shadow: 0 10px 26px rgba(0, 0, 0, 0.65), 0 0 16px rgba(255, 77, 0, 0.28);
  color: #ffffff;
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
  cursor: pointer;
  transform: translate3d(var(--ia-mc-x, 0px), 0, 0);
  animation: ia-av-glow 2.2s ease-in-out infinite;
}
#iaAvatarMiniCallout .ia-av-dot {
  flex-shrink: 0;
  animation: ia-av-pulse 1.4s ease-in-out infinite;
}

#iaAvatarFormModal {
  width: 336px;
  max-width: calc(100vw - 24px);
  padding: 16px;
  border-radius: 18px;
  background: rgba(12, 12, 18, 0.97);
  -webkit-backdrop-filter: blur(18px);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 77, 0, 0.55);
  box-shadow: 0 24px 56px rgba(0, 0, 0, 0.78), 0 0 28px rgba(255, 77, 0, 0.18);
  color: #f3f4f6;
  animation: ia-av-pop 240ms cubic-bezier(0.22, 1, 0.36, 1) both;
}
#iaAvatarFormModal h4 {
  margin: 0 0 4px 0;
  font-size: 15px;
  font-weight: 800;
  color: #ffffff;
}
.ia-av-sub {
  margin: 0 0 12px 0;
  font-size: 12px;
  line-height: 1.4;
  color: #9ca3af;
}
.ia-av-field {
  margin-bottom: 10px;
}
.ia-av-field label {
  display: block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #d1d5db;
  margin-bottom: 4px;
}
.ia-av-field input {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.05);
  color: #ffffff;
  font-size: 13px;
  outline: none;
  transition: border-color 150ms, background 150ms;
}
.ia-av-field input:focus {
  border-color: #ff4d00;
  background: rgba(255, 255, 255, 0.08);
}
.ia-av-lgpd {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 4px 0 11px 0;
  font-size: 11.5px;
  line-height: 1.38;
  color: #cbd5e1;
  cursor: pointer;
}
.ia-av-lgpd input[type="checkbox"] {
  width: 16px;
  height: 16px;
  margin: 1px 0 0 0;
  accent-color: #ff4d00;
  flex-shrink: 0;
  cursor: pointer;
}
#iaAvatarFormError {
  margin: 0 0 10px 0;
  font-size: 12px;
  color: #fca5a5;
  background: rgba(239, 68, 68, 0.14);
  border: 1px solid rgba(239, 68, 68, 0.35);
  border-radius: 8px;
  padding: 7px 10px;
}
#iaAvatarFormError[hidden], #iaAvatarSuccessBox[hidden] { display: none !important; }
#iaAvatarSubmit {
  width: 100%;
  height: 42px;
  border-radius: 11px;
  border: 0;
  background: linear-gradient(135deg, #25d366 0%, #16a34a 100%);
  color: #052e16;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  transition: filter 160ms, transform 160ms;
}
#iaAvatarSubmit:hover { filter: brightness(1.06); transform: translateY(-1px); }
.ia-av-modal-channel {
  display: block;
  margin-top: 10px;
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  color: #ff9a5c;
  text-decoration: none;
}
.ia-av-modal-channel:hover { text-decoration: underline; }
#iaAvatarSuccessBox {
  padding: 10px 12px;
  border-radius: 12px;
  background: rgba(34, 197, 94, 0.12);
  border: 1px solid rgba(34, 197, 94, 0.35);
  font-size: 12.5px;
  color: #dcfce7;
}
#iaAvatarDirectWa {
  display: inline-flex;
  margin-top: 8px;
  padding: 8px 12px;
  border-radius: 9px;
  background: #25d366;
  color: #052e16;
  font-weight: 800;
  font-size: 12px;
  text-decoration: none;
}

#iaAvatarSpriteWrap {
  position: relative;
  width: 136px;
  height: 157px;
  opacity: 0;
  will-change: transform, opacity;
}
#iaAvatarBtn {
  width: 100%;
  height: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  display: block;
  transform-origin: bottom center;
}
#iaAvatarImg {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  filter: drop-shadow(0 12px 24px rgba(0, 0, 0, 0.55));
  user-select: none;
  -webkit-user-drag: none;
}
#iaAvatarHideBtn {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 20px;
  height: 20px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(14, 14, 20, 0.85);
  color: #9ca3af;
  font-size: 12px;
  line-height: 1;
  cursor: pointer;
  opacity: 0.72;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: opacity 150ms, color 150ms;
}
#iaAvatarHideBtn:hover { opacity: 1; color: #fff; }
#iaAvatarRestore {
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255, 77, 0, 0.5);
  background: rgba(14, 14, 20, 0.92);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}

@media (min-width: 1024px) {
  #iaAvatarMiniCallout {
    display: none !important;
  }
}

@media (max-width: 1023px) {
  #${ROOT_ID} {
    right: 0;
    left: 0;
    bottom: 0;
    align-items: flex-end;
  }
  #iaAvatarBubble {
    display: none !important;
  }
  #iaAvatarSpriteWrap {
    position: fixed;
    left: 0;
    right: auto;
    bottom: var(--ia-av-ground, 69px);
    width: 86px;
    height: 100px;
    z-index: 45;
  }
  #iaAvatarFormModal {
    position: fixed;
    left: 12px;
    right: 12px;
    bottom: calc(var(--ia-av-ground, 69px) + 12px);
    margin: 0 auto;
    width: auto;
    max-width: 360px;
    max-height: calc(100vh - 120px);
    max-height: calc(100dvh - 120px);
    overflow-y: auto;
    z-index: 47;
  }
  #iaAvatarRestore {
    position: fixed;
    right: 12px;
    bottom: calc(var(--ia-av-ground, 69px) + 8px);
    z-index: 45;
  }
}

@keyframes ia-av-pop {
  from { opacity: 0; transform: translateY(10px) scale(0.94); }
  to { opacity: 1; transform: none; }
}
@keyframes ia-av-glow {
  0%, 100% { box-shadow: 0 10px 24px rgba(0, 0, 0, 0.65), 0 0 14px rgba(255, 77, 0, 0.28); }
  50% { box-shadow: 0 12px 28px rgba(0, 0, 0, 0.72), 0 0 24px rgba(255, 77, 0, 0.58); }
}
@keyframes ia-av-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.45; transform: scale(1.3); }
}
`;

function sanitizeText(value, maxLen) {
  return String(value || '')
    .replace(/[\u0000-\u001f\u007f<>]/g, '')
    .trim()
    .slice(0, maxLen);
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
}

function sanitizeHttpUrl(rawUrl, fallbackUrl) {
  try {
    const parsed = new URL(String(rawUrl || ''), window.location.origin);
    if (parsed.protocol === 'https:' || parsed.protocol === 'http:') {
      return parsed.href;
    }
  } catch (e) {}
  return fallbackUrl;
}

function preloadFrames(basePath, files, timeoutMs = 2500) {
  let capId = 0;
  const loaders = files.map(
    (name) =>
      new Promise((resolve) => {
        const img = new Image();
        img.onload = resolve;
        img.onerror = resolve;
        img.src = basePath + name;
      })
  );
  const cap = new Promise((resolve) => {
    capId = window.setTimeout(resolve, timeoutMs);
  });
  return Promise.race([
    Promise.all(loaders).then(() => {
      if (capId) window.clearTimeout(capId);
    }),
    cap,
  ]);
}

function pushDataLayer(payload) {
  try {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
  } catch (e) {}
}

function isMobileViewport() {
  return window.innerWidth < 1024;
}

function measureMobileGroundBottom() {
  const bar = document.querySelector('div[class*="lg:hidden"].fixed.bottom-0');
  const h = bar ? bar.getBoundingClientRect().height : 72;
  // Offset 3px for the sprite's 3% bottom alpha margin so feet rest flush on the bar
  return Math.max(0, Math.round(h > 0 ? h - 3 : 69));
}

/**
 * Mounts and runs the interactive Hermes Assistant avatar widget v2.
 */
export function initAvatarWidget(customConfig = {}) {
  if (window.__iaAvatar && typeof window.__iaAvatar.destroy === 'function') {
    window.__iaAvatar.destroy();
  }

  const cfg = Object.assign({}, DEFAULT_CONFIG, window.iaAvatarConfig || {}, customConfig);
  const rawBase = typeof cfg.basePath === 'string' && cfg.basePath.trim() ? cfg.basePath.trim() : DEFAULT_CONFIG.basePath;
  const basePath = rawBase.endsWith('/') ? rawBase : `${rawBase}/`;
  const safeChannelUrl = sanitizeHttpUrl(cfg.channelUrl, DEFAULT_CONFIG.channelUrl);
  const safeChannelLabel = sanitizeText(cfg.channelLabel, 60) || DEFAULT_CONFIG.channelLabel;

  if (!document.getElementById(STYLE_ID)) {
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = WIDGET_CSS;
    document.head.appendChild(style);
  }

  const root = document.createElement('div');
  root.id = ROOT_ID;
  root.setAttribute('aria-live', 'polite');
  root.innerHTML = `
    <div id="iaAvatarFormModal" role="dialog" aria-modal="false" aria-label="Falar com especialista no WhatsApp" hidden>
      <div class="ia-av-header">
        <span class="ia-av-badge"><span class="ia-av-dot"></span> Atendimento Rápido</span>
        <button type="button" id="iaAvatarFormClose" class="ia-av-close" aria-label="Fechar formulário">&times;</button>
      </div>
      <h4>Quer ajuda para começar?</h4>
      <p class="ia-av-sub">Preencha seu nome e e-mail para falar direto com nosso time no WhatsApp.</p>
      <form id="iaAvatarLeadForm" novalidate>
        <div class="ia-av-field">
          <label for="iaAvatarName">Seu nome *</label>
          <input id="iaAvatarName" name="name" type="text" required minlength="2" maxlength="80" autocomplete="name" placeholder="Ex.: João Silva">
        </div>
        <div class="ia-av-field">
          <label for="iaAvatarEmail">Seu melhor e-mail *</label>
          <input id="iaAvatarEmail" name="email" type="email" required maxlength="120" autocomplete="email" placeholder="voce@empresa.com.br">
        </div>
        <label class="ia-av-lgpd">
          <input type="checkbox" id="iaAvatarLgpd" name="lgpd" required>
          <span>Concordo com o uso dos meus dados para contato via WhatsApp e e-mail, conforme a LGPD.</span>
        </label>
        <p id="iaAvatarFormError" hidden></p>
        <button type="submit" id="iaAvatarSubmit">Ir para o WhatsApp &rarr;</button>
        <a id="iaAvatarModalChannelLink" class="ia-av-modal-channel" href="#" target="_blank" rel="noopener noreferrer"></a>
      </form>
      <div id="iaAvatarSuccessBox" hidden>
        <div>Perfeito! Tudo pronto para conversar com nosso vendedor no WhatsApp:</div>
        <a id="iaAvatarDirectWa" href="#" target="_blank" rel="noopener noreferrer">Abrir WhatsApp agora &rarr;</a>
      </div>
    </div>

    <div id="iaAvatarBubble" hidden>
      <div class="ia-av-header">
        <span class="ia-av-badge"><span class="ia-av-dot"></span> Assistente IA</span>
        <button type="button" id="iaAvatarBubbleClose" class="ia-av-close" aria-label="Minimizar balão">&times;</button>
      </div>
      <p id="iaAvatarBubbleText"></p>
      <div class="ia-av-actions">
        <a id="iaAvatarChannelBtn" class="ia-av-btn-primary" href="#" target="_blank" rel="noopener noreferrer"></a>
        <button type="button" id="iaAvatarHelpBtn" class="ia-av-btn-secondary">Quero ajuda</button>
      </div>
    </div>

    <button type="button" id="iaAvatarMiniCallout" hidden aria-label="Abrir atendimento">
      <span class="ia-av-dot"></span>
      <span id="iaAvatarMiniText">Oi! 👋</span>
    </button>

    <div id="iaAvatarSpriteWrap" hidden>
      <button type="button" id="iaAvatarBtn" aria-label="Falar com assistente da Inteligência Agêntica">
        <img id="iaAvatarImg" alt="Assistente Inteligência Agêntica" width="260" height="301">
      </button>
      <button type="button" id="iaAvatarHideBtn" aria-label="Ocultar assistente" title="Ocultar assistente">&times;</button>
    </div>

    <button type="button" id="iaAvatarRestore" hidden>💬 Assistente IA</button>
  `;
  document.body.appendChild(root);

  const elBubble = root.querySelector('#iaAvatarBubble');
  const elBubbleText = root.querySelector('#iaAvatarBubbleText');
  const btnBubbleClose = root.querySelector('#iaAvatarBubbleClose');
  const btnChannel = root.querySelector('#iaAvatarChannelBtn');
  const btnHelp = root.querySelector('#iaAvatarHelpBtn');
  const elMiniCallout = root.querySelector('#iaAvatarMiniCallout');
  const elMiniText = root.querySelector('#iaAvatarMiniText');
  const elModal = root.querySelector('#iaAvatarFormModal');
  const btnFormClose = root.querySelector('#iaAvatarFormClose');
  const elForm = root.querySelector('#iaAvatarLeadForm');
  const inputName = root.querySelector('#iaAvatarName');
  const inputEmail = root.querySelector('#iaAvatarEmail');
  const inputLgpd = root.querySelector('#iaAvatarLgpd');
  const elFormError = root.querySelector('#iaAvatarFormError');
  const modalChannelLink = root.querySelector('#iaAvatarModalChannelLink');
  const elSuccessBox = root.querySelector('#iaAvatarSuccessBox');
  const linkDirectWa = root.querySelector('#iaAvatarDirectWa');
  const elSpriteWrap = root.querySelector('#iaAvatarSpriteWrap');
  const btnAvatar = root.querySelector('#iaAvatarBtn');
  const imgAvatar = root.querySelector('#iaAvatarImg');
  const btnHide = root.querySelector('#iaAvatarHideBtn');
  const btnRestore = root.querySelector('#iaAvatarRestore');

  btnChannel.href = safeChannelUrl;
  btnChannel.textContent = safeChannelLabel;
  modalChannelLink.href = safeChannelUrl;
  modalChannelLink.textContent = `Prefere só acompanhar? ${safeChannelLabel} →`;
  imgAvatar.src = `${basePath}fall-drop.webp`;

  let state = 'waiting';
  let destroyed = false;
  let dropTriggered = false;
  let bubbleDismissed = false;
  let formOpen = false;
  let messageIndex = 0;
  let miniIndex = 0;
  let lastWhatsappUrl = '';

  const MOBILE_SPRITE_W = 86;
  let mobileX = Math.max(8, window.innerWidth - MOBILE_SPRITE_W - 14);
  let mobileDir = -1; // start walking left across the bottom bar
  let groundBottom = measureMobileGroundBottom();
  let lastMobile = isMobileViewport();

  const timers = new Set();
  const intervals = new Set();
  let dropRaf = 0;
  let walkRaf = 0;
  let cookieObserver = null;

  const setTimer = (fn, ms) => {
    const id = window.setTimeout(() => {
      timers.delete(id);
      if (!destroyed) fn();
    }, ms);
    timers.add(id);
    return id;
  };

  const clearSpriteTimers = () => {
    for (const id of timers) window.clearTimeout(id);
    timers.clear();
    for (const id of intervals) window.clearInterval(id);
    intervals.clear();
    if (dropRaf) {
      window.cancelAnimationFrame(dropRaf);
      dropRaf = 0;
    }
    if (walkRaf) {
      window.cancelAnimationFrame(walkRaf);
      walkRaf = 0;
    }
  };

  const setFrame = (name) => {
    if (destroyed) return;
    imgAvatar.src = `${basePath}${name}`;
  };

  const syncMobileGround = () => {
    groundBottom = measureMobileGroundBottom();
    root.style.setProperty('--ia-av-ground', `${groundBottom}px`);
    if (isMobileViewport()) {
      const maxX = Math.max(8, window.innerWidth - MOBILE_SPRITE_W - 8);
      mobileX = Math.min(Math.max(8, mobileX), maxX);
      if (state !== 'falling' && state !== 'waiting' && state !== 'hidden') {
        elSpriteWrap.style.transform = `translate3d(${mobileX}px, 0, 0)`;
      }
      positionMiniCallout();
    } else {
      elMiniCallout.hidden = true;
      if (state !== 'falling') {
        elSpriteWrap.style.transform = '';
      }
    }
  };

  const positionMiniCallout = () => {
    if (!isMobileViewport() || elMiniCallout.hidden) return;
    const vw = window.innerWidth;
    const pillW = elMiniCallout.offsetWidth || 120;
    const desired = mobileX + MOBILE_SPRITE_W / 2 - pillW / 2;
    const clamped = Math.max(8, Math.min(vw - pillW - 8, desired));
    elMiniCallout.style.setProperty('--ia-mc-x', `${Math.round(clamped)}px`);
  };

  const showMiniCallout = () => {
    if (!isMobileViewport() || formOpen || state === 'hidden') return;
    elBubble.hidden = true;
    elMiniText.textContent = MINI_CALLOUTS[miniIndex % MINI_CALLOUTS.length];
    elMiniCallout.hidden = false;
    positionMiniCallout();
  };

  const squash = () => {
    if (typeof btnAvatar.animate !== 'function') return;
    btnAvatar.animate(
      [
        { transform: 'scale(1, 1)' },
        { transform: 'scale(1.14, 0.84)' },
        { transform: 'scale(0.94, 1.07)' },
        { transform: 'scale(1, 1)' },
      ],
      { duration: 380, easing: 'ease-out' }
    );
  };

  const startDesktopIdleLoop = () => {
    if (destroyed || state === 'hidden' || state === 'falling' || state === 'landing') return;
    state = 'idle';
    let step = 0;
    const id = window.setInterval(() => {
      if (destroyed || state !== 'idle') return;
      step = (step + 1) % 8;
      setFrame(`breathe-${step}.webp`);
    }, 260);
    intervals.add(id);

    const scheduleBlink = () => {
      setTimer(() => {
        if (destroyed || state !== 'idle') return;
        setFrame('blink.webp');
        setTimer(() => {
          if (state === 'idle') setFrame('breathe-0.webp');
          scheduleBlink();
        }, 140);
      }, 3400 + Math.floor(Math.random() * 2200));
    };
    scheduleBlink();
  };

  const startMiniCalloutCycle = () => {
    const id = window.setInterval(() => {
      if (destroyed || !isMobileViewport() || formOpen || state === 'hidden') return;
      miniIndex = (miniIndex + 1) % MINI_CALLOUTS.length;
      elMiniText.textContent = MINI_CALLOUTS[miniIndex];
      positionMiniCallout();
    }, 3200);
    intervals.add(id);
  };

  const startMobileWalkCycle = () => {
    if (destroyed || !isMobileViewport() || formOpen || state === 'hidden') return;
    clearSpriteTimers();
    syncMobileGround();
    showMiniCallout();
    startMiniCalloutCycle();

    const beginWalk = (dir) => {
      if (destroyed || !isMobileViewport() || formOpen || state === 'hidden') return;
      mobileDir = dir;
      state = dir < 0 ? 'walkingLeft' : 'walkingRight';
      let frameStep = 0;
      const frameInt = window.setInterval(() => {
        if (destroyed || (state !== 'walkingLeft' && state !== 'walkingRight')) return;
        const prefix = state === 'walkingLeft' ? 'walk-left' : 'walk-right';
        setFrame(`${prefix}-${frameStep % 8}.webp`);
        frameStep++;
      }, 120);
      intervals.add(frameInt);

      let lastTs = performance.now();
      const segmentMs = 3200 + Math.floor(Math.random() * 2200);
      const startedAt = lastTs;

      const stepWalk = (ts) => {
        if (destroyed || (state !== 'walkingLeft' && state !== 'walkingRight')) return;
        const dt = Math.min(2.5, Math.max(0.5, (ts - lastTs) / 16.67));
        lastTs = ts;
        const maxX = Math.max(8, window.innerWidth - MOBILE_SPRITE_W - 8);
        mobileX += mobileDir * 0.95 * dt;

        let hitEdge = false;
        if (mobileX <= 8) {
          mobileX = 8;
          mobileDir = 1;
          hitEdge = true;
        } else if (mobileX >= maxX) {
          mobileX = maxX;
          mobileDir = -1;
          hitEdge = true;
        }

        elSpriteWrap.style.transform = `translate3d(${mobileX}px, 0, 0)`;
        positionMiniCallout();

        if (hitEdge || ts - startedAt >= segmentMs) {
          walkRaf = 0;
          window.clearInterval(frameInt);
          intervals.delete(frameInt);
          pauseBetweenWalks(mobileDir);
          return;
        }
        walkRaf = window.requestAnimationFrame(stepWalk);
      };
      walkRaf = window.requestAnimationFrame(stepWalk);
    };

    const pauseBetweenWalks = (nextDir) => {
      if (destroyed || !isMobileViewport() || formOpen || state === 'hidden') return;
      state = 'idle';
      let bStep = 0;
      const bInt = window.setInterval(() => {
        if (destroyed || state !== 'idle') return;
        setFrame(`breathe-${bStep % 8}.webp`);
        bStep++;
      }, 260);
      intervals.add(bInt);

      setTimer(() => {
        window.clearInterval(bInt);
        intervals.delete(bInt);
        beginWalk(nextDir);
      }, 2400 + Math.floor(Math.random() * 1000));
    };

    beginWalk(mobileDir);
  };

  const playDesktopTalkBurst = (msgText) => {
    if (destroyed || state === 'hidden') return;
    clearSpriteTimers();
    state = 'talking';
    elMiniCallout.hidden = true;
    if (!bubbleDismissed && !formOpen) {
      elBubbleText.textContent = msgText;
      elBubble.hidden = false;
    }
    let step = 0;
    const talkInt = window.setInterval(() => {
      if (destroyed || state !== 'talking') return;
      setFrame(`talk-${step % 8}.webp`);
      step++;
    }, 180);
    intervals.add(talkInt);

    setTimer(() => {
      window.clearInterval(talkInt);
      intervals.delete(talkInt);
      startDesktopIdleLoop();
      scheduleNextDesktopMessage();
    }, 2400);
  };

  const scheduleNextDesktopMessage = () => {
    setTimer(() => {
      if (destroyed || isMobileViewport() || state === 'hidden' || formOpen || bubbleDismissed) return;
      messageIndex = (messageIndex + 1) % DESKTOP_MESSAGES.length;
      playDesktopTalkBurst(DESKTOP_MESSAGES[messageIndex]);
    }, 9000);
  };

  const runLandingSequence = () => {
    if (destroyed) return;
    state = 'landing';
    squash();
    setFrame('fall-land.webp');
    setTimer(() => {
      setFrame('fall-getup.webp');
      setTimer(() => {
        setFrame('fall-dizzy.webp');
        setTimer(() => {
          setFrame('wave-1.webp');
          setTimer(() => {
            setFrame('wave-2.webp');
            setTimer(() => {
              setFrame('wave-3.webp');
              setTimer(() => {
                preloadFrames(basePath, EXTRA_FRAMES, 4000);
                if (isMobileViewport()) {
                  startMobileWalkCycle();
                } else {
                  messageIndex = 0;
                  playDesktopTalkBurst(DESKTOP_MESSAGES[0]);
                }
              }, 220);
            }, 220);
          }, 220);
        }, 440);
      }, 360);
    }, 320);
  };

  const startDrop = async () => {
    if (destroyed || dropTriggered) return;
    dropTriggered = true;
    if (cookieObserver) {
      cookieObserver.disconnect();
      cookieObserver = null;
    }

    const toPreload = isMobileViewport() ? [...CRITICAL_FRAMES, ...WALK_FRAMES.slice(0, 4)] : CRITICAL_FRAMES;
    await preloadFrames(basePath, toPreload, 2500);
    if (destroyed) return;

    clearSpriteTimers();
    syncMobileGround();
    state = 'falling';
    setFrame('fall-drop.webp');
    elSpriteWrap.hidden = false;
    elSpriteWrap.style.opacity = '1';

    const mob = isMobileViewport();
    if (mob) {
      mobileX = Math.max(8, window.innerWidth - MOBILE_SPRITE_W - 14);
    }

    let y = -(window.innerHeight + 160);
    let vy = 2;
    let lastTs = performance.now();
    elSpriteWrap.style.transform = mob ? `translate3d(${mobileX}px, ${y}px, 0)` : `translate3d(0, ${y}px, 0)`;

    const tick = (ts) => {
      if (destroyed || state !== 'falling') return;
      const dt = Math.min(2.5, Math.max(0.5, (ts - lastTs) / 16.67));
      lastTs = ts;
      vy += 1.35 * dt;
      y += vy * dt;
      if (y >= 0) {
        elSpriteWrap.style.transform = mob ? `translate3d(${mobileX}px, 0, 0)` : 'translate3d(0, 0, 0)';
        dropRaf = 0;
        runLandingSequence();
        return;
      }
      elSpriteWrap.style.transform = mob ? `translate3d(${mobileX}px, ${y}px, 0)` : `translate3d(0, ${y}px, 0)`;
      dropRaf = window.requestAnimationFrame(tick);
    };
    dropRaf = window.requestAnimationFrame(tick);
  };

  const openForm = () => {
    if (destroyed) return;
    formOpen = true;
    elBubble.hidden = true;
    elMiniCallout.hidden = true;
    elFormError.hidden = true;
    elSuccessBox.hidden = true;
    elForm.hidden = false;
    elModal.hidden = false;

    squash();
    if (state !== 'falling' && state !== 'landing') {
      clearSpriteTimers();
      state = 'reacting';
      let step = 0;
      const appInt = window.setInterval(() => {
        if (destroyed || state !== 'reacting') return;
        if (step >= 6) {
          window.clearInterval(appInt);
          intervals.delete(appInt);
          startDesktopIdleLoop();
          return;
        }
        setFrame(`approve-${step}.webp`);
        step++;
      }, 90);
      intervals.add(appInt);
    }

    pushDataLayer({ event: 'avatar_form_open', avatar_source: 'hermes_assistant' });
    setTimer(() => inputName.focus(), 60);
  };

  const closeForm = () => {
    formOpen = false;
    elModal.hidden = true;
    if (state === 'hidden' || state === 'falling' || state === 'landing') return;
    if (isMobileViewport()) {
      startMobileWalkCycle();
    } else if (!bubbleDismissed) {
      elBubble.hidden = false;
      scheduleNextDesktopMessage();
    }
  };

  const onKeyDown = (e) => {
    if (e.key === 'Escape' && formOpen) closeForm();
  };
  const onResize = () => {
    const mob = isMobileViewport();
    syncMobileGround();
    if (mob !== lastMobile) {
      lastMobile = mob;
      if (dropTriggered && state !== 'hidden' && state !== 'falling' && state !== 'landing') {
        if (mob) {
          elBubble.hidden = true;
          if (!formOpen) startMobileWalkCycle();
        } else {
          elMiniCallout.hidden = true;
          if (!formOpen) playDesktopTalkBurst(DESKTOP_MESSAGES[messageIndex]);
        }
      }
    }
  };
  document.addEventListener('keydown', onKeyDown);
  window.addEventListener('resize', onResize, { passive: true });

  btnAvatar.addEventListener('click', openForm);
  elMiniCallout.addEventListener('click', openForm);
  btnHelp.addEventListener('click', openForm);
  btnFormClose.addEventListener('click', closeForm);

  btnBubbleClose.addEventListener('click', () => {
    bubbleDismissed = true;
    elBubble.hidden = true;
  });

  const onChannelClick = () => {
    pushDataLayer({
      event: 'avatar_channel_click',
      channel_url: safeChannelUrl,
    });
  };
  btnChannel.addEventListener('click', onChannelClick);
  modalChannelLink.addEventListener('click', onChannelClick);

  btnHide.addEventListener('click', () => {
    clearSpriteTimers();
    state = 'hidden';
    formOpen = false;
    elBubble.hidden = true;
    elMiniCallout.hidden = true;
    elModal.hidden = true;
    elSpriteWrap.hidden = true;
    btnRestore.hidden = false;
  });

  btnRestore.addEventListener('click', () => {
    btnRestore.hidden = true;
    elSpriteWrap.hidden = false;
    elSpriteWrap.style.opacity = '1';
    bubbleDismissed = false;
    syncMobileGround();
    if (isMobileViewport()) {
      startMobileWalkCycle();
    } else {
      playDesktopTalkBurst(DESKTOP_MESSAGES[messageIndex]);
    }
  });

  elForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = sanitizeText(inputName.value, 80);
    const email = sanitizeText(inputEmail.value, 120);

    if (name.length < 2) {
      elFormError.textContent = 'Por favor, informe seu nome (mínimo 2 letras).';
      elFormError.hidden = false;
      inputName.focus();
      return;
    }
    if (!isValidEmail(email)) {
      elFormError.textContent = 'Por favor, informe um e-mail válido.';
      elFormError.hidden = false;
      inputEmail.focus();
      return;
    }
    if (!inputLgpd.checked) {
      elFormError.textContent = 'Para continuar, marque a caixa de consentimento conforme a LGPD.';
      elFormError.hidden = false;
      inputLgpd.focus();
      return;
    }

    elFormError.hidden = true;
    const cleanPhone = String(cfg.whatsappNumber || '').replace(/\D/g, '');
    const msg = `Olá! Meu nome é ${name} (${email}). Estava no site da Inteligência Agêntica e quero ajuda para começar!`;
    const waUrl = `https://wa.me/${cleanPhone}?text=${encodeURIComponent(msg)}`;
    lastWhatsappUrl = waUrl;

    const firstName = name.split(/\s+/)[0] || name;
    pushDataLayer({
      event: 'generate_lead',
      form_id: 'avatarLeadForm',
      form_name: 'Avatar Assistente WhatsApp',
      lead_name: name,
      lead_first_name: firstName,
      lead_email: email,
      lead_source: 'avatar_widget',
      lgpd_consent: true,
      page_path: window.location.pathname,
      user_data: { email },
    });
    pushDataLayer({
      event: 'avatar_whatsapp_redirect',
      lead_source: 'avatar_widget',
      whatsapp_number: cleanPhone,
    });

    if (cfg.enableListmonk && cfg.listmonkEndpoint) {
      fetch(cfg.listmonkEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        keepalive: true,
        body: JSON.stringify({
          email,
          name,
          list_uuids: [cfg.listmonkListUuid],
        }),
      }).catch(() => {});
    }

    linkDirectWa.href = waUrl;
    elForm.hidden = true;
    elSuccessBox.hidden = false;

    const opened = window.open('', '_blank');
    if (opened) {
      try {
        opened.opener = null;
        opened.location.href = waUrl;
      } catch (err) {}
    } else {
      setTimer(() => {
        if (!destroyed) window.location.assign(waUrl);
      }, 280);
    }
  });

  // Start drop after cookie banner closes (or 1600ms if already closed; 6500ms max fallback)
  const banner = document.getElementById('cookie-consent-banner');
  const isBannerOpen = () => banner && window.getComputedStyle(banner).display !== 'none';

  if (isBannerOpen() && 'MutationObserver' in window) {
    cookieObserver = new MutationObserver(() => {
      if (!isBannerOpen()) {
        setTimer(startDrop, 350);
      }
    });
    cookieObserver.observe(banner, { attributes: true, attributeFilter: ['style', 'class'] });
    setTimer(startDrop, 6500);
  } else {
    setTimer(startDrop, 1600);
  }

  const destroy = () => {
    if (destroyed) return;
    destroyed = true;
    clearSpriteTimers();
    if (cookieObserver) {
      cookieObserver.disconnect();
      cookieObserver = null;
    }
    document.removeEventListener('keydown', onKeyDown);
    window.removeEventListener('resize', onResize);
    root.remove();
    if (window.__iaAvatar && window.__iaAvatar.destroy === destroy) {
      delete window.__iaAvatar;
    }
  };

  const api = {
    getState: () => ({
      state,
      isMobile: isMobileViewport(),
      x: Math.round(mobileX),
      groundBottom,
      formOpen,
      bubbleOpen: !elBubble.hidden,
      miniCalloutOpen: !elMiniCallout.hidden,
      lgpdChecked: !!inputLgpd.checked,
      messageIndex,
      lastWhatsappUrl,
    }),
    openForm,
    closeForm,
    replayDrop: () => {
      dropTriggered = false;
      bubbleDismissed = false;
      btnRestore.hidden = true;
      startDrop();
    },
    getLastWhatsappUrl: () => lastWhatsappUrl,
    destroy,
  };

  window.__iaAvatar = api;
  return api;
}
