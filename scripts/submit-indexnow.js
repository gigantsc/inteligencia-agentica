import fs from 'fs';
import path from 'path';
import { siteConfig } from '../site.config.js';

// IndexNow key generation or reading
const KEY_FILE = path.join(process.cwd(), 'indexnow-key.txt');

function getIndexNowKey() {
  if (fs.existsSync(KEY_FILE)) {
    return fs.readFileSync(KEY_FILE, 'utf-8').trim();
  }
  // Generate random 32-char hex key if not exists
  const key = Array.from({ length: 32 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
  fs.writeFileSync(KEY_FILE, key);
  fs.writeFileSync(path.join(process.cwd(), `${key}.txt`), key);
  return key;
}

function parseSitemapUrls() {
  const sitemapPath = path.join(process.cwd(), 'sitemap.xml');
  if (!fs.existsSync(sitemapPath)) {
    throw new Error('sitemap.xml não encontrado. Execute npm run build primeiro.');
  }
  const xml = fs.readFileSync(sitemapPath, 'utf-8');
  const locRegex = /<loc>(.*?)<\/loc>/g;
  const urls = [];
  let match;
  while ((match = locRegex.exec(xml)) !== null) {
    if (match[1]) urls.push(match[1].trim());
  }
  return [...new Set(urls)];
}

async function submitIndexNow() {
  console.log('🚀 Iniciando envio para IndexNow...');
  const key = getIndexNowKey();
  const host = new URL(siteConfig.url).host;
  const keyLocation = `${siteConfig.url}/${key}.txt`;
  const urls = parseSitemapUrls();

  console.log(`📡 Host: ${host}`);
  console.log(`🔑 Key Location: ${keyLocation}`);
  console.log(`📄 Total de URLs para envio: ${urls.length}`);

  const payload = {
    host,
    key,
    keyLocation,
    urlList: urls,
  };

  try {
    const response = await fetch('https://api.indexnow.org/indexnow', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
      },
      body: JSON.stringify(payload),
    });

    if (response.status === 200 || response.status === 202) {
      console.log(`✅ Sucesso! ${urls.length} URLs submetidas instantaneamente para o IndexNow (Bing/Yandex). Status: ${response.status}`);
    } else {
      const text = await response.text();
      console.warn(`⚠️ IndexNow retornou status ${response.status}: ${text}`);
    }
  } catch (err) {
    console.error('❌ Falha na conexão com IndexNow:', err.message);
  }
}

submitIndexNow();
