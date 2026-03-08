import json
import re

with open('scraped_projects.json', 'r') as f:
    projects = json.load(f)

with open('portfolio.html', 'r') as f:
    content = f.read()

# Generate new gallery HTML
gallery_html = ""
for idx, proj in enumerate(projects):
    title_parts = proj['title'].split('\n')
    year = title_parts[0] if len(title_parts) > 1 else "2024"
    name = title_parts[-1]
    
    # Use different accent colors for variety (like the original design)
    colors = ['bg-accent-lime', 'bg-primary text-white', 'bg-accent-pink text-white']
    color = colors[idx % len(colors)]
    
    card = f"""
<!-- Project {idx+1} -->
<a href="{proj['url']}" target="_blank" class="group cursor-pointer block">
<div class="bg-white dark:bg-slate-800 bold-border p-3 thick-shadow-sm group-hover:-translate-y-2 transition-transform h-full flex flex-col">
<div class="aspect-square bg-slate-200 mb-4 overflow-hidden bold-border flex-shrink-0">
<img class="w-full h-full object-cover" data-alt="{name}" src="{proj['image']}"/>
</div>
<div class="flex-grow flex flex-col justify-between">
    <div>
        <span class="inline-block {color} text-[10px] font-black px-2 py-1 bold-border mb-2 uppercase">{year}</span>
        <h3 class="text-xl font-black uppercase leading-tight">{name}</h3>
    </div>
</div>
</div>
</a>
"""
    gallery_html += card

# We need to replace the content inside:
# <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-20"> ... </section>

pattern = re.compile(r'(<section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-20">)(.*?)(</section>)', re.DOTALL)
new_content = pattern.sub(r'\1\n' + gallery_html + r'\n\3', content)

with open('portfolio.html', 'w') as f:
    f.write(new_content)

print("Updated portfolio.html with scraped projects")
