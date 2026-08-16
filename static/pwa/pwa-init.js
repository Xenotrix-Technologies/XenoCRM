// XenoCRM Progressive Web App (PWA) Client Init Script
(function () {
    let deferredPrompt = null;

    // 1. Service Worker Registration
    if ('serviceWorker' in navigator) {
        let refreshing = false;
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            if (!refreshing) {
                refreshing = true;
                console.log('[XenoCRM PWA] ServiceWorker updated, refreshing application...');
                window.location.reload();
            }
        });

        window.addEventListener('load', () => {
            const swUrl = window.XENOCRM_SW_URL || '/static/pwa/service-worker.js';
            
            navigator.serviceWorker.register(swUrl)
                .then((registration) => {
                    console.log('[XenoCRM PWA] ServiceWorker registered with scope:', registration.scope);
                    
                    // Force update check
                    registration.update();

                    // Check for SW updates
                    registration.addEventListener('updatefound', () => {
                        const newWorker = registration.installing;
                        if (newWorker) {
                            newWorker.addEventListener('statechange', () => {
                                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                    newWorker.postMessage({ type: 'SKIP_WAITING' });
                                    if (window.showToast) {
                                        showToast('App updated to the latest version.', 'info');
                                    }
                                }
                            });
                        }
                    });
                })
                .catch((err) => {
                    console.warn('[XenoCRM PWA] ServiceWorker registration failed:', err);
                });
        });
    }

    // 2. Capture Install Prompt (Chrome / Android / Edge)
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent default mini-infobar
        e.preventDefault();
        deferredPrompt = e;

        // Show PWA install trigger button/banner if present
        showInstallBanner();
    });

    // 3. Track App Installed State
    window.addEventListener('appinstalled', () => {
        deferredPrompt = null;
        hideInstallBanner();
        if (window.showToast) {
            showToast('XenoCRM installed successfully on your home screen!', 'success');
        }
    });

    // 4. Online / Offline Network Monitoring
    window.addEventListener('online', () => {
        if (window.showToast) {
            showToast('Network connection restored. Back online!', 'success');
        }
        const offlineBanner = document.getElementById('offline-network-banner');
        if (offlineBanner) offlineBanner.classList.add('hidden');
    });

    window.addEventListener('offline', () => {
        if (window.showToast) {
            showToast('You are currently offline. Live ERP changes require internet connection.', 'error');
        }
        const offlineBanner = document.getElementById('offline-network-banner');
        if (offlineBanner) offlineBanner.classList.remove('hidden');
    });

    // Global Functions for Install Trigger
    window.triggerPWAInstall = function () {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('[XenoCRM PWA] User accepted the install prompt');
                } else {
                    console.log('[XenoCRM PWA] User dismissed the install prompt');
                }
                deferredPrompt = null;
                hideInstallBanner();
            });
        } else if (isIOS()) {
            showIOSInstallInstructions();
        } else {
            if (window.showToast) {
                showToast('App installation is available from your browser menu ("Add to Home Screen").', 'info');
            }
        }
    };

    function isIOS() {
        return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    }

    function isInStandaloneMode() {
        return (window.matchMedia('(display-mode: standalone)').matches) || (window.navigator.standalone) || document.referrer.includes('android-app://');
    }

    function showInstallBanner() {
        if (isInStandaloneMode()) return;
        
        const banner = document.getElementById('pwa-install-banner');
        if (banner) {
            banner.classList.remove('hidden');
        }
    }

    function hideInstallBanner() {
        const banner = document.getElementById('pwa-install-banner');
        if (banner) {
            banner.classList.add('hidden');
        }
    }

    function showIOSInstallInstructions() {
        const modal = document.getElementById('ios-install-modal');
        if (modal) {
            modal.classList.remove('hidden');
        } else if (window.showToast) {
            showToast('To install on iPhone/iPad: tap the Share button in Safari, then tap "Add to Home Screen".', 'info');
        }
    }

    // Auto check on load if on iOS & not standalone
    document.addEventListener('DOMContentLoaded', () => {
        if (isIOS() && !isInStandaloneMode()) {
            const iosBanner = document.getElementById('pwa-install-banner');
            if (iosBanner) iosBanner.classList.remove('hidden');
        }
    });
})();
