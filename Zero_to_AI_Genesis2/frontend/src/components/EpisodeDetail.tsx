'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, BookOpen, Lightbulb } from 'lucide-react';
import { useState } from 'react';
import { AlgorithmFlow } from './AlgorithmFlow';
import type { Episode } from '@/data/seasons';

export function EpisodeDetail({ episode, color, seasonId }: { episode: Episode; color: string; seasonId: number }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <motion.div
      data-testid={`episode-${seasonId}-${episode.id}`}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4 }}
      className="glass-card overflow-hidden"
    >
      <button
        data-testid={`episode-toggle-${seasonId}-${episode.id}`}
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-6 flex items-start gap-4 text-left hover:bg-white/[0.02] transition-colors duration-200"
      >
        <div
          className="w-10 h-10 rounded-lg flex-shrink-0 flex items-center justify-center font-accent text-sm font-bold"
          style={{
            backgroundColor: `${color}15`,
            color: color,
            border: `1px solid ${color}25`,
          }}
        >
          {episode.id.toString().padStart(2, '0')}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-heading font-semibold text-white text-lg mb-1">
            {episode.title}
          </h3>
          <p className="text-sm" style={{ color }}>{episode.subtitle}</p>
        </div>
        <ChevronDown
          className={`w-5 h-5 text-genesis-muted flex-shrink-0 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}
        />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: 'easeInOut' }}
            className="overflow-hidden"
          >
            <div className="px-6 pb-6 space-y-6">
              <div className="pl-14">
                <div className="flex items-start gap-2 mb-4">
                  <BookOpen className="w-4 h-4 text-genesis-muted flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-genesis-muted leading-relaxed">
                    {episode.description}
                  </p>
                </div>

                {episode.keyEquation && (
                  <div
                    className="mb-4 p-3 rounded-lg font-mono text-sm"
                    style={{
                      backgroundColor: `${color}08`,
                      border: `1px solid ${color}15`,
                      color: '#d4d4d8',
                    }}
                    data-testid={`equation-${seasonId}-${episode.id}`}
                  >
                    <span className="text-[10px] font-accent tracking-wider block mb-1" style={{ color }}>KEY EQUATION</span>
                    {episode.keyEquation}
                  </div>
                )}

                <div className="flex items-start gap-2 mb-6">
                  <Lightbulb className="w-4 h-4 flex-shrink-0 mt-0.5" style={{ color }} />
                  <div className="flex flex-wrap gap-2">
                    {episode.concepts.map((concept) => (
                      <span
                        key={concept}
                        className="px-2.5 py-1 rounded-full text-[11px] font-medium"
                        style={{
                          backgroundColor: `${color}10`,
                          color: `${color}cc`,
                          border: `1px solid ${color}20`,
                        }}
                      >
                        {concept}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <AlgorithmFlow episode={episode} color={color} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
