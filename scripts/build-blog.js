import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';
import { marked } from 'marked';
import { markedHighlight } from 'marked-highlight';
import Prism from 'prismjs';
import loadLanguages from 'prismjs/components/index.js';
import slugify from 'slugify';
import { Feed } from 'feed';
import { siteConfig } from '../site.config.js';

// Load common languages for Prism
loadLanguages(['bash', 'json', 'yaml', 'typescript', 'javascript', 'python', 'docker', 'nginx', 'markdown', 'html', 'css']);

// Configure marked with syntax highlighting and slug IDs
marked.use(
  markedHighlight({
    highlight(code, lang) {
      const language = Prism.languages[lang] ? lang : 'bash';
      return Prism.highlight(code, Prism.languages[language] || Prism.languages.bash, language);
    }
  }),
  {
    gfm: true,
    breaks: true,
  }
);

const POSTS_DIR = path.resolve(process.cwd(), 'content/posts');
const OUTPUT_DIR = process.cwd();

// Helper: Calculate reading time
function calculateReadingTime(text) {
  const wordsPerMinute = 200;
  const words = text.trim().split(/\s+/).length;
  const minutes = Math.ceil(words / wordsPerMinute);
  return `${minutes} min de leitura`;
}

// Helper: Extract ToC from markdown
function extractToC(markdown) {
  const toc = [];
  const lines = markdown.split('\n');
  lines.forEach((line) => {
    const match = line.match(/^(#{2,3})\s+(.+)$/);
    if (match) {
      const level = match[1].length;
      const rawText = match[2].trim().replace(/\*\*/g, '').replace(/`/g, '');
      const id = slugify(rawText, { lower: true, strict: true });
      toc.push({ level, text: rawText, id });
    }
  });
  return toc;
}

// Helper: Add IDs to H2/H3 headings in HTML
function addHeadingIds(html) {
  return html.replace(/<h([2-3])>(.*?)<\/h\1>/gi, (match, level, text) => {
    const rawText = text.replace(/<[^>]+>/g, '').trim();
    const id = slugify(rawText, { lower: true, strict: true });
    return `<h${level} id="${id}" class="scroll-mt-24 group flex items-center justify-between">${text} <a href="#${id}" class="opacity-0 group-hover:opacity-100 text-gray-500 hover:text-cyan-400 text-sm ml-2 transition-opacity">#</a></h${level}>`;
  });
}

// 1. Read and parse all markdown posts
function getAllPosts() {
  if (!fs.existsSync(POSTS_DIR)) return [];
  const files = fs.readdirSync(POSTS_DIR).filter((f) => f.endsWith('.md') || f.endsWith('.mdx'));
  
  const posts = files.map((filename) => {
    const filePath = path.join(POSTS_DIR, filename);
    const rawContent = fs.readFileSync(filePath, 'utf-8');
    const { data, content } = matter(rawContent);

    const slug = data.slug || filename.replace(/\.(md|mdx)$/, '');
    const readingTime = calculateReadingTime(content);
    const toc = extractToC(content);
    const htmlContent = addHeadingIds(marked.parse(content));

    return {
      ...data,
      slug,
      content,
      htmlContent,
      readingTime,
      toc,
      date: data.date ? new Date(data.date).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
      lastmod: data.lastmod ? new Date(data.lastmod).toISOString().split('T')[0] : data.date,
      tags: data.tags || [],
      keywords: data.keywords || [],
      draft: Boolean(data.draft),
      featured: Boolean(data.featured),
      };
      });

      return posts
      .filter((p) => !p.draft)
      .sort((a, b) => {
      if (b.featured && !a.featured) return 1;
      if (a.featured && !b.featured) return -1;
      return new Date(b.date).getTime() - new Date(a.date).getTime();
      });
}

// Global Layout Shell
function renderLayout({ title, description, url, ogImage, structuredData, body, activeNav = 'blog' }) {
  const currentYear = new Date().getFullYear();
  const canonicalUrl = url ? `${siteConfig.url}${url}` : siteConfig.url;
  const image = ogImage || `${siteConfig.url}/static/og-banner.png`;

  return `<!DOCTYPE html>
<html lang="pt-BR" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title ? `${title} | Inteligência Agêntica` : siteConfig.title}</title>
  <meta name="description" content="${description || siteConfig.description}">
  <link rel="canonical" href="${canonicalUrl}">
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="${canonicalUrl}">
  <meta property="og:title" content="${title || siteConfig.title}">
  <meta property="og:description" content="${description || siteConfig.description}">
  <meta property="og:image" content="${image}">
  <meta property="og:site_name" content="Inteligência Agêntica">
  <meta property="og:locale" content="pt_BR">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:url" content="${canonicalUrl}">
  <meta name="twitter:title" content="${title || siteConfig.title}">
  <meta name="twitter:description" content="${description || siteConfig.description}">
  <meta name="twitter:image" content="${image}">

  <!-- Fonts & Tailwind -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://cdn.tailwindcss.com">
  <link rel="preconnect" href="https://unpkg.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            obsidian: '#07070A',
            'obsidian-light': '#0E0E14',
            'obsidian-card': '#111118',
            magenta: '#C000FF',
            'magenta-dim': '#8B00B8',
            ciano: '#00E5FF',
            'ciano-dim': '#009DB8',
            ouro: '#DFBA6B',
            'ouro-light': '#F0D48A',
            'ouro-dark': '#B8952E',
          },
          fontFamily: {
            sans: ['Inter', 'system-ui', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
        },
      },
    }
  </script>
  <script defer src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
  
  <!-- Prism Syntax Theme -->
  <style>
    * { box-sizing: border-box; }
    body { background-color: #07070A; color: #E0E0E6; font-family: 'Inter', sans-serif; overflow-x: hidden; }
    ::selection { background: rgba(192, 0, 255, 0.35); color: #fff; }
    .glass { background: rgba(17, 17, 24, 0.65); border: 1px solid rgba(255, 255, 255, 0.08); backdrop-filter: blur(16px); }
    .glass-card { background: rgba(14, 14, 20, 0.7); border: 1px solid rgba(255, 255, 255, 0.06); backdrop-filter: blur(12px); transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1); }
    .glass-card:hover { border-color: rgba(0, 229, 255, 0.3); transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0, 229, 255, 0.08); }
    .gradient-text { background: linear-gradient(135deg, #C000FF 0%, #00E5FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gradient-text-gold { background: linear-gradient(135deg, #DFBA6B 0%, #F0D48A 40%, #DFBA6B 70%, #B8952E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .btn-gold { background: linear-gradient(135deg, #B8952E 0%, #DFBA6B 35%, #F0D48A 50%, #DFBA6B 65%, #B8952E 100%); color: #07070A; font-weight: 700; transition: all 0.2s ease; }
    .btn-gold:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(223, 186, 107, 0.35); }
    .hero-glow { position: absolute; border-radius: 50%; filter: blur(140px); opacity: 0.16; pointer-events: none; }
    .top-bar { background: rgba(7, 7, 10, 0.85); backdrop-filter: blur(14px); border-bottom: 1px solid rgba(255,255,255,0.06); }
    
    /* Article typography styling */
    .prose-custom { font-size: 1.05rem; line-height: 1.8; color: #D1D5DB; }
    .prose-custom p { margin-bottom: 1.5rem; }
    .prose-custom h1 { font-size: 2.25rem; font-weight: 900; color: #fff; margin-top: 2.5rem; margin-bottom: 1.25rem; line-height: 1.2; }
    .prose-custom h2 { font-size: 1.65rem; font-weight: 800; color: #fff; margin-top: 2.5rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem; }
    .prose-custom h3 { font-size: 1.25rem; font-weight: 700; color: #00E5FF; margin-top: 2rem; margin-bottom: 0.75rem; }
    .prose-custom ul, .prose-custom ol { margin-bottom: 1.5rem; padding-left: 1.5rem; }
    .prose-custom ul { list-style-type: disc; }
    .prose-custom ol { list-style-type: decimal; }
    .prose-custom li { margin-bottom: 0.5rem; }
    .prose-custom strong { color: #fff; font-weight: 700; }
    .prose-custom a { color: #00E5FF; text-decoration: underline; text-underline-offset: 3px; }
    .prose-custom a:hover { color: #F0D48A; }
    .prose-custom blockquote { border-left: 4px solid #00E5FF; background: rgba(0, 229, 255, 0.05); padding: 1.25rem 1.5rem; margin: 1.75rem 0; border-radius: 0 0.75rem 0.75rem 0; color: #E5E7EB; }
    .prose-custom blockquote p { margin-bottom: 0; }
    .prose-custom code:not(pre code) { background: rgba(255, 255, 255, 0.08); color: #00E5FF; padding: 0.2rem 0.4rem; border-radius: 0.375rem; font-family: 'JetBrains Mono', monospace; font-size: 0.9em; }
    .prose-custom pre { background: #0A0A0F !important; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 0.75rem; padding: 1.25rem; margin: 1.75rem 0; overflow-x: auto; }
    .prose-custom pre code { color: #E0E0E6; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 1.6; }
    .prose-custom table { width: 100%; border-collapse: collapse; margin: 1.75rem 0; font-size: 0.95rem; }
    .prose-custom th { background: rgba(255, 255, 255, 0.05); color: #fff; font-weight: 700; text-align: left; padding: 0.75rem 1rem; border: 1px solid rgba(255, 255, 255, 0.1); }
    .prose-custom td { padding: 0.75rem 1rem; border: 1px solid rgba(255, 255, 255, 0.08); }
    .prose-custom tr:nth-child(even) { background: rgba(255, 255, 255, 0.02); }
    .prose-custom hr { border-color: rgba(255, 255, 255, 0.08); margin: 2.5rem 0; }
  </style>

  ${structuredData ? `<script type="application/ld+json">${JSON.stringify(structuredData)}</script>` : ''}
</head>
<body class="antialiased min-h-screen flex flex-col justify-between">
  
  <!-- TOP NAVBAR -->
  <nav class="top-bar fixed top-0 inset-x-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
      <a href="/" class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-magenta to-ciano flex items-center justify-center">
          <i data-lucide="brain" class="w-4.5 h-4.5 text-white"></i>
        </div>
        <span class="text-sm sm:text-base font-bold tracking-tight text-white">Inteligência Agêntica</span>
      </a>

      <!-- Desktop Nav -->
      <div class="hidden md:flex items-center gap-6">
        <a href="/" class="text-xs font-semibold text-gray-300 hover:text-white transition-colors">Início</a>
        <a href="/#cursos" class="text-xs font-semibold text-gray-300 hover:text-white transition-colors">Treinamentos</a>
        <a href="/#ao-vivo" class="text-xs font-semibold text-gray-300 hover:text-white transition-colors">Ao Vivo</a>
        <a href="/#oferta" class="text-xs font-semibold text-gray-300 hover:text-white transition-colors">Planos</a>
        <a href="/cases" class="text-xs font-semibold text-gray-300 hover:text-white transition-colors">Cases</a>
        <a href="/blog" class="text-xs font-bold ${activeNav === 'blog' ? 'text-ciano border-b-2 border-ciano pb-0.5' : 'text-gray-300 hover:text-white'} transition-colors">Blog</a>
      </div>

      <div class="flex items-center gap-3">
        <a href="/#oferta" class="btn-gold px-4 py-2 rounded-lg text-xs font-bold tracking-wide">
          Acessar Comunidade
        </a>
      </div>
    </div>
  </nav>

  <!-- MAIN BODY -->
  <main class="pt-20 flex-grow">
    ${body}
  </main>

  <!-- FOOTER -->
  <footer class="border-t border-white/5 py-12 bg-obsidian-light/50 mt-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
        <div class="md:col-span-2">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-6 h-6 rounded-md bg-gradient-to-br from-magenta to-ciano flex items-center justify-center">
              <i data-lucide="brain" class="w-3.5 h-3.5 text-white"></i>
            </div>
            <span class="text-sm font-bold text-white">Inteligência Agêntica</span>
          </div>
          <p class="text-xs text-gray-400 max-w-sm leading-relaxed">
            O ecossistema definitivo para empresários e profissionais que constroem, hospedam e lideram agentes autônomos de IA 24 horas por dia.
          </p>
        </div>

        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-white mb-3">Navegação</h4>
          <ul class="space-y-2 text-xs text-gray-400">
            <li><a href="/" class="hover:text-ciano transition-colors">Início</a></li>
            <li><a href="/#cursos" class="hover:text-ciano transition-colors">Treinamentos</a></li>
            <li><a href="/#ao-vivo" class="hover:text-ciano transition-colors">Mentorias ao Vivo</a></li>
            <li><a href="/#oferta" class="hover:text-ciano transition-colors">Planos e Assinatura</a></li>
            <li><a href="/blog" class="hover:text-ciano transition-colors">Blog & Artigos</a></li>
          </ul>
        </div>

        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-white mb-3">Recursos & IA</h4>
          <ul class="space-y-2 text-xs text-gray-400">
            <li><a href="/sitemap.xml" class="hover:text-ciano transition-colors">Sitemap XML</a></li>
            <li><a href="/robots.txt" class="hover:text-ciano transition-colors">Robots.txt (AI Friendly)</a></li>
            <li><a href="/llms.txt" class="hover:text-ciano transition-colors">LLMs.txt (Índice IA)</a></li>
            <li><a href="/feed.xml" class="hover:text-ciano transition-colors">RSS Feed</a></li>
          </ul>
        </div>
      </div>

      <div class="pt-8 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-[11px] text-gray-500">&copy; ${currentYear} Inteligência Agêntica &bull; JePierre Soluções. Todos os direitos reservados.</p>
        <p class="text-[10px] text-gray-500">Ecossistema Hermes OS &bull; Powered by Nous Research</p>
      </div>
    </div>
  </footer>

  <script>
    if (typeof lucide !== 'undefined') {
      lucide.createIcons();
    }
  </script>
</body>
</html>`;
}

// 2. Build Blog Home (/blog/index.html)
function buildBlogHome(posts) {
  const allTags = [...new Set(posts.flatMap((p) => p.tags))];
  const featuredPost = posts[0];
  const remainingPosts = posts.slice(1);

  const body = `
  <section class="relative py-12 sm:py-16 overflow-hidden">
    <!-- Glows -->
    <div class="hero-glow bg-magenta -top-20 -left-20 w-96 h-96 absolute"></div>
    <div class="hero-glow bg-ciano top-40 -right-20 w-96 h-96 absolute"></div>

    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- Header -->
      <div class="text-center max-w-3xl mx-auto mb-12">
        <span class="inline-block mb-3 px-3.5 py-1 rounded-full text-[11px] font-semibold tracking-[0.15em] uppercase text-ciano border border-ciano/20 bg-ciano/5">
          Conhecimento & Engenharia Agêntica
        </span>
        <h1 class="text-3xl sm:text-5xl font-extrabold text-white tracking-tight mb-4">
          Blog Inteligência <span class="gradient-text">Agêntica</span>
        </h1>
        <p class="text-gray-400 text-sm sm:text-base leading-relaxed">
          Tutoriais práticos, guias de VPS, arquitetura de multi-agentes e estratégias de GEO para posicionar seu negócio na era das IAs autônomas.
        </p>
      </div>

      <!-- Tag Filters -->
      <div class="flex flex-wrap items-center justify-center gap-2 mb-12">
        <a href="/blog" class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-ciano text-obsidian shadow-lg shadow-ciano/20">
          Todos os Artigos
        </a>
        ${allTags
          .map(
            (tag) => `
          <a href="/tags/${slugify(tag, { lower: true })}" class="px-3.5 py-1.5 rounded-full text-xs font-semibold bg-white/[0.04] text-gray-300 hover:text-white hover:bg-white/[0.08] border border-white/5 transition-colors">
            #${tag}
          </a>
        `
          )
          .join('')}
      </div>

      <!-- Featured Post -->
      ${
        featuredPost
          ? `
      <div class="mb-14">
        <div class="glass-card rounded-2xl overflow-hidden border border-white/10 hover:border-ciano/40 group">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-0">
            <div class="lg:col-span-7 h-64 sm:h-80 lg:h-full relative overflow-hidden bg-obsidian-card">
              <img src="${featuredPost.image}" alt="${featuredPost.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
              <div class="absolute inset-0 bg-gradient-to-t from-obsidian via-transparent to-transparent lg:hidden"></div>
            </div>
            <div class="lg:col-span-5 p-6 sm:p-8 flex flex-col justify-between">
              <div>
                <div class="flex items-center gap-2 text-[11px] font-semibold text-ciano uppercase tracking-wider mb-3">
                  <span>Destaque</span> &bull; <span>${featuredPost.readingTime}</span>
                </div>
                <h2 class="text-xl sm:text-2xl font-bold text-white mb-3 group-hover:text-ciano transition-colors leading-snug">
                  <a href="/blog/${featuredPost.slug}">
                    ${featuredPost.title}
                  </a>
                </h2>
                <p class="text-xs sm:text-sm text-gray-400 line-clamp-3 mb-4 leading-relaxed">
                  ${featuredPost.summary}
                </p>
              </div>

              <div class="pt-4 border-t border-white/5 flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <img src="${siteConfig.author.avatar}" alt="${featuredPost.author}" class="w-7 h-7 rounded-full border border-white/10">
                  <span class="text-xs font-medium text-gray-300">${featuredPost.author}</span>
                </div>
                <a href="/blog/${featuredPost.slug}" class="text-xs font-bold text-ouro hover:text-ouro-light inline-flex items-center gap-1">
                  Ler artigo <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      `
          : ''
      }

      <!-- Grid of Posts -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        ${remainingPosts
          .map(
            (post) => `
          <article class="glass-card rounded-2xl overflow-hidden flex flex-col justify-between group">
            <div>
              <div class="h-48 overflow-hidden relative bg-obsidian-card">
                <img src="${post.image}" alt="${post.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
                <div class="absolute top-3 left-3 flex flex-wrap gap-1.5">
                  ${post.tags
                    .slice(0, 2)
                    .map(
                      (t) =>
                        `<span class="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider bg-obsidian/80 text-ciano backdrop-blur-md border border-white/10">${t}</span>`
                    )
                    .join('')}
                </div>
              </div>
              <div class="p-6">
                <div class="flex items-center gap-2 text-[11px] text-gray-400 mb-2">
                  <span>${post.date}</span> &bull; <span>${post.readingTime}</span>
                </div>
                <h3 class="text-base font-bold text-white group-hover:text-ciano transition-colors mb-2 leading-snug">
                  <a href="/blog/${post.slug}">
                    ${post.title}
                  </a>
                </h3>
                <p class="text-xs text-gray-400 line-clamp-3 leading-relaxed">
                  ${post.summary}
                </p>
              </div>
            </div>

            <div class="p-6 pt-0 border-t border-white/5 mt-4 flex items-center justify-between text-xs">
              <span class="text-gray-400">${post.author}</span>
              <a href="/blog/${post.slug}" class="text-ouro font-semibold hover:text-ouro-light inline-flex items-center gap-1">
                Ler <i data-lucide="arrow-right" class="w-3 h-3"></i>
              </a>
            </div>
          </article>
        `
          )
          .join('')}
      </div>

      <!-- Bottom Community Callout -->
      <div class="mt-16 glass rounded-2xl p-8 text-center border border-ouro/20 bg-gradient-to-br from-ouro/5 to-transparent">
        <h3 class="text-xl sm:text-2xl font-bold text-white mb-2">Quer instalar e liderar agentes na sua empresa?</h3>
        <p class="text-xs sm:text-sm text-gray-300 max-w-xl mx-auto mb-6">
          Assine a comunidade Inteligência Agêntica com 4 encontros ao vivo por mês, biblioteca completa de automações e suporte técnico dedicado.
        </p>
        <a href="/#oferta" class="btn-gold px-6 py-3 rounded-xl text-xs sm:text-sm font-bold tracking-wide inline-flex items-center gap-2">
          Ver Planos & Assinar Agora <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </a>
      </div>

    </div>
  </section>
  `;

  return renderLayout({
    title: 'Blog & Artigos',
    description: 'Tutoriais e artigos práticos sobre Agentes Autônomos de IA, VPS, Docker e GEO.',
    url: '/blog',
    body,
    activeNav: 'blog',
  });
}

// 3. Build Individual Post (/blog/[slug]/index.html)
function buildPostPage(post, allPosts) {
  const relatedPosts = allPosts
    .filter((p) => p.slug !== post.slug && p.tags.some((t) => post.tags.includes(t)))
    .slice(0, 2);

  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    description: post.summary,
    image: post.image,
    datePublished: post.date,
    dateModified: post.lastmod || post.date,
    author: {
      '@type': 'Person',
      name: post.author,
      url: siteConfig.author.linkedin,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Inteligência Agêntica',
      url: siteConfig.url,
      logo: {
        '@type': 'ImageObject',
        url: `${siteConfig.url}/static/logos.png`,
      },
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `${siteConfig.url}/blog/${post.slug}`,
    },
    keywords: post.keywords.join(', '),
  };

  const breadcrumbData = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Início',
        item: siteConfig.url,
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Blog',
        item: `${siteConfig.url}/blog`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: post.title,
        item: `${siteConfig.url}/blog/${post.slug}`,
      },
    ],
  };

  const body = `
  <div class="relative py-10 overflow-hidden">
    <div class="hero-glow bg-magenta/40 -top-40 right-0 w-[500px] h-[500px] absolute"></div>
    <div class="hero-glow bg-ciano/30 top-1/2 -left-40 w-[500px] h-[500px] absolute"></div>

    <article class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- Breadcrumb -->
      <nav class="flex items-center gap-2 text-xs text-gray-400 mb-6" aria-label="Breadcrumb">
        <a href="/" class="hover:text-white transition-colors">Início</a>
        <span>&rsaquo;</span>
        <a href="/blog" class="hover:text-white transition-colors">Blog</a>
        <span>&rsaquo;</span>
        <span class="text-ciano truncate max-w-[200px] sm:max-w-none">${post.title}</span>
      </nav>

      <!-- Post Header -->
      <header class="mb-10 text-center sm:text-left">
        <div class="flex flex-wrap items-center gap-2 mb-4">
          ${post.tags
            .map(
              (t) =>
                `<a href="/tags/${slugify(t, { lower: true })}" class="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider bg-ciano/10 text-ciano border border-ciano/20 hover:bg-ciano/20 transition-colors">#${t}</a>`
            )
            .join('')}
        </div>

        <h1 class="text-2xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight leading-tight mb-6">
          ${post.title}
        </h1>

        <div class="flex flex-wrap items-center justify-between gap-4 py-4 border-y border-white/10 text-xs text-gray-400">
          <div class="flex items-center gap-3">
            <img src="${siteConfig.author.avatar}" alt="${post.author}" class="w-10 h-10 rounded-full border border-white/10">
            <div>
              <p class="font-bold text-white text-sm">${post.author}</p>
              <p class="text-[11px] text-gray-400">${siteConfig.author.role}</p>
            </div>
          </div>

          <div class="flex items-center gap-4 text-xs">
            <span class="flex items-center gap-1"><i data-lucide="calendar" class="w-3.5 h-3.5 text-ciano"></i> ${post.date}</span>
            <span class="flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5 text-ouro"></i> ${post.readingTime}</span>
          </div>
        </div>
      </header>

      <!-- Featured Image -->
      ${
        post.image
          ? `
      <div class="mb-12 rounded-2xl overflow-hidden border border-white/10 glass shadow-2xl">
        <img src="${post.image}" alt="${post.title}" class="w-full h-auto max-h-[460px] object-cover">
      </div>
      `
          : ''
      }

      <!-- Table of Contents (if > 1 heading) -->
      ${
        post.toc && post.toc.length > 1
          ? `
      <div class="mb-10 glass rounded-2xl p-6 border border-white/10">
        <h3 class="text-xs font-bold uppercase tracking-wider text-ouro mb-3 flex items-center gap-2">
          <i data-lucide="list" class="w-4 h-4"></i> Índice do Artigo
        </h3>
        <ul class="space-y-2 text-xs sm:text-sm">
          ${post.toc
            .map(
              (item) => `
            <li class="${item.level === 3 ? 'ml-4 text-gray-400' : 'font-semibold text-gray-200'}">
              <a href="#${item.id}" class="hover:text-ciano transition-colors flex items-center gap-1.5">
                <span class="text-ciano/60">&rsaquo;</span> ${item.text}
              </a>
            </li>
          `
            )
            .join('')}
        </ul>
      </div>
      `
          : ''
      }

      <!-- Main Article Content -->
      <div class="prose-custom">
        ${post.htmlContent}
      </div>

      <!-- Social Share -->
      <div class="mt-12 py-6 border-y border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
        <span class="text-xs font-bold uppercase tracking-wider text-gray-300">Compartilhar este artigo:</span>
        <div class="flex items-center gap-2">
          <a href="https://api.whatsapp.com/send?text=${encodeURIComponent(`${post.title} - ${siteConfig.url}/blog/${post.slug}`)}" target="_blank" rel="noopener" class="p-2.5 rounded-lg bg-green-500/10 text-green-400 hover:bg-green-500/20 border border-green-500/20 text-xs font-semibold inline-flex items-center gap-1.5 transition-colors">
            <i data-lucide="message-circle" class="w-4 h-4"></i> WhatsApp
          </a>
          <a href="https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(`${siteConfig.url}/blog/${post.slug}`)}" target="_blank" rel="noopener" class="p-2.5 rounded-lg bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 border border-blue-500/20 text-xs font-semibold inline-flex items-center gap-1.5 transition-colors">
            <i data-lucide="linkedin" class="w-4 h-4"></i> LinkedIn
          </a>
          <a href="https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent(`${siteConfig.url}/blog/${post.slug}`)}" target="_blank" rel="noopener" class="p-2.5 rounded-lg bg-white/5 text-gray-200 hover:bg-white/10 border border-white/10 text-xs font-semibold inline-flex items-center gap-1.5 transition-colors">
            <i data-lucide="twitter" class="w-4 h-4"></i> X / Twitter
          </a>
        </div>
      </div>

      <!-- Author Bio Box -->
      <div class="mt-10 glass rounded-2xl p-6 sm:p-8 flex flex-col sm:flex-row items-center sm:items-start gap-5 border border-white/10">
        <img src="${siteConfig.author.avatar}" alt="${post.author}" class="w-16 h-16 rounded-full border-2 border-ouro">
        <div class="text-center sm:text-left">
          <h4 class="text-base font-bold text-white mb-1">Escrito por ${siteConfig.author.name}</h4>
          <p class="text-xs text-gray-400 leading-relaxed mb-3">
            ${siteConfig.author.bio}
          </p>
          <div class="flex items-center justify-center sm:justify-start gap-3 text-xs text-ciano">
            <a href="${siteConfig.author.github}" target="_blank" class="hover:underline">GitHub</a> &bull;
            <a href="${siteConfig.author.linkedin}" target="_blank" class="hover:underline">LinkedIn</a> &bull;
            <a href="${siteConfig.author.twitter}" target="_blank" class="hover:underline">X</a>
          </div>
        </div>
      </div>

      <!-- In-Article Community Banner -->
      <div class="mt-12 p-8 rounded-2xl glass border border-ouro/30 bg-gradient-to-r from-magenta/10 via-ciano/5 to-ouro/10 text-center">
        <span class="inline-block px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider text-ouro bg-ouro/10 border border-ouro/20 mb-3">
          Comunidade Inteligência Agêntica
        </span>
        <h3 class="text-xl sm:text-2xl font-bold text-white mb-2">Aprenda a aplicar tudo isso na prática</h3>
        <p class="text-xs sm:text-sm text-gray-300 max-w-lg mx-auto mb-6">
          Tenha acesso a 4 mentorias ao vivo por mês, biblioteca completa de skills e templates prontos para rodar no seu servidor.
        </p>
        <a href="/#oferta" class="btn-gold px-8 py-3.5 rounded-xl text-sm font-bold tracking-wide inline-flex items-center gap-2">
          Garantir Vaga na Comunidade <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </a>
      </div>

      <!-- Related Posts -->
      ${
        relatedPosts.length > 0
          ? `
      <div class="mt-16">
        <h3 class="text-lg font-bold text-white mb-6">Artigos Relacionados</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
          ${relatedPosts
            .map(
              (p) => `
            <a href="/blog/${p.slug}" class="glass-card rounded-xl p-5 border border-white/5 block group">
              <span class="text-[10px] font-bold uppercase text-ciano mb-1 block">${p.tags[0] || 'Artigo'}</span>
              <h4 class="text-sm font-bold text-white group-hover:text-ciano transition-colors leading-snug mb-2">${p.title}</h4>
              <p class="text-xs text-gray-400 line-clamp-2">${p.summary}</p>
            </a>
          `
            )
            .join('')}
        </div>
      </div>
      `
          : ''
      }

    </article>
  </div>
  `;

  return renderLayout({
    title: post.title,
    description: post.summary,
    url: `/blog/${post.slug}`,
    ogImage: post.image,
    structuredData: [structuredData, breadcrumbData],
    body,
    activeNav: 'blog',
  });
}

// 4. Build Tag Page (/tags/[tag]/index.html)
function buildTagPage(tag, posts) {
  const taggedPosts = posts.filter((p) => p.tags.map((t) => slugify(t, { lower: true })).includes(tag));

  const body = `
  <section class="relative py-12 sm:py-16">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-3xl mx-auto mb-12">
        <a href="/blog" class="inline-flex items-center gap-1 text-xs text-ciano hover:underline mb-3">
          <i data-lucide="arrow-left" class="w-3.5 h-3.5"></i> Voltar para todos os artigos
        </a>
        <h1 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mb-2">
          Artigos em <span class="gradient-text">#${tag}</span>
        </h1>
        <p class="text-gray-400 text-xs sm:text-sm">
          ${taggedPosts.length} ${taggedPosts.length === 1 ? 'artigo encontrado' : 'artigos encontrados'}
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        ${taggedPosts
          .map(
            (post) => `
          <article class="glass-card rounded-2xl overflow-hidden flex flex-col justify-between group">
            <div>
              <div class="h-48 overflow-hidden relative bg-obsidian-card">
                <img src="${post.image}" alt="${post.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
              </div>
              <div class="p-6">
                <div class="flex items-center gap-2 text-[11px] text-gray-400 mb-2">
                  <span>${post.date}</span> &bull; <span>${post.readingTime}</span>
                </div>
                <h3 class="text-base font-bold text-white group-hover:text-ciano transition-colors mb-2 leading-snug">
                  <a href="/blog/${post.slug}">
                    ${post.title}
                  </a>
                </h3>
                <p class="text-xs text-gray-400 line-clamp-3 leading-relaxed">
                  ${post.summary}
                </p>
              </div>
            </div>

            <div class="p-6 pt-0 border-t border-white/5 mt-4 flex items-center justify-between text-xs">
              <span class="text-gray-400">${post.author}</span>
              <a href="/blog/${post.slug}" class="text-ouro font-semibold hover:text-ouro-light inline-flex items-center gap-1">
                Ler <i data-lucide="arrow-right" class="w-3 h-3"></i>
              </a>
            </div>
          </article>
        `
          )
          .join('')}
      </div>
    </div>
  </section>
  `;

  return renderLayout({
    title: `Artigos sobre #${tag}`,
    description: `Artigos e tutoriais categorizados sob a tag #${tag} no blog Inteligência Agêntica.`,
    url: `/tags/${tag}`,
    body,
    activeNav: 'blog',
  });
}

