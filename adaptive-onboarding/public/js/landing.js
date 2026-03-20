document.addEventListener('DOMContentLoaded', () => {
    // 1. Initial word splits
    const titles = document.querySelectorAll('[data-split-words]');
    titles.forEach(title => {
        if (window.splitWords) window.splitWords(title);
    });

    // 2. Metora Parallax Logic Layers
    const hero = document.querySelector('.hero');
    if (hero) {
        let reqId;
        let mouseX = window.innerWidth / 2;
        let mouseY = window.innerHeight / 2;
        
        let cx = window.innerWidth / 2;
        let cy = window.innerHeight / 2;

        const bgText = document.querySelector('.hero-bg-text');
        const visual = document.querySelector('.hero-visual');
        const floatCards = document.querySelector('.hero-float-cards');
        const atmosphere = document.querySelector('.hero-atmosphere');

        hero.addEventListener('mousemove', e => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        // Using RAF for smoother parallax
        function parallaxLoop() {
            // Lerp center tracking
            cx += (mouseX - cx) * 0.1;
            cy += (mouseY - cy) * 0.1;

            const xPct = (cx / window.innerWidth - 0.5);
            const yPct = (cy / window.innerHeight - 0.5);

            if (bgText) bgText.style.transform = `translate(-50%, -50%) translate(${xPct * 16}px, ${yPct * 10}px)`;
            if (visual) visual.style.transform = `translateY(-50%) translate(${xPct * 40}px, ${yPct * 24}px)`;
            if (floatCards) floatCards.style.transform = `translate(${xPct * 28}px, ${yPct * 18}px)`;
            if (atmosphere) atmosphere.style.background = `radial-gradient(900px circle at ${50 + xPct * 10}% ${50 + yPct * 10}%, rgba(61,10,92,0.55), transparent 70%)`;

            reqId = requestAnimationFrame(parallaxLoop);
        }
        parallaxLoop();
    }

    // 3. Staggered Intersection Observer for Module Grid & Spotlight Hover
    const modulesTrack = document.getElementById('modules-track');
    const moduleCards = document.querySelectorAll('.module-demo-card[data-stagger]');
    
    if (modulesTrack && moduleCards.length > 0) {
        
        // Spotlight Hover Effect
        modulesTrack.addEventListener('mousemove', e => {
            for (const card of moduleCards) {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            }
        });

        // Stagger Reveal
        const gridObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    moduleCards.forEach((card, i) => {
                        setTimeout(() => {
                            card.classList.add('visible');
                        }, i * 80); // Stagger 80ms
                    });
                    gridObserver.disconnect();
                }
            });
        }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });
        
        gridObserver.observe(modulesTrack);
    }

    // 4. Gap Stat Parallax Glow
    const gapCard = document.querySelector('.gap-modern-card');
    const ambientGlow = document.querySelector('.card-ambient-glow');
    if (gapCard && ambientGlow) {
        gapCard.addEventListener('mousemove', e => {
            const rect = gapCard.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const moveX = (x - rect.width/2) * 0.15;
            const moveY = (y - rect.height/2) * 0.15;
            ambientGlow.style.transform = `rotate(30deg) translate(${moveX}px, ${moveY}px)`;
        });
    }
});
