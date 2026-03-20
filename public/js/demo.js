document.addEventListener('DOMContentLoaded', () => {

  // 1. Stagger persona cards
  document.querySelectorAll('.persona-card').forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    setTimeout(() => {
      card.style.transition = 'opacity 0.5s cubic-bezier(0.16,1,0.3,1), transform 0.5s cubic-bezier(0.16,1,0.3,1)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 100 + i * 120);
  });

  // 2. Animate all three rings
  document.querySelectorAll('.ring-arc').forEach(arc => {
    const score = parseInt(arc.getAttribute('data-score'));
    const circumference = 251.2;
    arc.style.strokeDashoffset = circumference;
    setTimeout(() => {
      arc.style.transition = 'stroke-dashoffset 1.2s cubic-bezier(0.16,1,0.3,1)';
      arc.style.strokeDashoffset = circumference - (score / 100) * circumference;
    }, 400);
  });

  // 3. Animate comparison bars
  setTimeout(() => {
    document.querySelectorAll('.bar-fill').forEach(bar => {
      bar.style.width = bar.getAttribute('data-width') + '%';
    });
  }, 600);

  // VIEW FULL ROADMAP toggle logic
  document.querySelectorAll('.persona-card').forEach(card => {
    card.querySelector('.view-roadmap-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      const profile = card.getAttribute('data-profile');
      const panel = document.getElementById(`panel-${profile}`);
      const isOpen = panel.classList.toggle('open');

      // Close other panels
      document.querySelectorAll('.roadmap-panel').forEach(p => {
        if (p.id !== `panel-${profile}`) p.classList.remove('open');
      });

      // Toggle active state on cards
      document.querySelectorAll('.persona-card').forEach(c => c.classList.remove('active'));
      if (isOpen) card.classList.add('active');

      // Scroll panel into view smoothly
      if (isOpen) {
        setTimeout(() => panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);
      }
    });
  });

  // COLLAPSE buttons inside panels
  document.querySelectorAll('.collapse-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const panel = e.target.closest('.roadmap-panel');
      panel.classList.remove('open');
      document.querySelectorAll('.persona-card').forEach(c => c.classList.remove('active'));
    });
  });

  // Filter Domain Pills
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      // toggle active class
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.getAttribute('data-filter');

      // hide/show cards
      document.querySelectorAll('.persona-card').forEach(card => {
        if (card.getAttribute('data-domain') === filter) {
          card.style.display = 'flex';
          setTimeout(() => { card.style.opacity = '1'; }, 50);
        } else {
          card.style.display = 'none';
          card.style.opacity = '0';
        }
      });
      
      // Close all panels on filter change
      document.querySelectorAll('.roadmap-panel').forEach(p => p.classList.remove('open'));
    });
  });
});
