# 13-Image-Generation-Guide — AyurShakti.shop

## Purpose
This document guides AI agents and users on the manual image generation workflow for blog posts. To maintain a premium, aesthetic, and consistent visual identity, all images are generated manually using a designated external AI app and then linked to the project.

## Workflow

Whenever a new article is drafted (via `docs/09-article-writing-rule.md`), an image request must be created for the human user to generate and provide the image.

### Step 1: Add Request to the Queue
After writing an article, the AI agent must append a new block to `data/tracking/manual-image-requests.txt`.

**Format to append:**
```text
Article Title: [Exact Article Title]
Description: [Brief description of the image subject, lighting, and style (e.g., Minimalist watercolor style, vibrant green colors)]

Image URL Link: 
Image Quantity: 1
Status: Pending
--------------------------------------------------
```

### Step 2: Manual Generation (By User)
The user checks `manual-image-requests.txt` during the startup routine.
1. The user takes the `Description` and uses their custom AI image generation app.
2. The user uploads the generated image to the GitHub repository `bhati8833/ayurshakti-images` in the `/img/` folder.
3. The image becomes available on the CDN at `https://resources.ayurshakti.shop/img/[filename].jpg`.
4. The user pastes the CDN URL into the `Image URL Link` field.
5. The user updates the `Status` to `Completed`.

### Step 3: Verification
Before publishing, the pre-publish checklist in `docs/09-article-writing-rule.md` requires verifying that the image URL is present and the image has been properly added to the article content.

## Design Guidelines for the User

When generating images manually, please adhere to these guidelines:

### ✅ DOs
- **Art Style:** Use styles like "minimalist illustration", "watercolor painting", "clean vector art", or "aesthetic photography".
- **Lighting & Vibe:** Use "soft golden lighting", "peaceful atmosphere", "vibrant colors", and "premium clean look".
- **Dimensions:** Generate in a 16:9 aspect ratio (1280x720) for blog headers.

### ❌ DON'Ts
- **NO TEXT:** Ensure the image contains no text, words, or typography.
- **No Close-up Human Faces/Hands:** Avoid distorted AI faces or hands. Use "faceless" or "silhouette".
