/* Ankor — interações compartilhadas (home + landing pages). Sem dependências. */
(function () {
  'use strict';

  var CFG = window.ANKOR_CONFIG || {};
  var IMAGES = window.ANKOR_IMAGES || [];
  var BASE = document.documentElement.getAttribute('data-base') || '';
  var IMG = BASE + 'assets/img/';
  var byId = {};
  IMAGES.forEach(function (im) { byId[im.id] = im; });

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var ICON = {
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    prev: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M15 5l-7 7 7 7"/></svg>',
    next: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 5l7 7-7 7"/></svg>'
  };
  var UNIT_LABEL = { '303': 'Cobertura 303', '304': 'Cobertura 304' };

  function track(event, data) {
    window.dataLayer = window.dataLayer || [];
    var payload = { event: event };
    for (var k in data) payload[k] = data[k];
    window.dataLayer.push(payload);
  }

  /* ---------- Header / navegação ---------- */
  var header = $('.header');
  var mobileBar = $('.mobile-bar');
  function onScroll() {
    var y = window.scrollY;
    if (header && !header.classList.contains('header--solid')) header.classList.toggle('is-scrolled', y > 40);
    if (mobileBar) mobileBar.classList.toggle('is-visible', y > window.innerHeight * 0.6);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var toggle = $('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open);
    });
    $$('.nav a').forEach(function (a) {
      a.addEventListener('click', function () {
        document.body.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- Hero com troca suave de fotos ---------- */
  var slides = $$('.hero__slide');
  if (slides.length > 1) {
    var dots = $$('.hero__dots button');
    var caption = $('.hero__caption');
    var current = 0, timer;
    var go = function (i) {
      slides[current].classList.remove('is-active');
      if (dots[current]) dots[current].classList.remove('is-active');
      current = (i + slides.length) % slides.length;
      var s = slides[current];
      var img = $('img', s);
      if (img && img.dataset.srcset) { img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); }
      if (img && img.dataset.src) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
      s.classList.add('is-active');
      if (dots[current]) dots[current].classList.add('is-active');
      if (caption) caption.textContent = s.getAttribute('data-caption') || '';
    };
    var play = function () { clearInterval(timer); timer = setInterval(function () { go(current + 1); }, 6500); };
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); play(); }); });
    // Carrega as fotos seguintes só depois da primeira (LCP) estar pronta.
    window.addEventListener('load', function () {
      slides.forEach(function (s) {
        var im = $('img', s);
        if (!im || !im.dataset.src) return;
        var pre = new Image();
        if (im.dataset.srcset) { pre.sizes = im.sizes; pre.srcset = im.dataset.srcset; }
        pre.src = im.dataset.src;
      });
      if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) play();
    });
  }

  /* ---------- Revelação no scroll ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    $$('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    $$('.reveal').forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- Lightbox ---------- */
  var lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', 'Visualizar imagem');
  lb.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button class="icon-btn lb-close" aria-label="Fechar">' + ICON.close + '</button>' +
    '<button class="icon-btn lb-prev" aria-label="Imagem anterior">' + ICON.prev + '</button>' +
    '<button class="icon-btn lb-next" aria-label="Próxima imagem">' + ICON.next + '</button>';
  document.body.appendChild(lb);
  var lbList = [], lbIndex = 0, lbReturn = null;
  function lbShow(i) {
    lbIndex = (i + lbList.length) % lbList.length;
    var im = byId[lbList[lbIndex]];
    if (!im) return;
    var img = $('img', lb);
    img.src = IMG + im.src;
    img.alt = im.cap;
    var note = im.cat === 'plantas' ? 'Planta humanizada ilustrativa' : 'Foto real' + (im.unit ? ' · ' + UNIT_LABEL[im.unit] + ' · unidade sem decoração' : '');
    $('figcaption', lb).innerHTML = im.cap + '<small>' + note + ' — ' + (lbIndex + 1) + ' / ' + lbList.length + '</small>';
    var nextIm = byId[lbList[(lbIndex + 1) % lbList.length]];
    if (nextIm) { var pre = new Image(); pre.src = IMG + nextIm.src; }
  }
  function lbOpen(list, i) {
    lbList = list; lbReturn = document.activeElement;
    lbShow(i);
    lb.classList.add('is-open');
    document.body.classList.add('lock');
    $('.lb-close', lb).focus();
  }
  function lbClose() {
    lb.classList.remove('is-open');
    if (!$('.modal.is-open')) document.body.classList.remove('lock');
    if (lbReturn) lbReturn.focus();
  }
  $('.lb-close', lb).addEventListener('click', lbClose);
  $('.lb-prev', lb).addEventListener('click', function () { lbShow(lbIndex - 1); });
  $('.lb-next', lb).addEventListener('click', function () { lbShow(lbIndex + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) lbClose(); });
  var touchX = null;
  lb.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) lbShow(lbIndex + (dx < 0 ? 1 : -1));
    touchX = null;
  });

  /* Itens de galeria já presentes no HTML: [data-img] dentro de um [data-lb-group] */
  document.addEventListener('click', function (e) {
    var item = e.target.closest('[data-img]');
    if (!item) return;
    e.preventDefault();
    var group = item.closest('[data-lb-group]') || document;
    var list = $$('[data-img]', group).map(function (el) { return el.getAttribute('data-img'); });
    lbOpen(list, list.indexOf(item.getAttribute('data-img')));
  });

  function itemHTML(im, lazy, large) {
    return '<button class="g-item" type="button" data-img="' + im.id + '">' +
      '<img src="' + IMG + (large ? im.src : im.sm) + '" alt="' + im.cap + '" width="' + im.w + '" height="' + im.h + '"' + (lazy ? ' loading="lazy" decoding="async"' : '') + '>' +
      '<span class="g-cap">' + im.cap + '</span></button>';
  }

  /* ---------- Grupos de galeria ---------- */
  function has(im, words) { return words.some(function (w) { return im.id.indexOf(w) !== -1; }); }
  function groupsFor(scope) {
    if (scope === '303' || scope === '304') {
      var u = IMAGES.filter(function (im) { return im.unit === scope; });
      var rooms = u.filter(function (im) { return im.cat === 'coberturas'; });
      var parts = [
        { key: 'social', label: 'Living e cozinha', items: rooms.filter(function (im) { return has(im, ['living', 'cozinha']); }) },
        { key: 'vista', label: 'Vista para o mar', items: u.filter(function (im) { return im.cat === 'vista'; }) },
        { key: 'solarium', label: 'Solarium e área gourmet', items: rooms.filter(function (im) { return has(im, ['solarium', 'bancada']) && !has(im, ['living']); }) },
        { key: 'suites', label: 'Suítes e banheiros', items: rooms.filter(function (im) { return has(im, ['suite', 'banho', 'lavabo', 'circulacao', 'corredor']); }) },
        { key: 'serra', label: 'Vista para a serra', items: u.filter(function (im) { return im.cat === 'serra'; }) }
      ];
      // "Todas" alterna os ambientes para a primeira tela não repetir o mesmo cômodo.
      var mixed = [], max = Math.max.apply(null, parts.map(function (g) { return g.items.length; }));
      for (var i = 0; i < max; i++) parts.forEach(function (g) { if (g.items[i]) mixed.push(g.items[i]); });
      return [{ key: 'todas', label: 'Todas', items: mixed }].concat(parts, [
        { key: 'planta', label: 'Planta', items: u.filter(function (im) { return im.cat === 'plantas'; }) }
      ]);
    }
    // Galeria da home: só o empreendimento (coberturas e plantas ficam nas landing pages).
    var cats = [['empreendimento', 'Empreendimento'], ['lazer', 'Lazer'], ['localizacao', 'Localização']];
    var homeImgs = IMAGES.filter(function (im) { return !im.unit; });
    var groups = [{ key: 'todas', label: 'Todas', items: homeImgs }];
    cats.forEach(function (c) { groups.push({ key: c[0], label: c[1], items: IMAGES.filter(function (im) { return im.cat === c[0]; }) }); });
    return groups;
  }
  function tabsHTML(groups, active) {
    return groups.filter(function (g) { return g.items.length; }).map(function (g) {
      return '<button type="button" role="tab" data-key="' + g.key + '" aria-selected="' + (g.key === active) + '">' + g.label + '<span class="count">' + g.items.length + '</span></button>';
    }).join('');
  }

  /* Galeria filtrável dentro da landing page */
  $$('[data-inline-gallery]').forEach(function (wrap) {
    var scope = wrap.getAttribute('data-inline-gallery');
    var limit = +wrap.getAttribute('data-limit') || 6;
    var groups = groupsFor(scope).filter(function (g) { return g.key !== 'planta'; });
    var tabs = $('.tabs', wrap), grid = $('.lp-gallery', wrap);
    var render = function (key) {
      var g = groups.filter(function (x) { return x.key === key; })[0];
      tabs.innerHTML = tabsHTML(groups, key);
      var items = g.items.slice(0, limit);
      grid.innerHTML = items.map(function (im, i) { return itemHTML(im, true, i === 0); }).join('');
    };
    tabs.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) render(b.getAttribute('data-key')); });
    render('todas');
  });

  /* Galeria completa (modal, carregada sob demanda) */
  var modal = null;
  function openGallery(scope, startKey) {
    var groups = groupsFor(scope);
    if (!modal) {
      modal = document.createElement('div');
      modal.className = 'modal';
      modal.setAttribute('role', 'dialog');
      modal.setAttribute('aria-modal', 'true');
      modal.innerHTML = '<div class="modal__bar"><h2 class="modal__title"></h2>' +
        '<button class="icon-btn" data-close aria-label="Fechar galeria">' + ICON.close + '</button>' +
        '<div class="tabs" role="tablist"></div></div>' +
        '<div class="modal__body"><p class="modal__note"></p><div class="masonry" data-lb-group></div></div>';
      document.body.appendChild(modal);
      $('[data-close]', modal).addEventListener('click', closeGallery);
    }
    var title = scope === '303' || scope === '304' ? 'Galeria · ' + UNIT_LABEL[scope] : 'Galeria · Ankor Exclusive Residence';
    $('.modal__title', modal).textContent = title;
    $('.modal__note', modal).textContent = scope === '303' || scope === '304'
      ? 'Fotos reais da unidade, entregue sem decoração. A planta humanizada é ilustrativa.'
      : 'Fotos do empreendimento entregue. As fotos e plantas das coberturas estão nas páginas de cada unidade.';
    var tabs = $('.tabs', modal), grid = $('.masonry', modal);
    var render = function (key) {
      var g = groups.filter(function (x) { return x.key === key; })[0] || groups[0];
      tabs.innerHTML = tabsHTML(groups, g.key);
      grid.innerHTML = g.items.map(function (im) { return itemHTML(im, true); }).join('');
      $('.modal__body', modal).scrollTop = 0;
    };
    tabs.onclick = function (e) { var b = e.target.closest('button'); if (b) render(b.getAttribute('data-key')); };
    render(startKey || 'todas');
    modal.classList.add('is-open');
    document.body.classList.add('lock');
    $('[data-close]', modal).focus();
    track('gallery_open', { scope: scope });
  }
  function closeGallery() {
    if (!modal) return;
    modal.classList.remove('is-open');
    document.body.classList.remove('lock');
  }
  $$('[data-open-gallery]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault();
      openGallery(b.getAttribute('data-open-gallery'), b.getAttribute('data-gallery-tab'));
    });
  });

  /* ---------- Vídeos ---------- */
  var vm = null;
  function openVideo(id, title) {
    if (!vm) {
      vm = document.createElement('div');
      vm.className = 'video-modal';
      vm.setAttribute('role', 'dialog');
      vm.setAttribute('aria-modal', 'true');
      vm.innerHTML = '<div class="video-modal__frame"></div><button class="icon-btn" aria-label="Fechar vídeo">' + ICON.close + '</button>';
      document.body.appendChild(vm);
      var close = function () { vm.classList.remove('is-open'); $('.video-modal__frame', vm).innerHTML = ''; document.body.classList.remove('lock'); };
      $('button', vm).addEventListener('click', close);
      vm.addEventListener('click', function (e) { if (e.target === vm) close(); });
      vm._close = close;
    }
    $('.video-modal__frame', vm).innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&modestbranding=1" title="' + title + '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
    vm.classList.add('is-open');
    document.body.classList.add('lock');
    $('button', vm).focus();
    track('video_play', { video: title });
  }
  $$('[data-video]').forEach(function (b) {
    b.addEventListener('click', function () { openVideo(b.getAttribute('data-video'), b.getAttribute('data-title') || 'Vídeo'); });
  });

  /* ---------- Carrossel ---------- */
  $$('[data-carousel]').forEach(function (root) {
    var track_ = $('.carousel__track', root);
    var prev = $('[data-prev]', root.parentNode), next = $('[data-next]', root.parentNode);
    var bar = $('.carousel__progress span', root);
    var step = function () { var c = track_.children[0]; return c ? c.getBoundingClientRect().width + 24 : 300; };
    var update = function () {
      var max = track_.scrollWidth - track_.clientWidth;
      if (prev) prev.disabled = track_.scrollLeft <= 4;
      if (next) next.disabled = track_.scrollLeft >= max - 4;
      if (bar) {
        var ratio = track_.clientWidth / track_.scrollWidth;
        bar.style.width = (ratio * 100) + '%';
        bar.style.transform = 'translateX(' + (max ? (track_.scrollLeft / max) * ((1 - ratio) / ratio) * 100 : 0) + '%)';
      }
    };
    if (prev) prev.addEventListener('click', function () { track_.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { track_.scrollBy({ left: step(), behavior: 'smooth' }); });
    track_.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });

  /* ---------- Mapa: carrega o Google Maps só quando pedido ---------- */
  $$('[data-map]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var box = btn.closest('.map');
      var f = document.createElement('iframe');
      f.src = btn.getAttribute('data-map');
      f.title = 'Mapa de localização do Ankor';
      f.loading = 'lazy';
      f.referrerPolicy = 'no-referrer-when-downgrade';
      box.appendChild(f);
      btn.remove();
      var pin = $('.map__pin', box); if (pin) pin.remove();
    });
  });

  /* ---------- Teclado ---------- */
  document.addEventListener('keydown', function (e) {
    if (lb.classList.contains('is-open')) {
      if (e.key === 'Escape') lbClose();
      if (e.key === 'ArrowLeft') lbShow(lbIndex - 1);
      if (e.key === 'ArrowRight') lbShow(lbIndex + 1);
      return;
    }
    if (e.key === 'Escape') {
      if (vm && vm.classList.contains('is-open')) vm._close();
      else if (modal && modal.classList.contains('is-open')) closeGallery();
      else document.body.classList.remove('nav-open');
    }
  });

  /* ---------- Formulário do respondi.app: repassa as UTMs da página para o formulário ---------- */
  var qs = window.location.search.substring(1);
  if (qs) $$('iframe[data-respondi]').forEach(function (f) { f.src = f.getAttribute('src') + '&' + qs; });

  /* ---------- CTAs que pré-selecionam o interesse no formulário ---------- */
  $$('[data-interest]').forEach(function (a) {
    a.addEventListener('click', function () {
      var v = a.getAttribute('data-interest');
      var input = $('.form input[name="interesse"][value="' + v + '"]');
      if (input) input.checked = true;
      var goal = a.getAttribute('data-goal');
      var goalInput = $('.form input[name="objetivo"]');
      if (goal && goalInput) goalInput.value = goal;
    });
  });

  /* WhatsApp na barra fixa (só aparece se configurado) */
  if (CFG.whatsapp) {
    $$('[data-whatsapp]').forEach(function (a) {
      a.hidden = false;
      a.href = 'https://wa.me/' + CFG.whatsapp + '?text=' + encodeURIComponent(a.getAttribute('data-whatsapp'));
      a.target = '_blank';
      a.rel = 'noopener';
    });
  }
  $$('[data-book]').forEach(function (a) { if (CFG.bookUrl) { a.href = CFG.bookUrl; a.hidden = false; } });

  /* ---------- Formulário ---------- */
  $$('form.form').forEach(function (form) {
    var phone = $('input[name="whatsapp"]', form);
    if (phone) phone.addEventListener('input', function () {
      var d = phone.value.replace(/\D/g, '').slice(0, 11);
      var out = d;
      if (d.length > 2) out = '(' + d.slice(0, 2) + ') ' + d.slice(2);
      if (d.length > 7) out = '(' + d.slice(0, 2) + ') ' + d.slice(2, 7) + '-' + d.slice(7);
      phone.value = out;
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = $('.form__status', form);
      var ok = true;
      $$('[required]', form).forEach(function (el) {
        var valid = el.type === 'checkbox' ? el.checked : el.value.trim() !== '' && el.checkValidity();
        var field = el.closest('.field');
        if (field) field.classList.toggle('has-error', !valid);
        if (!valid) ok = false;
      });
      if (phone && phone.value.replace(/\D/g, '').length < 10) { phone.closest('.field').classList.add('has-error'); ok = false; }
      if (!ok) { status.className = 'form__status is-err'; status.textContent = 'Confira os campos destacados.'; return; }

      var data = new FormData(form);
      var obj = {};
      data.forEach(function (v, k) { obj[k] = v; });
      obj.pagina = location.href;
      var btn = $('button[type="submit"]', form);
      var done = function () {
        form.reset();
        status.className = 'form__status is-ok';
        status.textContent = 'Recebemos seu contato. Um consultor falará com você em breve.';
        btn.disabled = false;
        track('lead_submit', { interesse: obj.interesse || '', objetivo: obj.objetivo || '' });
      };
      var fail = function () {
        status.className = 'form__status is-err';
        status.textContent = 'Não foi possível enviar agora. Tente novamente em instantes.';
        btn.disabled = false;
      };
      var text = 'Olá! Tenho interesse no Ankor Exclusive Residence.\n' +
        'Nome: ' + obj.nome + '\nE-mail: ' + obj.email + '\nWhatsApp: ' + obj.whatsapp +
        (obj.cidade ? '\nCidade: ' + obj.cidade : '') +
        (obj.interesse ? '\nInteresse: ' + obj.interesse : '') +
        (obj.objetivo ? '\nObjetivo: ' + obj.objetivo : '') +
        (obj.mensagem ? '\nMensagem: ' + obj.mensagem : '');

      btn.disabled = true;
      if (CFG.formEndpoint) {
        fetch(CFG.formEndpoint, { method: 'POST', headers: { 'Accept': 'application/json' }, body: data })
          .then(function (r) { if (r.ok) done(); else fail(); })
          .catch(fail);
      } else if (CFG.whatsapp) {
        window.open('https://wa.me/' + CFG.whatsapp + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
        done();
      } else if (CFG.email) {
        location.href = 'mailto:' + CFG.email + '?subject=' + encodeURIComponent('Contato pelo site — ' + (obj.interesse || 'Ankor')) + '&body=' + encodeURIComponent(text);
        done();
      } else {
        btn.disabled = false;
        status.className = 'form__status is-err';
        status.textContent = 'Envio ainda não configurado (defina formEndpoint, whatsapp ou email em assets/js/config.js).';
        if (window.console) console.warn('[Ankor] Configure o destino do formulário em assets/js/config.js');
      }
    });
  });
})();
