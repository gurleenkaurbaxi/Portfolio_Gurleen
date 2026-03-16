import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# Set page config for a professional full-width look
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

# --- Iframe-safe CSS overrides ---
# These fix rendering issues caused by animations/observers not working inside Streamlit's iframe.
IFRAME_CSS_OVERRIDES = """
<style>
    /* FIX 1: Force all fade-in elements to be visible.
       The IntersectionObserver JS never fires inside an iframe,
       so sections stay at opacity:0 forever. This forces them visible. */
    .fade-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }

    /* FIX 2: Force the h1 clip-path to be fully open.
       The nameSilkReveal animation may not fire in the iframe context. */
    h1 {
        clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%) !important;
        opacity: 1 !important;
    }

    /* FIX 3: Change nav from fixed to sticky for iframe compatibility.
       position:fixed inside an iframe with no scroll can collapse layout. */
    nav {
        position: sticky !important;
    }

    /* FIX 4: Remove the grain texture overlay.
       The SVG noise filter can cause rendering issues in some iframe contexts. */
    body::before {
        display: none !important;
    }

    /* FIX 5: Remove cursor blob (doesn't track properly in iframe). */
    .cursor-blob {
        display: none !important;
    }
</style>
"""

def main():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
        with open("script.js", "r", encoding="utf-8") as f:
            js = f.read()
    except Exception as e:
        st.error(f"Error loading portfolio assets: {e}")
        return

    # In-line images as Base64 to ensure they load within the Streamlit iframe
    if os.path.exists("avatar.png"):
        img_base64 = get_base64_of_bin_file("avatar.png")
        html = html.replace('src="avatar.png"', f'src="data:image/png;base64,{img_base64}"')

    # Bundle Styles and Scripts into the HTML
    html = html.replace('<link rel="stylesheet" href="style.css">', f'<style>{css}</style>')
    html = html.replace('<script src="script.js"></script>', f'<script>{js}</script>')

    # Inject iframe-safe CSS overrides right before </head>
    html = html.replace('</head>', f'{IFRAME_CSS_OVERRIDES}\n</head>')

    # Global Streamlit UI Overrides — hide branding, remove padding
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

    # Render the portfolio inside Streamlit
    components.html(html, height=8500, scrolling=False)

if __name__ == "__main__":
    main()
