import glob

def make_responsive():
    for file in glob.glob('*.html'):
        with open(file, 'r') as f:
            content = f.read()

        changed = False

        # General generic flex wrapper fixes for header
        if 'flex items-center justify-between' in content and '<header' in content:
            # We want to change the header container to allow column stacking on mobile
            content = content.replace('flex items-center justify-between', 'flex flex-col md:flex-row items-center justify-between gap-4 md:gap-0', 1)
            changed = True

        # Fix nav links that are hidden on mobile
        if 'hidden md:flex' in content:
            content = content.replace('hidden md:flex', 'flex flex-wrap justify-center')
            changed = True
        elif 'hidden lg:flex' in content:
            content = content.replace('hidden lg:flex', 'flex flex-wrap justify-center')
            changed = True

        # Let's ensure CTA buttons in the header wrap nicely 
        # (This is harder to target blindly, but gap-4 above handles spacing)

        if changed:
            with open(file, 'w') as f:
                f.write(content)
            print(f"Updated {file}")

make_responsive()
