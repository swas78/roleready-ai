// Helper: animated count-up
function countUp(el, target, duration = 1200) {
  if (!el) return;
  let start = null;
  const step = timestamp => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // cubic ease-out
    el.textContent = Math.floor(eased * target);
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target;
  };
  requestAnimationFrame(step);
}

// Activity Feed logic
function addActivity(text) {
  const feed = document.getElementById('activityFeed');
  if (!feed) return;
  const item = document.createElement('div');
  item.className = 'activity-item';
  item.textContent = text;
  
  feed.prepend(item);
  if (feed.children.length > 6) {
    feed.children[feed.children.length - 1].remove();
  }
}

// Ring Animation Helper
function animateRing(score) {
  const circle = document.querySelector('.ring-progress');
  if (!circle) return;
  const circumference = 2 * Math.PI * 90; // r=90
  circle.style.strokeDasharray = circumference;
  circle.style.strokeDashoffset = circumference;
  
  setTimeout(() => {
    const offset = circumference - (score / 100) * circumference;
    circle.style.transition = 'stroke-dashoffset 1.4s cubic-bezier(0.16,1,0.3,1)';
    circle.style.strokeDashoffset = offset;
  }, 300);
}

let completedCount = 0;

function markComplete(index, hours, title, btn) {
  const card = btn.closest('.module-card');
  if (card.classList.contains('completed')) return; // Already completed

  // Mark as complete visually
  card.classList.add('completed');
  card.querySelector('.module-order-circle').innerHTML = '&#10003;'; // Checkmark
  
  completedCount++;
  
  // Update Hours Saved
  const currentHours = parseInt(document.querySelector('.hours-saved-number').textContent);
  const newHours = currentHours + hours;
  countUp(document.querySelector('.hours-saved-number'), newHours, 600);
  
  // Recalculate and update Readiness Score
  // Formula prescribed: newScore = baseScore + (completedCount / total) * (100 - baseScore) * 0.6
  if (TOTAL_MODULES > 0) {
    const boost = (completedCount / TOTAL_MODULES) * (100 - BASE_SCORE) * 0.6;
    const newScore = Math.min(100, Math.floor(BASE_SCORE + boost));
    
    countUp(document.querySelector('.readiness-number'), newScore, 800);
    countUp(document.querySelector('.readiness-number-pill'), newScore, 800);
    countUp(document.querySelector('.readiness-number-ring'), newScore, 800);
    
    animateRing(newScore);
    
    const readinessBar = document.querySelector('.readiness-bar-fill');
    if (readinessBar) {
      readinessBar.style.width = newScore + '%';
    }
  }

  // Push activity
  addActivity(`✓ Completed: ${title} · +${hours}h saved`);
}

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initial count-up
  countUp(document.querySelector('.readiness-number'), BASE_SCORE);
  countUp(document.querySelector('.readiness-number-pill'), BASE_SCORE);
  countUp(document.querySelector('.readiness-number-ring'), BASE_SCORE);
  countUp(document.querySelector('.hours-saved-number'), RESULT_DATA.time_saved_hours || 0);

  // 2. Progress bars expansion
  setTimeout(() => {
    document.querySelectorAll('[data-width]').forEach(el => {
      el.style.width = el.getAttribute('data-width') + '%';
    });
  }, 50);

  // 3. Render ring load
  animateRing(BASE_SCORE);

  // 4. Activity seed
  addActivity(`Analysis complete · ${TOTAL_MODULES} modules generated`);

  // 5. Expand panels logically
  document.querySelectorAll('.module-card').forEach(card => {
    const toggle = card.querySelector('.why-toggle');
    if (toggle) {
      toggle.addEventListener('click', () => {
        const panel = card.querySelector('.reason-panel');
        const isOpen = panel.classList.toggle('open');
        toggle.textContent = isOpen ? '↑ Hide reasoning' : '↓ Why this module?';
        if (isOpen) {
          addActivity(`Module opened: ${card.dataset.title}`);
        }
      });
    }
  });

  // 6. Complete bindings
  document.querySelectorAll('.complete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      markComplete(
        parseInt(btn.getAttribute('data-index')),
        parseInt(btn.getAttribute('data-hours')),
        btn.getAttribute('data-title'),
        btn
      );
    });
  });
});
