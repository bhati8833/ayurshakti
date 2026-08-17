/**
 * AyurShakti Wikipedia-style Automatic Interlinker & Hover Preview Card System
 * Automatically converts key Ayurvedic terms into internal deep links with instant hover preview cards.
 */

interface InterlinkMetadata {
  path: string;
  category: string;
  definition: string;
}

const INTERLINK_MAP: Record<string, InterlinkMetadata> = {
  'Charaka Samhita': {
    path: '/samhitas/charaka-samhita',
    category: 'Canonical Treatise',
    definition: 'The foundational Ayurvedic medical treatise on internal medicine (Kayachikitsa) authored by Maharshi Charaka.',
  },
  'Sushruta Samhita': {
    path: '/samhitas/sushruta-samhita',
    category: 'Canonical Treatise',
    definition: 'The classical surgical text of Ayurveda authored by Sushruta, detailing surgical instruments, Marma points, and anatomy.',
  },
  'Ashtanga Hridaya': {
    path: '/samhitas',
    category: 'Canonical Treatise',
    definition: 'Vagbhata\'s poetic compendium synthesizing the medical wisdom of Charaka and Sushruta Samhitas.',
  },
  'Marma': {
    path: '/research/marma-sastra-and-ayurveda-study-by-c-suresh-kumar',
    category: 'Sharira / Anatomy',
    definition: 'Vital anatomical junctions of ligaments, vessels, joints, bones, and nerves containing life essence (Prana).',
  },
  'Ashwagandha': {
    path: '/herbs/ashwagandha',
    category: 'Dravyaguna / Herb',
    definition: 'Withania somnifera, a premier adaptogenic root enhancing stress resilience, neuromuscular strength, and vitality.',
  },
  'Shatavari': {
    path: '/herbs/shatavari',
    category: 'Dravyaguna / Herb',
    definition: 'Asparagus racemosus root, a soothing nutritive tonic supporting female reproductive health and digestive mucosa.',
  },
  'Giloy': {
    path: '/herbs/giloy',
    category: 'Dravyaguna / Herb',
    definition: 'Tinospora cordifolia (Guduchi), the ultimate immunomodulatory vine that clears chronic fever and purifies blood.',
  },
  'Triphala': {
    path: '/herbs/triphala',
    category: 'Dravyaguna / Formulation',
    definition: 'The classical 3-fruit synergy (Amalaki, Haritaki, Bibhitaki) supporting digestive regularity and tissue detox.',
  },
  'Dosha': {
    path: '/dosha-quiz',
    category: 'Constitutional Assessment',
    definition: 'The three fundamental bio-energetic forces (Vata, Pitta, Kapha) governing physical and mental health.',
  },
  'Vata': {
    path: '/dosha-quiz',
    category: 'Sharira / Physiology',
    definition: 'The Ayurvedic dosha governed by Air and Ether elements, controlling movement, nerve impulses, and respiration.',
  },
  'Pitta': {
    path: '/dosha-quiz',
    category: 'Sharira / Physiology',
    definition: 'The Ayurvedic dosha governed by Fire and Water elements, regulating digestion, metabolism, and body heat.',
  },
  'Kapha': {
    path: '/dosha-quiz',
    category: 'Sharira / Physiology',
    definition: 'The Ayurvedic dosha governed by Water and Earth elements, responsible for bodily structure, immunity, and lubrication.',
  },
  'Prakriti': {
    path: '/dosha-quiz',
    category: 'Constitutional Assessment',
    definition: 'An individual\'s unique psycho-physiological constitution determined at conception by Vata, Pitta, and Kapha.',
  },
  'Agni': {
    path: '/glossary/term/agni',
    category: 'Sharira / Physiology',
    definition: 'The metabolic digestive fire responsible for food assimilation, cellular metabolism, and systemic transformation.',
  },
  'Ama': {
    path: '/glossary/term/ama',
    category: 'Nidana / Pathology',
    definition: 'Toxic, undigested metabolic waste byproduct resulting from impaired Agni, causing channel blockage and disease.',
  },
  'Ojas': {
    path: '/glossary/term/ojas',
    category: 'Sharira / Physiology',
    definition: 'The subtle essence of all seven tissue dhatus, representing physical immunity, vitality, and mental resilience.',
  },
  'Prana': {
    path: '/glossary/term/prana',
    category: 'Sharira / Physiology',
    definition: 'The vital life-force energy animating respiratory function, sensory perception, and nervous system impulses.',
  },
  'Dhatu': {
    path: '/glossary/term/dhatu',
    category: 'Sharira / Anatomy',
    definition: 'The seven fundamental bodily tissues (Rasa, Rakta, Mamsa, Meda, Asthi, Majja, Shukra) sustaining anatomical life.',
  },
  'Srotas': {
    path: '/glossary/term/srotas',
    category: 'Sharira / Anatomy',
    definition: 'Microscopic and macroscopic anatomical channels transporting nutrients, wastes, and nervous system energy.',
  },
  'Rasayana': {
    path: '/glossary/term/rasayana',
    category: 'Chikitsa / Treatment',
    definition: 'Rejuvenative therapies, herbs, and protocols designed to rebuild stamina, prevent premature aging, and enhance longevity.',
  },
  'Abhyanga': {
    path: '/glossary/term/abhyanga',
    category: 'Chikitsa / Treatment',
    definition: 'Traditional Ayurvedic warm herbal oil body massage that nourishes tissues, pacifies Vata dosha, and enhances circulation.',
  },
};

export function applyWikipediaInterlinks(htmlContent: string): string {
  if (!htmlContent) return htmlContent;

  let processedHtml = htmlContent;
  const replacedTerms = new Set<string>();

  for (const [term, meta] of Object.entries(INTERLINK_MAP)) {
    if (replacedTerms.has(term.toLowerCase())) continue;

    // Matches term outside existing HTML tags and outside <a>...</a> anchors
    const regex = new RegExp(`(?<!<[^>]*)\\b(${term})\\b(?![^<]*>|[^<]*<\\/a>)`, 'i');

    if (regex.test(processedHtml)) {
      const tooltipHtml = `
<span class="ayur-tooltip-wrapper group relative inline-block">
  <a href="${meta.path}" class="text-ayur-emerald font-medium underline decoration-ayur-emerald/40 underline-offset-4 hover:decoration-ayur-emerald hover:text-ayur-forest transition-colors" title="Explore ${term} on AyurShakti">$1</a>
  <span class="ayur-tooltip-card absolute bottom-full left-1/2 mb-2 w-72 p-4 rounded-2xl bg-white border border-ayur-gold/30 shadow-card z-50 text-left text-xs space-y-2 font-normal text-ayur-sage">
    <span class="flex items-center justify-between border-b border-ayur-gold/20 pb-1.5 font-sans">
      <span class="font-serif font-bold text-ayur-forest text-sm">${term}</span>
      <span class="px-2 py-0.5 rounded-full bg-ayur-forest/10 text-ayur-forest text-[10px] uppercase font-semibold">${meta.category}</span>
    </span>
    <span class="block text-ayur-sage leading-relaxed font-sans">${meta.definition}</span>
    <span class="block text-[11px] font-bold text-ayur-emerald border-t border-ayur-gold/10 pt-1 font-sans">Click to explore full guide →</span>
  </span>
</span>`.trim();

      processedHtml = processedHtml.replace(regex, tooltipHtml);
      replacedTerms.add(term.toLowerCase());
    }
  }

  return processedHtml;
}
