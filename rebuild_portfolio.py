import json
import re

with open('scraped_full_projects.json', 'r') as f:
    projects = json.load(f)

with open('portfolio.html', 'r') as f:
    content = f.read()

# Color rotation
colors = [
    'bg-accent-lime text-black',
    'bg-primary text-white',
    'bg-accent-pink text-white',
    'bg-black text-white',
    'bg-accent-lime text-black',
    'bg-primary text-white',
]

def build_project_card(proj, idx):
    name = proj['name']
    url = proj['url']
    images = proj.get('images', [])
    texts = proj.get('texts', [])
    
    # Primary image (first one is the cover)
    cover_img = images[0] if images else ''
    extra_imgs = images[1:6]  # Up to 5 additional images
    
    # Description text (first meaningful paragraph)
    description = ''
    for t in texts:
        if len(t) > 40 and t != name and 'cookie' not in t.lower() and 'privacy' not in t.lower():
            description = t[:200] + ('…' if len(t) > 200 else '')
            break
    
    badge_color = colors[idx % len(colors)]
    
    # Build an image gallery strip if more images
    img_strip = ''
    if extra_imgs:
        img_strip = '<div class="grid grid-cols-3 gap-2 mt-3">'
        for img_s in extra_imgs[:6]:
            img_strip += f'<div class="aspect-square overflow-hidden bold-border"><img class="w-full h-full object-cover" src="{img_s}" alt="{name}"/></div>'
        img_strip += '</div>'
    
    desc_html = f'<p class="text-sm font-bold text-slate-600 dark:text-slate-400 mt-2 leading-snug">{description}</p>' if description else ''
    
    card = f"""
<!-- Project: {name} -->
<div class="group">
  <div class="bg-white dark:bg-slate-800 bold-border thick-shadow-sm group-hover:-translate-y-2 transition-transform duration-300 h-full flex flex-col">
    <a href="{url}" target="_blank" class="block">
      <div class="aspect-square bg-slate-200 overflow-hidden bold-border">
        <img class="w-full h-full object-cover hover:scale-105 transition-transform duration-500" src="{cover_img}" alt="{name}" loading="lazy"/>
      </div>
    </a>
    <div class="p-4 flex flex-col flex-grow">
      <span class="inline-block {badge_color} text-[10px] font-black px-2 py-1 bold-border mb-3 uppercase self-start">View Project ↗</span>
      <a href="{url}" target="_blank" class="hover:text-primary transition-colors">
        <h3 class="text-lg font-black uppercase leading-tight mb-2">{name}</h3>
      </a>
      {desc_html}
      {img_strip}
    </div>
  </div>
</div>
"""
    return card

# Generate new grid
all_cards = ''.join(build_project_card(p, i) for i, p in enumerate(projects))

# Replace the entire main section (between </header> and <footer)
main_section = f"""<main class="flex-1 w-full max-w-7xl mx-auto px-4 md:px-10 py-12">
<!-- Hero Section -->
<section class="mb-16">
<div class="bg-accent-pink p-8 bold-border thick-shadow mb-8">
<h2 class="text-6xl md:text-9xl font-black uppercase tracking-tighter leading-none text-[#0d161c]">
                        OUR<br/>WORK
                    </h2>
</div>
<p class="font-bold text-lg text-slate-600 dark:text-slate-400 max-w-2xl">Real packaging and branding projects crafted for clients worldwide. Click any project to explore the full case study.</p>
</section>
<!-- All Projects Grid -->
<section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
{all_cards}
</section>
</main>"""

# Replace everything between </header> and <footer
result = re.sub(r'</header>.*?(?=<footer)', '</header>\n' + main_section + '\n', content, flags=re.DOTALL)

with open('portfolio.html', 'w') as f:
    f.write(result)

print(f"Rebuilt portfolio.html with {len(projects)} real projects and removed Box Lab/Unboxing sections")
