/* ==========================================================================
   The Academy's Bryan - script.js
   Versión: 1.0
   Autor: Equipo (adaptado para Bryan Leonardo Pacheco Torres)
   ========================================================================== */

/* -------------------------
   Utilidades y helpers
   ------------------------- */
   const safeQuery = (selector, ctx = document) => ctx.querySelector(selector);
   const safeQueryAll = (selector, ctx = document) => Array.from(ctx.querySelectorAll(selector));
   
   const debounce = (fn, wait = 200) => {
     let t;
     return (...args) => {
       clearTimeout(t);
       t = setTimeout(() => fn.apply(this, args), wait);
     };
   };
   
   const throttle = (fn, limit = 200) => {
     let inThrottle;
     return (...args) => {
       if (!inThrottle) {
         fn.apply(this, args);
         inThrottle = true;
         setTimeout(() => (inThrottle = false), limit);
       }
     };
   };
   
   const isTouchDevice = () => ('ontouchstart' in window) || navigator.maxTouchPoints > 0;
   
   /* -------------------------
      Toasts (mensajes no intrusivos)
      ------------------------- */
   const Toast = (() => {
     let container;
     function ensureContainer() {
       if (!container) {
         container = document.createElement('div');
         container.id = 'toast-container';
         Object.assign(container.style, {
           position: 'fixed',
           right: '20px',
           bottom: '20px',
           zIndex: 9999,
           display: 'flex',
           flexDirection: 'column',
           gap: '10px',
           alignItems: 'flex-end'
         });
         document.body.appendChild(container);
       }
     }
     function show(message, { duration = 4000, type = 'info' } = {}) {
       ensureContainer();
       const el = document.createElement('div');
       el.className = `toast toast-${type}`;
       el.textContent = message;
       Object.assign(el.style, {
         background: type === 'error' ? '#b00020' : type === 'success' ? '#1e8e3e' : '#222',
         color: '#fff',
         padding: '10px 14px',
         borderRadius: '8px',
         boxShadow: '0 6px 18px rgba(0,0,0,0.15)',
         maxWidth: '320px',
         fontSize: '0.95rem'
       });
       container.appendChild(el);
       setTimeout(() => {
         el.style.transition = 'opacity 300ms ease, transform 300ms ease';
         el.style.opacity = '0';
         el.style.transform = 'translateY(8px)';
         setTimeout(() => el.remove(), 320);
       }, duration);
     }
     return { show };
   })();
   
   /* -------------------------
      Modo oscuro persistente
      ------------------------- */
   const DarkMode = (() => {
     const key = 'theacademy_darkmode';
     function isDark() {
       return localStorage.getItem(key) === '1';
     }
     function apply(dark) {
       document.documentElement.classList.toggle('dark-mode', dark);
       localStorage.setItem(key, dark ? '1' : '0');
     }
     function toggle() {
       apply(!isDark());
       Toast.show(isDark() ? 'Modo oscuro activado' : 'Modo oscuro desactivado', { type: 'success' });
     }
     return { isDark, apply, toggle };
   })();
   
   /* -------------------------
      Menú responsive (hamburguesa)
      ------------------------- */
   const ResponsiveMenu = (() => {
     const menu = safeQuery('#menu');
     const btn = safeQuery('#menu-toggle'); // botón hamburguesa
     function init() {
       if (!menu || !btn) return;
       btn.addEventListener('click', (e) => {
         e.preventDefault();
         const expanded = btn.getAttribute('aria-expanded') === 'true';
         btn.setAttribute('aria-expanded', String(!expanded));
         menu.classList.toggle('show');
       });
       // Cerrar al click fuera
       document.addEventListener('click', (e) => {
         if (!menu.classList.contains('show')) return;
         if (!menu.contains(e.target) && !btn.contains(e.target)) {
           menu.classList.remove('show');
           btn.setAttribute('aria-expanded', 'false');
         }
       });
       // Cerrar con Escape
       document.addEventListener('keydown', (e) => {
         if (e.key === 'Escape' && menu.classList.contains('show')) {
           menu.classList.remove('show');
           btn.setAttribute('aria-expanded', 'false');
         }
       });
     }
     return { init };
   })();
   
   /* -------------------------
      Acordeón FAQ
      ------------------------- */
   const FAQ = (() => {
     function init() {
       const items = safeQueryAll('.faq-item');
       if (!items.length) return;
       items.forEach(item => {
         item.setAttribute('role', 'button');
         item.setAttribute('tabindex', '0');
         item.addEventListener('click', toggleItem);
         item.addEventListener('keydown', (e) => {
           if (e.key === 'Enter' || e.key === ' ') {
             e.preventDefault();
             toggleItem.call(item);
           }
         });
       });
     }
     function toggleItem() {
       const answer = this.nextElementSibling;
       if (!answer || !answer.classList.contains('faq-answer')) return;
       const isOpen = answer.classList.contains('open');
       // Cerrar todas
       document.querySelectorAll('.faq-answer.open').forEach(a => {
         a.classList.remove('open');
         a.style.maxHeight = null;
       });
       if (!isOpen) {
         answer.classList.add('open');
         answer.style.maxHeight = answer.scrollHeight + 'px';
       } else {
         answer.classList.remove('open');
         answer.style.maxHeight = null;
       }
     }
     return { init };
   })();
   
   /* -------------------------
      Banner de cookies simple
      ------------------------- */
   const CookieBanner = (() => {
     const key = 'theacademy_cookies_accepted';
     function init() {
       if (localStorage.getItem(key) === '1') return;
       const banner = document.createElement('div');
       banner.id = 'cookie-banner';
       banner.innerHTML = `
         <div style="max-width:1100px;margin:0 auto;padding:14px 18px;display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;">
           <div style="color:#fff;font-size:0.95rem;">
             Usamos cookies para mejorar tu experiencia. Al continuar aceptas nuestra política.
           </div>
           <div style="display:flex;gap:8px;">
             <button id="cookie-accept" style="background:#1e8e3e;color:#fff;border:none;padding:8px 12px;border-radius:6px;cursor:pointer;">Aceptar</button>
             <button id="cookie-close" style="background:transparent;color:#fff;border:1px solid rgba(255,255,255,0.2);padding:8px 12px;border-radius:6px;cursor:pointer;">Cerrar</button>
           </div>
         </div>
       `;
       Object.assign(banner.style, {
         position: 'fixed',
         left: '0',
         right: '0',
         bottom: '0',
         background: '#0e1a33',
         zIndex: 9998,
         boxShadow: '0 -6px 18px rgba(0,0,0,0.2)'
       });
       document.body.appendChild(banner);
       document.getElementById('cookie-accept').addEventListener('click', () => {
         localStorage.setItem(key, '1');
         banner.remove();
         Toast.show('Cookies aceptadas', { type: 'success' });
       });
       document.getElementById('cookie-close').addEventListener('click', () => {
         banner.remove();
       });
     }
     return { init };
   })();
   
   /* -------------------------
      Lazy load images (fallback)
      ------------------------- */
   const LazyLoad = (() => {
     function init() {
       if ('loading' in HTMLImageElement.prototype) {
         // Si el navegador soporta loading="lazy", solo aseguramos que las imágenes lo tengan
         document.querySelectorAll('img[data-lazy]').forEach(img => img.setAttribute('loading', 'lazy'));
         return;
       }
       // Fallback con IntersectionObserver
       const imgs = document.querySelectorAll('img[data-lazy]');
       if (!imgs.length) return;
       const io = new IntersectionObserver((entries, observer) => {
         entries.forEach(entry => {
           if (entry.isIntersecting) {
             const img = entry.target;
             img.src = img.dataset.src;
             img.removeAttribute('data-lazy');
             observer.unobserve(img);
           }
         });
       }, { rootMargin: '200px 0px' });
       imgs.forEach(img => io.observe(img));
     }
     return { init };
   })();
   
   /* -------------------------
      Form validation básica
      ------------------------- */
   const FormValidation = (() => {
     function init() {
       const forms = document.querySelectorAll('form.needs-validation');
       if (!forms.length) return;
       forms.forEach(form => {
         form.addEventListener('submit', (e) => {
           if (!form.checkValidity()) {
             e.preventDefault();
             e.stopPropagation();
             form.classList.add('was-validated');
             Toast.show('Por favor, completa los campos requeridos.', { type: 'error' });
           } else {
             // Aquí puedes añadir lógica antes de enviar (p. ej. mostrar spinner)
           }
         });
       });
     }
     return { init };
   })();
   
   /* -------------------------
      Inicialización principal
      ------------------------- */
   document.addEventListener('DOMContentLoaded', () => {
     console.log('JavaScript cargado correctamente ✅');
   
     // Aplicar modo oscuro si estaba activo
     if (localStorage.getItem('theacademy_darkmode') === '1') {
       document.documentElement.classList.add('dark-mode');
     }
   
     // Inicializaciones
     ResponsiveMenu.init();
     FAQ.init();
     CookieBanner.init();
     LazyLoad.init();
     FormValidation.init();
   
     // Detectar dispositivo
     if (isTouchDevice()) {
       document.documentElement.classList.add('touch-device');
       console.log('Dispositivo táctil detectado');
     } else {
       document.documentElement.classList.add('no-touch');
     }
   
     // Mensaje de bienvenida no intrusivo (usar toast en vez de alert por defecto)
     if (!sessionStorage.getItem('welcome_shown')) {
       Toast.show("Bienvenido a The Academy's Bryan 🏆", { duration: 3500, type: 'success' });
       sessionStorage.setItem('welcome_shown', '1');
     }
   
     // Botón toggle dark si existe
     const toggleDarkBtn = safeQuery('#toggle-dark');
     if (toggleDarkBtn) {
       toggleDarkBtn.addEventListener('click', (e) => {
         e.preventDefault();
         DarkMode.toggle();
       });
     }
   
     // Debug: detectar ancho inicial
     if (window.innerWidth < 768) {
       console.log('Estás en un dispositivo móvil 📱');
     }
   });
   
   /* -------------------------
      Puntos de extensión / Analytics (placeholder)
      ------------------------- */
   const Analytics = (() => {
     function track(eventName, payload = {}) {
       // Placeholder: aquí puedes integrar Google Analytics, Plausible, etc.
       // Ejemplo: window.gtag && window.gtag('event', eventName, payload);
       console.log('[Analytics] event:', eventName, payload);
     }
     return { track };
   })();
   
   /* -------------------------
      Exportar funciones útiles al scope global (opcional)
      ------------------------- */
   window.TheAcademy = {
     toggleDarkMode: DarkMode.toggle,
     showToast: Toast.show,
     trackEvent: Analytics.track
   };
   