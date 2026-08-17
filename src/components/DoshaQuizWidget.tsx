'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { HeartPulse, CheckCircle2, RotateCcw, ArrowRight, Sparkles } from 'lucide-react';
import Link from 'next/link';

interface Question {
  id: number;
  question: string;
  options: {
    text: string;
    dosha: 'vata' | 'pitta' | 'kapha';
  }[];
}

const QUESTIONS: Question[] = [
  {
    id: 1,
    question: "How do you typically react under stress or heavy workload?",
    options: [
      { text: "Feel anxious, restless, or trouble sleeping (Vata)", dosha: 'vata' },
      { text: "Become irritable, impatient, or prone to acidity/heat (Pitta)", dosha: 'pitta' },
      { text: "Feel sluggish, slow to act, or seek comfort food (Kapha)", dosha: 'kapha' },
    ],
  },
  {
    id: 2,
    question: "What best describes your digestion & appetite (Agni)?",
    options: [
      { text: "Irregular — sometimes high appetite, sometimes bloated/gassy (Vata)", dosha: 'vata' },
      { text: "Strong & intense — get angry if meals are delayed, prone to heartburn (Pitta)", dosha: 'pitta' },
      { text: "Slow & steady — can skip meals easily, but slow digestion (Kapha)", dosha: 'kapha' },
    ],
  },
  {
    id: 3,
    question: "What type of climate or temperature affects you most?",
    options: [
      { text: "Dislike cold & windy weather, prefer warm cozy environments (Vata)", dosha: 'vata' },
      { text: "Dislike hot weather, sweat easily, prefer cool breeze (Pitta)", dosha: 'pitta' },
      { text: "Dislike cold & humid damp weather, thrive in warm dry weather (Kapha)", dosha: 'kapha' },
    ],
  },
];

export default function DoshaQuizWidget() {
  const [currentStep, setCurrentStep] = useState(0);
  const [scores, setScores] = useState({ vata: 0, pitta: 0, kapha: 0 });
  const [quizCompleted, setQuizCompleted] = useState(false);

  const handleSelectOption = (dosha: 'vata' | 'pitta' | 'kapha') => {
    const updatedScores = { ...scores, [dosha]: scores[dosha] + 1 };
    setScores(updatedScores);

    if (currentStep + 1 < QUESTIONS.length) {
      setCurrentStep(currentStep + 1);
    } else {
      setQuizCompleted(true);
    }
  };

  const resetQuiz = () => {
    setCurrentStep(0);
    setScores({ vata: 0, pitta: 0, kapha: 0 });
    setQuizCompleted(false);
  };

  const getDominantDosha = () => {
    if (scores.vata >= scores.pitta && scores.vata >= scores.kapha) {
      return {
        name: 'Vata Imbalance',
        desc: 'Air & Ether element dominance. You benefit from grounding, warming adaptogens like Ashwagandha and Sesame Oil Abhyanga.',
        herb: 'Ashwagandha & Brahmi',
        articleSlug: 'ashwagandha-benefits-for-men-complete',
      };
    }
    if (scores.pitta >= scores.vata && scores.pitta >= scores.kapha) {
      return {
        name: 'Pitta Imbalance',
        desc: 'Fire & Water element dominance. You benefit from cooling, digestive-soothing herbs like Shatavari, Guduchi (Giloy), and Coconut Oil.',
        herb: 'Shatavari & Giloy',
        articleSlug: 'shatavari-benefits-for-women-ayurvedic',
      };
    }
    return {
      name: 'Kapha Imbalance',
      desc: 'Earth & Water element dominance. You benefit from stimulating, detoxifying herbs like Triphala, Tulsi, and Ginger Agni tea.',
      herb: 'Triphala & Tulsi',
      articleSlug: 'ayurvedic-remedies-for-gut-health-7',
    };
  };

  const result = getDominantDosha();

  return (
    <div className="glass-panel-gold rounded-3xl p-8 sm:p-12 shadow-soft-glow relative overflow-hidden my-16 max-w-4xl mx-auto border border-ayur-gold/30">
      
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-full bg-ayur-forest text-ayur-gold flex items-center justify-center font-serif font-bold">
          <HeartPulse className="w-5 h-5 text-ayur-gold" />
        </div>
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-ayur-gold">Interactive Ayurvedic Self-Assessment</span>
          <h2 className="font-serif text-2xl sm:text-3xl font-bold text-ayur-forest">Find Your Primary Dosha Prakriti</h2>
        </div>
      </div>

      <AnimatePresence mode="wait">
        {!quizCompleted ? (
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.4 }}
            className="space-y-6"
          >
            <div className="flex justify-between items-center text-xs font-semibold text-ayur-sage">
              <span>Question {currentStep + 1} of {QUESTIONS.length}</span>
              <div className="flex gap-1.5">
                {QUESTIONS.map((_, idx) => (
                  <div
                    key={idx}
                    className={`h-1.5 rounded-full transition-all ${
                      idx === currentStep ? 'w-6 bg-ayur-emerald' : 'w-2 bg-ayur-border'
                    }`}
                  />
                ))}
              </div>
            </div>

            <h3 className="text-lg sm:text-xl font-serif font-semibold text-ayur-forest">
              {QUESTIONS[currentStep].question}
            </h3>

            <div className="space-y-3 pt-2">
              {QUESTIONS[currentStep].options.map((option, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSelectOption(option.dosha)}
                  className="w-full text-left p-4 rounded-xl bg-white border border-ayur-border hover:border-ayur-emerald hover:bg-ayur-sand/80 transition-all text-sm font-medium text-ayur-forest flex items-center justify-between group shadow-sm hover:shadow-md"
                >
                  <span>{option.text}</span>
                  <ArrowRight className="w-4 h-4 text-ayur-sage group-hover:text-ayur-emerald group-hover:translate-x-1 transition-all" />
                </button>
              ))}
            </div>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
            className="space-y-6 text-center py-4"
          >
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-100 text-ayur-emerald text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-4 h-4" /> Assessment Result
            </div>

            <h3 className="font-serif text-3xl font-bold text-ayur-forest">
              {result.name}
            </h3>

            <p className="text-sm text-ayur-sage max-w-xl mx-auto leading-relaxed">
              {result.desc}
            </p>

            <div className="p-4 rounded-2xl bg-white border border-ayur-border max-w-md mx-auto text-left flex items-start gap-3 shadow-sm">
              <CheckCircle2 className="w-5 h-5 text-ayur-emerald shrink-0 mt-0.5" />
              <div>
                <span className="text-xs font-bold text-ayur-forest uppercase tracking-wider">Recommended Botanicals:</span>
                <p className="text-sm font-serif font-bold text-ayur-emerald">{result.herb}</p>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link
                href={`/articles`}
                className="px-6 py-3 rounded-full bg-ayur-forest text-ayur-bg text-xs font-semibold uppercase tracking-wider shadow-md hover:bg-ayur-emerald transition-all"
              >
                Read Recommended Protocols
              </Link>
              <button
                onClick={resetQuiz}
                className="px-6 py-3 rounded-full border border-ayur-border text-ayur-forest text-xs font-semibold uppercase tracking-wider hover:bg-white transition-all flex items-center gap-2"
              >
                <RotateCcw className="w-4 h-4 text-ayur-sage" /> Retake Quiz
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
