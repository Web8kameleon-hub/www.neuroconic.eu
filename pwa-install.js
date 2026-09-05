(function () {
  const INSTALL_ID = 'pwaInstallBanner';
  const isStandalone = () =>
    window.matchMedia('(display-mode: standalone)').matches ||
    navigator.standalone === true;

  const getInstallText = () => {
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    return isIOS
      ? 'Open Safari → Share → Add to Home Screen'
      : 'Install app';
  };

  function ensureBanner() {
    const existing = document.getElementById(INSTALL_ID);
    if (existing) return existing;

    const banner = document.createElement('div');
    banner.id = INSTALL_ID;
    banner.setAttribute('role', 'status');
    banner.style.position = 'fixed';
    banner.style.left = '50%';
    banner.style.bottom = '20px';
    banner.style.transform = 'translateX(-50%)';
    banner.style.display = 'none';
    banner.style.zIndex = '9999';
    banner.style.maxWidth = '480px';
    banner.style.width = 'calc(100% - 32px)';
    banner.style.background = 'rgba(11, 16, 29, 0.96)';
    banner.style.border = '1px solid rgba(139, 92, 246, 0.4)';
    banner.style.boxShadow = '0 18px 42px rgba(9, 14, 24, 0.38)';
    banner.style.borderRadius = '18px';
    banner.style.padding = '12px 14px';
    banner.style.color = '#edf2ff';
    banner.style.fontFamily = 'Segoe UI, sans-serif';
    banner.style.fontSize = '14px';
    banner.style.lineHeight = '1.4';
    banner.style.backdropFilter = 'blur(10px)';

    const text = document.createElement('div');
    text.style.display = 'flex';
    text.style.alignItems = 'center';
    text.style.justifyContent = 'space-between';
    text.style.gap = '14px';

    const label = document.createElement('span');
    label.textContent = 'Install Neurosonic on your phone';
    label.style.flex = '1';
    label.style.color = '#e8edff';

    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = getInstallText();
    button.style.border = '0';
    button.style.borderRadius = '10px';
    button.style.padding = '9px 12px';
    button.style.fontWeight = '700';
    button.style.background = 'linear-gradient(135deg, #4cc9f0, #8b5cf6)';
    button.style.color = '#fff';
    button.style.cursor = 'pointer';
    button.style.fontSize = '12px';

    button.addEventListener('click', async () => {
      if (window.__NEUROSONIC_DEFERRED_PROMPT__) {
        window.__NEUROSONIC_DEFERRED_PROMPT__.prompt();
        const result = await window.__NEUROSONIC_DEFERRED_PROMPT__.userChoice;
        if (result && result.outcome === 'accepted') {
          banner.style.display = 'none';
        }
        return;
      }

      const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
        (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
      if (isIOS) {
        alert('On iPhone or iPad: open Safari, tap Share, then tap “Add to Home Screen”.');
      }
    });

    text.appendChild(label);
    text.appendChild(button);
    banner.appendChild(text);
    document.body.appendChild(banner);
    return banner;
  }

  function showInstallPrompt(message) {
    if (isStandalone()) return;
    const banner = ensureBanner();
    const button = banner.querySelector('button');
    if (message) {
      banner.querySelector('span').textContent = message;
    }
    button.textContent = getInstallText();
    banner.style.display = 'block';
  }

  function hideInstallPrompt() {
    const banner = document.getElementById(INSTALL_ID);
    if (banner) banner.style.display = 'none';
  }

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/service-worker.js').catch(function () {
        // no-op fallback when browser blocks registration
      });
    });
  }

  window.addEventListener('beforeinstallprompt', function (event) {
    event.preventDefault();
    window.__NEUROSONIC_DEFERRED_PROMPT__ = event;
    showInstallPrompt('Install Neurosonic on your phone');
  });

  window.addEventListener('appinstalled', function () {
    hideInstallPrompt();
  });

  document.addEventListener('DOMContentLoaded', function () {
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);

    if (!isStandalone()) {
      window.setTimeout(function () {
        if (!window.__NEUROSONIC_DEFERRED_PROMPT__) {
          showInstallPrompt(isIOS ? 'Add Neurosonic to your home screen' : 'Install Neurosonic on your phone');
        }
      }, 900);
    }
  });
})();
