/* なお｜動き
   GSAP 3.13.0 ＋ ScrollTrigger（index.html / weekly で読み込む）。
   - 動きを減らす設定の人には何もしない（<html> に .motion が付かない）
   - GSAP が読めなかったら .motion を外して、隠した要素を全部見せる
   - 動かすのは transform と opacity だけ（古いスマホでもカクつかない） */
(function () {
  var root = document.documentElement;
  if (!root.classList.contains('motion')) return;
  if (!window.gsap || !window.ScrollTrigger) { root.classList.remove('motion'); return; }

  var gsap = window.gsap;
  gsap.registerPlugin(window.ScrollTrigger);

  function all(sel, base) { return Array.prototype.slice.call((base || document).querySelectorAll(sel)); }

  var mm = gsap.matchMedia();

  mm.add('(prefers-reduced-motion: no-preference)', function () {
    /* 最初の画面：にじみ形 → 帯 → 大人 → 新人ちゃん → 小物 → 名前（約1.6秒） */
    var hero = document.querySelector('.hero');
    if (hero) {
      var q = function (s) { return all(s, hero); };
      var tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
      tl.fromTo(q('.blob'), { scale: .6, opacity: 0, transformOrigin: '50% 50%' }, { scale: 1, opacity: 1, duration: .9 })
        .fromTo(q('.hero-tag span'), { y: -40, opacity: 0 }, { y: 0, opacity: 1, duration: .6, stagger: .12 }, '-=.6')
        .fromTo(q('.hero-adult'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: .7, ease: 'back.out(1.8)' }, '-=.4')
        .fromTo(q('.hero-kid'), { x: 50, opacity: 0, rotation: 12 }, { x: 0, opacity: 1, rotation: 0, duration: .6, ease: 'back.out(2)' }, '-=.3')
        .fromTo(q('.prop'), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, stagger: .07, ease: 'back.out(2.5)' }, '-=.3')
        .fromTo(q('.hero-en, .hero-name-box'), { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: .5, stagger: .1 }, '-=.6')
        .add(function () {
          /* 待機中：呼吸くらいの小さな揺れ */
          gsap.to(q('.hero-adult'), { y: -5, duration: 2.4, repeat: -1, yoyo: true, ease: 'sine.inOut' });
          gsap.to(q('.hero-kid'), { rotation: -3, duration: 1.7, repeat: -1, yoyo: true, ease: 'sine.inOut', transformOrigin: '50% 100%' });
          q('.prop').forEach(function (el, i) {
            gsap.to(el, { y: -6, rotation: '+=6', duration: 2.8 + i * .3, repeat: -1, yoyo: true, ease: 'sine.inOut', delay: i * .2 });
          });
        });
    }

    /* スクロール：区切りの顔が横から跳ねて出る。見出しやカードは下から順に（一度だけ） */
    all('.sec').forEach(function (sec) {
      var art = sec.querySelector('.sec-art');
      if (art) {
        gsap.fromTo(art, { x: 80, rotation: 14, opacity: 0 }, {
          x: 0, rotation: 0, opacity: 1, duration: .75, ease: 'back.out(1.7)',
          scrollTrigger: { trigger: sec, start: 'top 78%', once: true }
        });
      }
      var items = all('.eyebrow, h2, .lead, .note, .reveal', sec).filter(function (el) {
        return el.closest('.sec') === sec;
      });
      if (items.length) {
        gsap.fromTo(items, { y: 24, opacity: 0 }, {
          y: 0, opacity: 1, duration: .6, stagger: .08, ease: 'power2.out',
          scrollTrigger: { trigger: sec, start: 'top 72%', once: true }
        });
      }
      all('.peek', sec).forEach(function (peek) {
        gsap.fromTo(peek, { x: 70, opacity: 0 }, {
          x: 0, opacity: 1, duration: .6, ease: 'back.out(2)',
          scrollTrigger: { trigger: peek, start: 'top 92%', once: true }
        });
      });
    });

    /* 最後のほうの区切りは、画面の高さによっては一度も「72%」に届かない。
       ページの終わりまで来たら、残っている要素を全部出す */
    window.ScrollTrigger.create({
      trigger: document.body, start: 'bottom bottom', once: true,
      onEnter: function () { gsap.to(all('.sec-art, .reveal, .peek, .sec .eyebrow, .sec h2, .sec .lead, .sec .note'), { opacity: 1, x: 0, y: 0, rotation: 0, duration: .4, overwrite: 'auto' }); }
    });
  });
})();
