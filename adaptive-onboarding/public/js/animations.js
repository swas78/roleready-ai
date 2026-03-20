window.countUp = function(el, target, duration = 2000) {
    let startTimestamp = null;
    const endValue = parseInt(target, 10);
    const startValue = 0;
    
    // cubic ease-out: 1 - Math.pow(1-t, 3)
    const easeOutCubic = t => 1 - Math.pow(1 - t, 3);

    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        let progress = Math.min((timestamp - startTimestamp) / duration, 1);
        
        let easedProgress = easeOutCubic(progress);
        let currentVal = Math.floor(easedProgress * (endValue - startValue) + startValue);
        
        el.textContent = currentVal;
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            el.textContent = endValue;
        }
    };
    window.requestAnimationFrame(step);
};

window.splitWords = function(el) {
    const text = el.textContent;
    el.innerHTML = '';
    const words = text.split(' ');
    
    el.style.perspective = '600px';
    
    words.forEach((word, index) => {
        const span = document.createElement('span');
        span.className = 'word';
        span.textContent = word + (index < words.length - 1 ? ' ' : '');
        span.style.setProperty('--d', `${index * 80}ms`);
        el.appendChild(span);
    });
};

window.addTilt = function(el) {
    el.addEventListener('mousemove', e => {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const multiplier = 10;
        
        const xPct = (x / rect.width) - 0.5;
        const yPct = (y / rect.height) - 0.5;
        
        const rotateX = -yPct * multiplier;
        const rotateY = xPct * multiplier;
        
        el.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`;
        el.style.transition = 'none';
    });

    el.addEventListener('mouseleave', () => {
        el.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale(1)`;
        el.style.transition = 'transform 0.5s ease';
    });
};

document.addEventListener('DOMContentLoaded', () => {
    // Reveal Elements using upgraded Observer Options
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.getAttribute('data-delay') || 0;
                setTimeout(() => {
                    entry.target.classList.add('revealed');
                }, parseInt(delay, 10));
                
                if (entry.target.hasAttribute('data-countup') && !entry.target.counted) {
                    window.countUp(entry.target, entry.target.getAttribute('data-countup'));
                    entry.target.counted = true;
                } else {
                    const children = entry.target.querySelectorAll('[data-countup]');
                    children.forEach(child => {
                        if (!child.counted) {
                            window.countUp(child, child.getAttribute('data-countup'));
                            child.counted = true;
                        }
                    });
                }
            }
        });
    }, { 
        threshold: 0.1,
        rootMargin: "0px 0px -40px 0px"
    });

    document.querySelectorAll('[data-reveal], [data-countup]').forEach(el => observer.observe(el));
});
