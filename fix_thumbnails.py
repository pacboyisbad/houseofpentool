import json, re

LOGO_IMG_ID = "95b73a47-cfd6-44e3-83d4-10197dcaab9e"

with open('scraped_full_projects.json', 'r') as f:
    projects = json.load(f)

# Strip the logo from each project's image list
for p in projects:
    p['images'] = [img for img in p['images'] if LOGO_IMG_ID not in img]

# Also use scraped_projects.json (carousel-style thumbnail) as fallback cover
with open('scraped_projects.json', 'r') as f:
    thumb_data = json.load(f)

thumb_map = {t['url']: t['image'] for t in thumb_data}

# Build the JS data array
js_projects = []
for p in projects:
    imgs = p.get('images', [])
    texts = p.get('texts', [])
    desc = ''
    for t in texts:
        clean = t.strip()
        if len(clean) > 40 and 'cookie' not in clean.lower() and 'privacy' not in clean.lower() and clean.lower() != p['name'].lower():
            desc = clean[:300]
            break

    # Cover: first real project image. Fallback to the scraped thumbnail
    cover = imgs[0] if imgs else thumb_map.get(p['url'], '')

    js_projects.append({
        "name": p['name'],
        "url": p['url'],
        "cover": cover,
        "images": imgs,  # all project images (logo stripped)
        "desc": desc
    })

# Color rotation
colors = ['bg-accent-lime text-black','bg-primary text-white','bg-accent-pink text-white',
          'bg-black text-white','bg-accent-lime text-black','bg-primary text-white']

cards_html = ""
for idx, p in enumerate(js_projects):
    badge_color = colors[idx % len(colors)]
    cards_html += f"""
<div class="group cursor-pointer" onclick="openProject({idx})">
  <div class="bg-white dark:bg-slate-800 bold-border thick-shadow-sm group-hover:-translate-y-3 group-hover:rotate-1 transition-all duration-300 h-full flex flex-col">
    <div class="aspect-square bg-slate-200 overflow-hidden bold-border">
      <img class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" src="{p['cover']}" alt="{p['name']}" loading="lazy"/>
    </div>
    <div class="p-4">
      <span class="inline-block {badge_color} text-[10px] font-black px-2 py-1 bold-border mb-2 uppercase">View Project</span>
      <h3 class="text-base font-black uppercase leading-tight">{p['name']}</h3>
    </div>
  </div>
</div>
"""

js_data = json.dumps(js_projects, ensure_ascii=False)

modal_html = f"""<main class="flex-1 w-full max-w-7xl mx-auto px-4 md:px-10 py-12">
<section class="mb-12">
  <div class="bg-accent-pink p-8 bold-border thick-shadow mb-6">
    <h2 class="text-6xl md:text-9xl font-black uppercase tracking-tighter leading-none text-[#0d161c]">OUR<br/>WORK</h2>
  </div>
  <p class="font-bold text-lg text-slate-600 dark:text-slate-400 max-w-2xl">Click any project to view the full case study.</p>
</section>
<section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-20">
{cards_html}
</section>
</main>

<div id="project-modal" class="fixed inset-0 z-[100] hidden flex-col bg-white dark:bg-background-dark overflow-hidden">
  <div class="sticky top-0 z-10 bg-white dark:bg-background-dark border-b-4 border-black px-6 py-4 flex items-center justify-between gap-4">
    <div>
      <p class="text-xs font-black uppercase tracking-widest text-primary mb-1">House of Pentool — Project</p>
      <h2 id="modal-title" class="text-2xl md:text-4xl font-black uppercase leading-tight"></h2>
    </div>
    <div class="flex items-center gap-3 flex-shrink-0">
      <a id="modal-ext-link" href="#" target="_blank" class="hidden md:inline-flex items-center gap-2 bg-accent-lime px-4 py-2 bold-border thick-shadow-sm font-black uppercase text-xs hover:-translate-y-1 transition-transform">
        Full Case Study ↗
      </a>
      <button onclick="closeProject()" class="bg-black text-white px-5 py-3 font-black uppercase text-sm border-2 border-black hover:bg-primary transition-colors">✕ Close</button>
    </div>
  </div>
  <div class="flex-1 overflow-y-auto">
    <div id="modal-desc" class="px-6 md:px-20 py-8 max-w-4xl mx-auto text-lg font-bold text-slate-700 dark:text-slate-300 leading-relaxed italic border-b-4 border-black"></div>
    <div id="modal-images" class="flex flex-col gap-0"></div>
    <div class="px-6 py-12 text-center border-t-4 border-black bg-black">
      <p class="text-white font-black uppercase tracking-widest mb-4">Want to see more?</p>
      <a id="modal-ext-link-bottom" href="#" target="_blank" class="inline-block bg-accent-lime px-8 py-4 bold-border font-black uppercase text-sm hover:-translate-y-1 transition-transform">View Full Case Study on mrpentool.com ↗</a>
    </div>
  </div>
</div>

<script>
const PROJECTS = {js_data};
function openProject(idx) {{
  const p = PROJECTS[idx];
  const modal = document.getElementById('project-modal');
  document.getElementById('modal-title').textContent = p.name;
  const descEl = document.getElementById('modal-desc');
  if (p.desc) {{ descEl.textContent = p.desc; descEl.classList.remove('hidden'); }}
  else {{ descEl.classList.add('hidden'); }}
  document.getElementById('modal-ext-link').href = p.url;
  document.getElementById('modal-ext-link-bottom').href = p.url;
  const imgContainer = document.getElementById('modal-images');
  imgContainer.innerHTML = '';
  p.images.forEach((src, i) => {{
    const div = document.createElement('div');
    div.innerHTML = `<img src="${{src}}" alt="${{p.name}} — image ${{i+1}}" class="w-full object-cover block" loading="${{i < 3 ? 'eager' : 'lazy'}}" />`;
    imgContainer.appendChild(div);
  }});
  modal.classList.remove('hidden');
  modal.classList.add('flex');
  document.body.style.overflow = 'hidden';
  modal.querySelector('.flex-1').scrollTop = 0;
}}
function closeProject() {{
  const modal = document.getElementById('project-modal');
  modal.classList.add('hidden');
  modal.classList.remove('flex');
  document.body.style.overflow = '';
}}
document.addEventListener('keydown', (e) => {{ if (e.key === 'Escape') closeProject(); }});
</script>
"""

with open('portfolio.html', 'r') as f:
    content = f.read()

result = re.sub(r'</header>.*?(?=<footer)', '</header>\n' + modal_html + '\n', content, flags=re.DOTALL)

with open('portfolio.html', 'w') as f:
    f.write(result)

print(f"Done! Rebuilt portfolio.html — logo stripped, real thumbnails used for {len(js_projects)} projects")
