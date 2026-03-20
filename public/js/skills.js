document.addEventListener('DOMContentLoaded', () => {

  // Domain Filter Logic
  document.querySelectorAll('.filter-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const domain = tab.getAttribute('data-domain');
      
      // Update active state
      document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      // Filter logic
      document.querySelectorAll('.course-card').forEach(card => {
        const show = domain === 'all' || card.getAttribute('data-domain') === domain;
        if (show) {
          card.style.display = 'flex';
          setTimeout(() => { card.style.opacity = '1'; }, 50);
        } else {
          card.style.display = 'none';
          card.style.opacity = '0';
        }
      });
    });
  });

  // Stagger Entrance Animation
  document.querySelectorAll('.course-card').forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(16px)';
    setTimeout(() => {
      card.style.transition = 'opacity 0.4s cubic-bezier(0.16,1,0.3,1), transform 0.4s cubic-bezier(0.16,1,0.3,1)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 60 + i * 40);
  });

});
