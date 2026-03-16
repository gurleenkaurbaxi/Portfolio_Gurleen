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
    # 1. Read files with error logging
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()
        with open("style.css", "r", encoding="utf-8") as f:
            css = f.read()
    except Exception as e:
        st.error(f"Critical error reading files: {e}")
        return

    # 2. Basic Bundling
    # Instead of complicated replacements, we'll strip the original head/body tags 
    # and re-assemble them to ensure 100% correctness.
    
    # Extract content between <body> and </body>
    start_body = html.find('<body>') + 6
    end_body = html.find('</body>')
    body_content = html[start_body:end_body]
    
    # CSS overrides for iframe compatibility
    overrides = """
    <style>
        .fade-in { opacity: 1 !important; transform: none !important; visibility: visible !important; }
        h1 { clip-path: none !important; opacity: 1 !important; }
        nav { position: sticky !important; top: 0; }
        body::before, .cursor-blob { display: none !important; }
        section { opacity: 1 !important; visibility: visible !important; transform: none !important; }
    </style>
    """
    
    # Re-assemble the HTML string
    final_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>{css}</style>
        {overrides}
    </head>
    <body style="margin:0; padding:0;">
        {body_content}
        <script>
            document.addEventListener('DOMContentLoaded', () => {{
                try {{ lucide.createIcons(); }} catch(e) {{}}
                document.querySelectorAll('.fade-in').forEach(el => {{
                    el.classList.add('visible');
                    el.style.opacity = '1';
                }});
            }});
        </script>
    </body>
    </html>
    """

    # 3. Handle Avatar
    if os.path.exists("avatar.png"):
        img_base64 = get_base64_of_bin_file("avatar.png")
        final_html = final_html.replace('src="avatar.png"', f'src="data:image/png;base64,{img_base64}"')

    # 4. Global Streamlit Overrides
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp { margin: 0; padding: 0; }
            .block-container { padding: 0 !important; }
            iframe { border: none !important; width: 100%; height: 100vh; }
        </style>
    """, unsafe_allow_html=True)

    # 5. Render
    components.html(final_html, height=8500, scrolling=True)

if __name__ == "__main__":
    main()
