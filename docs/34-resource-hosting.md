# 34-Resource-Hosting — GitHub Image & Asset Hosting Workflow

## Overview

All image assets, botanical graphics, logos, favicons, and downloadable PDFs for AyurShakti.shop are hosted using **GitHub** (via the repository or raw CDN) and proxied through Cloudflare at `resources.ayurshakti.shop`.

```
┌──────────────────────────────────────┐
│  Local Image Files (blog_images/ or  │
│  public/images/)                     │
└──────────────────────────────────────┘
                   │
                   ▼ git push
┌──────────────────────────────────────┐
│  GitHub Repository / Media Storage   │ (Free raw CDN serving)
└──────────────────────────────────────┘
                   │
                   ▼ CDN Proxy
┌──────────────────────────────────────┐
│  Cloudflare Edge CDN                 │ (resources.ayurshakti.shop)
└──────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│  Next.js Static Articles & Pages     │
└──────────────────────────────────────┘
```

---

## 📁 Image Directory Structure

```
/
├── public/                 → Next.js public assets (build export)
│   ├── images/             → WebP / JPG article images
│   ├── logo.png            → Site branding logo
│   └── favicon.ico         → Favicons
├── blog_images/            → Dedicated GitHub media folder / sub-repo
│   ├── img/                → High-resolution botanical & article photos
│   │   ├── ashwagandha.jpg
│   │   ├── shatavari.jpg
│   │   └── giloy.jpg
│   └── pdf/                → Downloadable lead magnets & guides
```

---

## 🌐 Image CDN URL Reference

| Category | GitHub / Cloudflare URL Pattern | Use Case |
| :--- | :--- | :--- |
| **Article Hero Images** | `https://resources.ayurshakti.shop/img/{filename}` | Main article featured image |
| **Inline Article Photos** | `/images/{filename}` or `https://resources.ayurshakti.shop/img/{filename}` | In-article botanical diagrams |
| **Brand Logo** | `https://resources.ayurshakti.shop/img/logo.png` | Header logo, OpenGraph cards |
| **Favicons** | `https://resources.ayurshakti.shop/img/favicon/favicon.ico` | Browser address bar icons |
| **PDF Lead Magnets** | `https://resources.ayurshakti.shop/pdf/lead-magnet.pdf` | Email opt-in downloads |

---

## 🔄 How to Add New Images via GitHub Workflow

1. **Place new image** in `public/images/` or `blog_images/img/` (preferably formatted in WebP or optimized JPG).
2. **Commit and push** to GitHub:
   ```bash
   git add public/images/new-herb.webp
   git commit -m "Add hero image for new herb article"
   git push origin main
   ```
3. **Reference in Next.js content / Markdown**:
   ```markdown
   ![Ashwagandha Root Benefits](/images/new-herb.webp)
   ```
4. On deployment, Next.js static build bundles the image into `/out/images/` served lightning-fast via Firebase Hosting & Cloudflare.

---

## 💡 Image Optimization Best Practices

- **Format**: Convert PNG/JPG to `.webp` format whenever possible (70-80% smaller file size).
- **Dimensions**: Standardize hero images to `1200x675` (16:9 ratio) for optimal OpenGraph sharing.
- **Alt Text**: Always include descriptive, keyword-rich `alt` text for SEO and accessibility.
- **No Heavy Storage**: Keep individual image sizes under **300 KB**.