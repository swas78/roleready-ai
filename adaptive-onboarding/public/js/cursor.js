document.addEventListener('DOMContentLoaded', () => {
    const cursor = document.createElement('div');
    cursor.id = 'cursor';
    document.body.appendChild(cursor);

    const speeds = [0.15, 0.1, 0.07]; // Multipliers for layer lerp
    const trails = [];
    for (let i = 1; i <= 3; i++) {
        const t = document.createElement('div');
        t.className = 'cursor-trail';
        t.id = `cursor-trail-${i}`;
        document.body.appendChild(t);
        trails.push({ 
            el: t, 
            cx: window.innerWidth / 2, 
            cy: window.innerHeight / 2, 
            tx: window.innerWidth / 2,  
            ty: window.innerHeight / 2,
            speed: speeds[i-1]
        });
    }

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;

    document.addEventListener('mousemove', e => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        
        cursor.style.left = mouseX + 'px';
        cursor.style.top = mouseY + 'px';
        
        trails[0].tx = mouseX;
        trails[0].ty = mouseY;
    });

    const animateTrails = () => {
        for(let i = 0; i < trails.length; i++) {
            let tr = trails[i];
            
            tr.cx += (tr.tx - tr.cx) * tr.speed;
            tr.cy += (tr.ty - tr.cy) * tr.speed;
            
            tr.el.style.left = tr.cx + 'px';
            tr.el.style.top = tr.cy + 'px';
            
            if (i < trails.length - 1) {
                trails[i+1].tx = tr.cx;
                trails[i+1].ty = tr.cy;
            }
        }
        
        requestAnimationFrame(animateTrails);
    };
    animateTrails();

    const addHoverEffect = () => {
        const hoverElements = document.querySelectorAll('a, button, [data-hover]');
        hoverElements.forEach(el => {
            if (!el.dataset.cursorBound) {
                el.dataset.cursorBound = '1';
                el.addEventListener('mouseenter', () => cursor.classList.add('hovering'));
                el.addEventListener('mouseleave', () => cursor.classList.remove('hovering'));
            }
        });
    };
    
    addHoverEffect();
    window.refreshCursor = addHoverEffect;

    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) navbar.classList.add('scrolled');
            else navbar.classList.remove('scrolled');
        });
    }
});
