document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // Custom Cursor Blob Movement (Refined for smoothness)
    const blob = document.querySelector('.cursor-blob');
    let curX = 0, curY = 0, tgX = 0, tgY = 0;

    document.addEventListener('mousemove', (e) => {
        tgX = e.clientX;
        tgY = e.clientY;
    });

    function updateCursor() {
        curX += (tgX - curX) * 0.1;
        curY += (tgY - curY) * 0.1;
        blob.style.transform = `translate(${curX - 200}px, ${curY - 200}px)`;
        requestAnimationFrame(updateCursor);
    }
    updateCursor();

    // Magnetic Buttons and Items Effect
    const magneticElements = document.querySelectorAll('.btn-main, .btn-primary, .contact-item, .stat-card');
    magneticElements.forEach(el => {
        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            el.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
        });
        el.addEventListener('mouseleave', () => {
            el.style.transform = `translate(0px, 0px)`;
        });
    });

    // Parallax effect for floating icons in hero
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        document.querySelectorAll('.floating-icon').forEach((icon, index) => {
            const speed = (index + 1) * 0.15;
            icon.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });

    // Navbar scroll effect
    const nav = document.querySelector('nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

    // Intersection Observer for staggered scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger appearance if multiple entries visible at once
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);
            }
        });
    }, observerOptions);

    // Apply animation classes to sections and key cards
    document.querySelectorAll('section, .award-card, .project-card, .stat-card, .cert-item').forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });

    // Smooth scroll for nav links (skip if opening new tabs)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            if (this.target === '_blank') {
                return;
            }
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 85;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // Gallery carousel controls
    const track = document.querySelector('.carousel-track');
    const slides = track ? Array.from(track.children) : [];
    let currentSlide = 0;

    const prevButton = document.querySelector('.carousel-btn.prev');
    const nextButton = document.querySelector('.carousel-btn.next');

    const visibleImages = 2;
    const maxSlideIndex = Math.max(0, slides.length - visibleImages);

    function updateCarousel() {
        if (!track) return;
        currentSlide = Math.max(0, Math.min(currentSlide, maxSlideIndex));
        const offset = -currentSlide * 50;
        track.style.transform = `translateX(${offset}%)`;
    }

    if (nextButton) {
        nextButton.addEventListener('click', () => {
            if (currentSlide >= maxSlideIndex) {
                currentSlide = 0;
            } else {
                currentSlide += 1;
            }
            updateCarousel();
        });
    }

    if (prevButton) {
        prevButton.addEventListener('click', () => {
            if (currentSlide <= 0) {
                currentSlide = maxSlideIndex;
            } else {
                currentSlide -= 1;
            }
            updateCarousel();
        });
    }

    // Awards horizontal card carousel controls
    const awardsTrack = document.querySelector('.awards-track');
    const awardsPrev = document.querySelector('.awards-btn.prev');
    const awardsNext = document.querySelector('.awards-btn.next');

    if (awardsTrack && awardsPrev && awardsNext) {
        const scrollAmount = () => {
            const card = awardsTrack.querySelector('.award-card');
            return card ? card.offsetWidth + 16 : awardsTrack.clientWidth * 0.8;
        };

        awardsPrev.addEventListener('click', () => {
            awardsTrack.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
        });

        awardsNext.addEventListener('click', () => {
            awardsTrack.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
        });
    }

    // Optional auto-rotation of carousel each 6 seconds
    setInterval(() => {
        if (slides.length > 0) {
            currentSlide = (currentSlide + 1) % slides.length;
            updateCarousel();
        }
    }, 6000);
});
