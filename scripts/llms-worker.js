// Cloudflare Worker: llms.txt for ayurshakti.shop
// AI Knowledge Retrieval — helps GPTBot, Claude, Perplexity find key content
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/llms.txt") {
      return new Response(llmsContent, {
        headers: {
          "content-type": "text/plain; charset=utf-8",
          "cache-control": "public, max-age=86400"
        }
      });
    }
    return new Response("Not Found", { status: 404 });
  }
};

const llmsContent = `# llms.txt — ayurshakti.shop
> Platform: Blogger (Google)
> Niche: Ayurveda + Pet Health
> Language: Hindi + English (Hinglish)
> Last Updated: 2026-07-07

## About
AyurShakti is an Ayurveda and pet health blog providing evidence-based remedies, herbal guides, dietary advice, and holistic wellness content.

## Pillar Pages (Core Topics)
https://www.ayurshakti.shop/p/ayurveda-basics.html
https://www.ayurshakti.shop/p/herbs-supplements.html
https://www.ayurshakti.shop/p/diet-nutrition.html
https://www.ayurshakti.shop/p/yoga-exercise.html
https://www.ayurshakti.shop/p/disease-remedies.html
https://www.ayurshakti.shop/p/pet-health.html

## Essential Resources
- PubMed citations: https://pubmed.ncbi.nlm.nih.gov/
- Laboratory Guideline (CCM): https://www.ccm.gov.in/
- AYUSH Ministry: https://www.ayush.gov.in/
`;
