import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# Set page config
st.set_page_config(
    page_title="Gurleen Kaur Baxi | Portfolio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# CSS overrides that fix rendering inside Streamlit's iframe
IFRAME_CSS_OVERRIDES = """
<style>
    /* Force all fade-in elements visible (IntersectionObserver won't fire in iframe) */
    .fade-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }

    /* Force h1 clip-path fully open */
    h1 {
        clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%) !important;
        opacity: 1 !important;
    }

    /* Sticky nav instead of fixed (fixed breaks in iframes) */
    nav {
        position: sticky !important;
        top: 0;
    }

    /* Disable effects that don't work in iframes */
    body::before { display: none !important; }
    .cursor-blob { display: none !important; }
    
    /* Ensure all sections are visible */
    section, .hero, .about, .experience, .awards, .certifications, .projects, .gallery, .contact {
        opacity: 1 !important;
        visibility: visible !important;
        transform: none !important;
    }
    
    /* Ensure all cards are visible */
    .award-card, .project-card, .stat-card, .cert-item, .timeline-item {
        opacity: 1 !important;
        visibility: visible !important;
        transform: none !important;
    }
</style>
"""

# JS override that safely wraps the original JS to prevent errors from crashing the page
IFRAME_JS_OVERRIDE = """
<script>
// Override the original DOMContentLoaded listener to be iframe-safe
document.addEventListener('DOMContentLoaded', () => {
    // Safely try to initialize Lucide icons
    try {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    } catch(e) {
        console.warn('Lucide init skipped:', e);
    }

    // Force all fade-in elements to be visible immediately
    document.querySelectorAll('.fade-in').forEach(el => {
        el.classList.add('visible');
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
    });
    
    // Force h1 to be visible
    const h1 = document.querySelector('h1');
    if (h1) {
        h1.style.clipPath = 'polygon(0 0, 100% 0, 100% 100%, 0 100%)';
        h1.style.opacity = '1';
    }

    // Navbar scroll effect (works in iframe with sticky)
    const nav = document.querySelector('nav');
    if (nav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
    }

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});
</script>
"""

def main():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        with open("script.js", "r", encoding="utf-8") as f:
            js_original = f.read()
    except Exception as e:
        st.error(f"Error loading portfolio assets: {e}")
        return

    # Base64 encode the avatar
    if os.path.exists("avatar.png"):
        img_base64 = get_base64_of_bin_file("avatar.png")
        html = html.replace('src="avatar.png"', f'src="data:image/png;base64,{img_base64}"')

    # Inject CSS inline
    html = html.replace('<link rel="stylesheet" href="style.css">', f'<style>{css}</style>')

    # REMOVE the original script.js entirely — replace with iframe-safe version
    html = html.replace('<script src="script.js"></script>', '')

    # Inject iframe CSS overrides before </head>
    html = html.replace('</head>', f'{IFRAME_CSS_OVERRIDES}\n</head>')

    # Inject iframe-safe JS before </body>
    html = html.replace('</body>', f'{IFRAME_JS_OVERRIDE}\n</body>')

    # Hide Streamlit branding
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp { margin: 0; padding: 0; }
            .block-container {
                padding: 0px !important;
                margin: 0px !important;
                max-width: 100% !important;
            }
            [data-testid="stVerticalBlock"] {
                gap: 0 !important;
            }
            iframe {
                border: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Render the portfolio
    components.html(html, height=8500, scrolling=True)

if __name__ == "__main__":
    main()
