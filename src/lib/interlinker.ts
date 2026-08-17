/**
 * AyurShakti Wikipedia-style Automatic Interlinker
 * Automatically converts key Ayurvedic terms into internal deep links
 */

const INTERLINK_MAP: Record<string, string> = {
  'Charaka Samhita': '/articles/charaka_samhita_english_translation_by_shree_gulabkunverba',
  'Sushruta Samhita': '/articles/sushruta_samhita_volume_1_sutrasthana_by_kaviraj_kunja_lal',
  'Ashtanga Hridaya': '/articles/ashtanga_hridaya_samhita_sanskrit',
  'Rasa Jala Nidhi': '/articles/rasa_jala_nidhi_vol_1_initiation_mercury_and_laboratory_b',
  'Vrikshayurveda': '/articles/vrikshayurveda_and_environmental_philosophy_by_beenapani',
  'Marma': '/articles/marma_sastra_and_ayurveda_study_by_c_suresh_kumar',
  'Ashwagandha': '/articles/ashwagandha_for_men',
  'Shatavari': '/articles/shatavari_for_women',
  'Giloy': '/articles/giloy_immunity',
  'Triphala': '/articles/triphala',
  'Dosha': '/dosha-quiz',
  'Doshas': '/dosha-quiz',
  'Vata': '/dosha-quiz',
  'Pitta': '/dosha-quiz',
  'Kapha': '/dosha-quiz',
  'Prakriti': '/dosha-quiz',
  'Agni': '/articles/glossary_a',
  'Ama': '/articles/glossary_a',
  'Ojas': '/articles/glossary_o',
  'Prana': '/articles/glossary_p',
  'Dhatu': '/articles/glossary_d',
  'Srotas': '/articles/glossary_s',
  'Rasayana': '/articles/glossary_r',
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
