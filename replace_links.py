import os
import glob

mapping = {
    '{{DATA:SCREEN:SCREEN_5}}': 'index.html',
    '{{DATA:SCREEN:SCREEN_6}}': 'process.html',
    '{{DATA:SCREEN:SCREEN_7}}': 'contact.html',
    '{{DATA:SCREEN:SCREEN_8}}': 'portfolio.html',
    '{{DATA:SCREEN:SCREEN_9}}': 'services.html'
}

for filepath in glob.glob('*.html'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    changed = False
    for k, v in mapping.items():
        if k in content:
            content = content.replace(k, v)
            changed = True
            
    if changed:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")
