/**
 * AyurShakti Wikipedia-style Automatic Interlinker
 * Automatically converts key Ayurvedic terms into internal deep links
 */

const INTERLINK_MAP: Record<string, string> = {
  'Charaka Samhita': '/samhitas/charaka-samhita',
  'Sushruta Samhita': '/samhitas/sushruta-samhita',
  'Ashtanga Hridaya': '/samhitas',
  'Rasa Jala Nidhi': '/canonical-texts',
  'Vrikshayurveda': '/research/vrikshayurveda-and-environmental-philosophy-by-beenapani',
  'Marma': '/research/marma-sastra-and-ayurveda-study-by-c-suresh-kumar',
  'Ashwagandha': '/herbs/ashwagandha',
  'Shatavari': '/herbs/shatavari',
  'Giloy': '/herbs/giloy',
  'Triphala': '/herbs/triphala',
  'Dosha': '/dosha-quiz',
  'Doshas': '/dosha-quiz',
  'Vata': '/dosha-quiz',
  'Pitta': '/dosha-quiz',
  'Kapha': '/dosha-quiz',
  'Prakriti': '/dosha-quiz',
  'Agni': '/glossary/a',
  'Ama': '/glossary/a',
  'Ojas': '/glossary/o',
  'Prana': '/glossary/p',
  'Dhatu': '/glossary/d',
  'Srotas': '/glossary/s',
  'Rasayana': '/glossary/r',
};

export function applyWikipediaInterlinks(htmlContent: string): string {
  if (!htmlContent) return htmlContent;

  let processedHtml = htmlContent;

  // Track replaced terms to prevent duplicate linking per page (Wikipedia standard)
  const replacedTerms = new Set<string>();

  for (const [term, path] of Object.entries(INTERLINK_MAP)) {
    if (replacedTerms.has(term.toLowerCase())) continue;

    // Matches term outside existing HTML tags and outside <a>...</a> anchors
    const regex = new RegExp(`(?<!<[^>]*)\\b(${term})\\b(?![^<]*>|[^<]*<\\/a>)`, 'i');

    if (regex.test(processedHtml)) {
      processedHtml = processedHtml.replace(
        regex,
        `<a href="${path}" class="text-ayur-emerald font-medium underline decoration-ayur-emerald/40 underline-offset-4 hover:decoration-ayur-emerald hover:text-ayur-forest transition-colors" title="Explore ${term} on AyurShakti">$1</a>`
      );
      replacedTerms.add(term.toLowerCase());
    }
  }

  return processedHtml;
}
