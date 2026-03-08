import glob
import re

for file in glob.glob('*.html'):
    with open(file, 'r') as f:
        content = f.read()

    # 1. Fix the main header flex container inside the <header> tag
    # For index.html, creative-cta.html which have the mx-auto container
    content = content.replace('<div class="mx-auto flex max-w-7xl items-center justify-between">', 
                              '<div class="mx-auto flex flex-col md:flex-row max-w-7xl items-center justify-between gap-6 md:gap-0 py-2 md:py-0">')
    content = content.replace('<div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 md:gap-0">',
                              '<div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 md:gap-0 py-2 md:py-0">')
    
    # Prevent whitespace-nowrap from breaking flex wrapping
    content = content.replace('whitespace-nowrap', '')

    # 2. Fix the title "House of Pentool" in header specifically
    # Find header block to do localized replacement
    header_match = re.search(r'<header.*?</header>', content, re.DOTALL)
    if header_match:
        header_html = header_match.group(0)
        
        # Replace the title inside header
        header_html = header_html.replace('House of Pentool</h2>', 'HOUSE OF<br class="block md:hidden"/>PENTOOL</h2>')
        header_html = header_html.replace('House of Pentool</h1>', 'HOUSE OF<br class="block md:hidden"/>PENTOOL</h1>')
        
        # Make navigation stack nicely on mobile instead of inline wrap
        header_html = header_html.replace('nav class="flex flex-wrap justify-center items-center', 'nav class="flex flex-col md:flex-row justify-center items-center gap-4 md:gap-8 my-4 md:my-0')
        header_html = header_html.replace('nav class="flex items-center', 'nav class="flex flex-col md:flex-row items-center gap-4 md:gap-8 my-4 md:my-0')
        
        # In process.html, we missed the <nav> previously perhaps. It had "flex flex-wrap" if it was hit.
        
        # Apply the replaced header back
        content = content[:header_match.start()] + header_html + content[header_match.end():]


    with open(file, 'w') as f:
        f.write(content)
    print(f"Updated {file}")
