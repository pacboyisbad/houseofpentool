import re
import glob

def replace_logos():
    for file in glob.glob('*.html'):
        with open(file, 'r') as f:
            content = f.read()

        # The icon div typically contains the material icon.
        pattern = re.compile(r'<div[^>]*>\s*<span class="material-symbols-outlined[^>]*>(?:pentagon|package_2)</span>\s*</div>', re.IGNORECASE)
        
        # We replace it with the Logo.svg img tag
        new_content = pattern.sub('<img src="Logo.svg" alt="House of Pentool Logo" class="h-10 w-auto object-contain">', content)
        
        # Let's also handle the case where it might be slightly different in contact.html footer.
        
        if new_content != content:
            with open(file, 'w') as f:
                f.write(new_content)
            print(f"Updated {file}")

replace_logos()
