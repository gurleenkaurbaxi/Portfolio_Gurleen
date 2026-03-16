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

def main():
    # 1. Read files
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
    except Exception as e:
        st.error(f"Critical error reading files: {e}")
        return

    # 2. Extract Body Content
    # We do a case-insensitive search for <body> and </body>
    import re
    body_match = re.search(r'<body>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_content = body_match.group(1)
    else:
        # Fallback if body tags are missing/malformed
        body_content = html

    # 3. Iframe Overrides
    overrides = """
    <style>
        /* Force visibility on all elements that use the fade-in animation */
        .fade-in { 
            opacity: 1 !important; 
            transform: none !important; 
            visibility: visible !important; 
            transition: none !important;
        }
        
        /* Force h1 reveal */
        h1 { 
            clip-path: none !important; 
            opacity: 1 !important; 
            visibility: visible !important;
        }

        /* Use sticky nav for better iframe compatibility */
        nav { 
            position: sticky !important; 
            top: 0; 
            z-index: 1000;
        }

        /* Disable effects that often fail in cross-origin iframes */
        body::before { display: none !important; }
        .cursor-blob { display: none !important; }
        .magnetic { transform: none !important; }

        /* Ensure all containers have base visibility */
        section, div, span, h1, h2, h3, p, a {
            opacity: 1 !important;
            visibility: visible !important;
        }
    </style>
    """

    # 4. Re-assemble Final HTML
    # We inject Lucide and our CSS directly
    final_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>{css}</style>
        {overrides}
    </head>
    <body style="margin:0; padding:0; background-color: #FFFAF5;">
        {body_content}
        <script>
            // Ensure icons load and visibility is triggered
            window.onload = () => {{
                try {{ if(window.lucide) lucide.createIcons(); }} catch(e) {{}}
                document.querySelectorAll('.fade-in').forEach(el => {{
                    el.classList.add('visible');
                }});
            }};
        </script>
    </body>
    </html>
    """

    # 5. Handle Avatar Path
    if os.path.exists("avatar.png"):
        img_base64 = get_base64_of_bin_file("avatar.png")
        final_html = final_html.replace('src="avatar.png"', f'src="data:image/png;base64,{img_base64}"')

    # 6. Streamlit Page Styling
    # We remove Streamlit's internal height constraints on the component
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
            [data-testid="stVerticalBlock"] { gap: 0 !important; }
            /* IMPORTANT: Don't force height: 100vh here, let the component height decide */
            iframe { border: none !important; }
        </style>
    """, unsafe_allow_html=True)

    # 7. Final Render
    # height=None would be ideal but components.html requires a value or it defaults to 150px.
    # We use a very large height and scrolling=False to make it look like a single page.
    components.html(final_html, height=10000, scrolling=False)

if __name__ == "__main__":
    main()