// 5. Generate Robots.txt (AI Friendly)
function generateRobotsTxt() {
  return `# Robots.txt - Inteligência Agêntica
# Otimizado para indexação por buscadores e motores de IA generativa (GEO)

User-agent: *
Allow: /

# Motores de IA Generativa e LLM Crawlers
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: cohere-ai
Allow: /

Sitemap: ${siteConfig.url}/sitemap.xml
`;
}

// 6. Generate Sitemap.xml
function generateSitemapXml(posts) {
  const allTags = [...new Set(posts.flatMap((p) => p.tags.map((t) => slugify(t, { lower: true }))))];
  const now = new Date().toISOString();

  let xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${siteConfig.url}/</loc>
    <lastmod>${now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>${siteConfig.url}/blog</loc>
    <lastmod>${now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>`;

  posts.forEach((post) => {
    xml += `
  <url>
    <loc>${siteConfig.url}/blog/${post.slug}</loc>
    <lastmod>${post.lastmod || post.date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>`;
  });

  allTags.forEach((tag) => {
    xml += `
  <url>
    <loc>${siteConfig.url}/tags/${tag}</loc>
    <lastmod>${now}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.6</priority>
  </url>`;
  });

  xml += `
</urlset>`;
  return xml;
}

// 7. Generate llms.txt and llms-full.txt
function generateLlmsTxt(posts) {
  let doc = `# Inteligência Agêntica — Base de Conhecimento para LLMs

> **Descrição:** Inteligência Agêntica é o ecossistema brasileiro de capacitação, infraestrutura e governança para agentes autônomos de IA (Hermes OS), automação de processos, servidores VPS com Docker e GEO (Generative Engine Optimization).

## Informações Principais
- **Website:** ${siteConfig.url}
- **Assinatura / Comunidade:** ${siteConfig.url}/#oferta (Planos Mensal R$ 97 / Anual R$ 497)
- **Pilares:** 4 encontros ao vivo por mês, biblioteca viva de automações semanais, tutoriais de VPS e Docker Swarm.

## Artigos e Guias Técnicos Disponíveis

`;

  posts.forEach((post) => {
    doc += `### [${post.title}](${siteConfig.url}/blog/${post.slug})
- **Data de Publicação:** ${post.date}
- **Tags:** ${post.tags.join(', ')}
- **Resumo:** ${post.summary}
- **URL:** ${siteConfig.url}/blog/${post.slug}

`;
  });

  return doc;
}

function generateLlmsFullTxt(posts) {
  let full = generateLlmsTxt(posts);
  full += `\n---\n\n# Conteúdo Integral dos Artigos\n\n`;

  posts.forEach((post) => {
    full += `## ${post.title}\n`;
    full += `URL: ${siteConfig.url}/blog/${post.slug}\n`;
    full += `Autor: ${post.author} | Data: ${post.date}\n\n`;
    full += `${post.content}\n\n---\n\n`;
  });

  return full;
}

// 8. Generate Feed.xml (RSS 2.0)
function generateRssFeed(posts) {
  const feed = new Feed({
    title: siteConfig.title,
    description: siteConfig.description,
    id: siteConfig.url,
    link: siteConfig.url,
    language: 'pt-BR',
    image: `${siteConfig.url}/static/og-banner.png`,
    favicon: `${siteConfig.url}/favicon.ico`,
    copyright: `All rights reserved ${new Date().getFullYear()}, Inteligência Agêntica`,
    author: {
      name: siteConfig.author.name,
      link: siteConfig.author.linkedin,
    },
  });

  posts.forEach((post) => {
    feed.addItem({
      title: post.title,
      id: `${siteConfig.url}/blog/${post.slug}`,
      link: `${siteConfig.url}/blog/${post.slug}`,
      description: post.summary,
      content: post.htmlContent,
      author: [
        {
          name: post.author,
          link: siteConfig.author.linkedin,
        },
      ],
      date: new Date(post.date),
      image: post.image,
    });
  });

  return feed.rss2();
}

// ==========================================
// MAIN BUILD EXECUTION
// ==========================================
async function main() {
  console.log('🚀 Iniciando build do Blog Inteligência Agêntica...');
  const posts = getAllPosts();
  console.log(`📄 Encontrados ${posts.length} artigos para compilação.`);

  // 1. Create Directories
  const blogDir = path.join(OUTPUT_DIR, 'blog');
  const tagsDir = path.join(OUTPUT_DIR, 'tags');
  if (!fs.existsSync(blogDir)) fs.mkdirSync(blogDir, { recursive: true });
  if (!fs.existsSync(tagsDir)) fs.mkdirSync(tagsDir, { recursive: true });

  // 2. Build /blog/index.html
  fs.writeFileSync(path.join(blogDir, 'index.html'), buildBlogHome(posts));
  console.log('✅ /blog/index.html gerado.');

  // 3. Build each /blog/[slug]/index.html
  posts.forEach((post) => {
    const postDir = path.join(blogDir, post.slug);
    if (!fs.existsSync(postDir)) fs.mkdirSync(postDir, { recursive: true });
    fs.writeFileSync(path.join(postDir, 'index.html'), buildPostPage(post, posts));
  });
  console.log(`✅ ${posts.length} páginas individuais de artigos geradas.`);

  // 4. Build tag pages /tags/[tag]/index.html
  const allTags = [...new Set(posts.flatMap((p) => p.tags.map((t) => slugify(t, { lower: true }))))];
  allTags.forEach((tag) => {
    const tagDir = path.join(tagsDir, tag);
    if (!fs.existsSync(tagDir)) fs.mkdirSync(tagDir, { recursive: true });
    fs.writeFileSync(path.join(tagDir, 'index.html'), buildTagPage(tag, posts));
  });
  console.log(`✅ ${allTags.length} páginas de tags geradas.`);

  // 5. Generate /sitemap.xml
  fs.writeFileSync(path.join(OUTPUT_DIR, 'sitemap.xml'), generateSitemapXml(posts));
  console.log('✅ /sitemap.xml gerado.');

  // 6. Generate /robots.txt
  fs.writeFileSync(path.join(OUTPUT_DIR, 'robots.txt'), generateRobotsTxt());
  console.log('✅ /robots.txt (GEO/AI-Friendly) gerado.');

  // 7. Generate /llms.txt and /llms-full.txt
  fs.writeFileSync(path.join(OUTPUT_DIR, 'llms.txt'), generateLlmsTxt(posts));
  fs.writeFileSync(path.join(OUTPUT_DIR, 'llms-full.txt'), generateLlmsFullTxt(posts));
  console.log('✅ /llms.txt e /llms-full.txt gerados para LLMs.');

  // 8. Generate /feed.xml
  fs.writeFileSync(path.join(OUTPUT_DIR, 'feed.xml'), generateRssFeed(posts));
  console.log('✅ /feed.xml (RSS 2.0) gerado.');

  console.log('\n🎉 Build completo concluído com sucesso!');
}

main().catch((err) => {
  console.error('❌ Erro durante o build:', err);
  process.exit(1);
});
