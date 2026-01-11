import os
import re
from bs4 import BeautifulSoup

def create_navigation_bar(prev_link, next_link, index_link="index.html"):
    """
    Creates the HTML for a floating navigation bar.
    """
    # Logic for Previous Button
    if prev_link:
        prev_html = f'<a href="{prev_link}" style="text-decoration: none; color: #94a3b8; font-weight: bold; font-family: sans-serif; transition: color 0.2s;" onmouseover="this.style.color=\'#fff\'" onmouseout="this.style.color=\'#94a3b8\'">← Prev</a>'
    else:
        prev_html = '<span style="color: #334155; cursor: default;">← Prev</span>'

    # Logic for Next Button
    if next_link:
        next_html = f'<a href="{next_link}" style="text-decoration: none; color: #94a3b8; font-weight: bold; font-family: sans-serif; transition: color 0.2s;" onmouseover="this.style.color=\'#fff\'" onmouseout="this.style.color=\'#94a3b8\'">Next →</a>'
    else:
        next_html = '<span style="color: #334155; cursor: default;">Next →</span>'

    # Assemble the Bar
    nav_html = f"""
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; 
                background: rgba(15, 23, 42, 0.9); border: 1px solid #38bdf8; 
                border-radius: 50px; padding: 10px 20px; display: flex; gap: 15px; 
                box-shadow: 0 10px 25px rgba(0,0,0,0.5); backdrop-filter: blur(10px);">
        
        {prev_html}
        
        <span style="color: #334155;">|</span>
        <a href="{index_link}" style="text-decoration: none; color: #38bdf8; font-weight: bold; font-family: sans-serif; transition: color 0.2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#38bdf8'">Home</a>
        <span style="color: #334155;">|</span>

        {next_html}
    </div>
    """
    return nav_html

def build_website():
    # 1. Get all HTML files and sort them naturally
    files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html']
    files.sort(key=lambda f: int(re.search(r'\d+', f).group()) if re.search(r'\d+', f) else 999)

    print(f"Linking {len(files)} slides...")

    slide_titles = []

    # 2. Loop through files to inject navigation
    for i, filename in enumerate(files):
        with open(filename, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Extract title for the index page later
        page_title = soup.title.string if soup.title else filename
        slide_titles.append((filename, page_title))

        # Determine Previous and Next files
        prev_file = files[i-1] if i > 0 else None
        next_file = files[i+1] if i < len(files) - 1 else None

        # Create the Nav Bar HTML
        nav_bar_html = create_navigation_bar(prev_file, next_file)
        nav_bar = BeautifulSoup(nav_bar_html, 'html.parser')

        # Remove any existing nav bars from previous runs
        existing_nav = soup.find('div', style=re.compile('position: fixed; bottom: 20px;'))
        if existing_nav:
            existing_nav.decompose()

        # Append new nav bar to body
        if soup.body:
            soup.body.append(nav_bar)
        
        # Save the file back
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
        print(f"Added navigation to {filename}")

    # 3. Create the Main Index Page (Table of Contents)
    index_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RIMS Presentation - Home</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            body { background-color: #0f172a; color: white; font-family: 'Inter', sans-serif; padding: 4rem; }
            .card { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(148, 163, 184, 0.1); padding: 1.5rem; border-radius: 12px; transition: all 0.2s; }
            .card:hover { transform: translateY(-5px); border-color: #38bdf8; background: rgba(30, 41, 59, 0.8); }
            h1 { font-size: 3rem; font-weight: 800; margin-bottom: 2rem; color: #f8fafc; text-align: center; }
            .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
            a { text-decoration: none; color: inherit; display: block; height: 100%; }
            .slide-num { color: #38bdf8; font-weight: bold; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 0.5rem; display: block; }
            .slide-title { font-size: 1.25rem; font-weight: 600; }
        </style>
    </head>
    <body>
        <h1>Presentation Overview</h1>
        <div class="grid-container">
    """

    for i, (fname, title) in enumerate(slide_titles):
        index_html += f"""
        <a href="{fname}">
            <div class="card">
                <span class="slide-num">Slide {i+1}</span>
                <div class="slide-title">{title}</div>
            </div>
        </a>
        """

    index_html += """
        </div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)

    print("Success! Created index.html and linked all slides.")

if __name__ == "__main__":
    build_website()