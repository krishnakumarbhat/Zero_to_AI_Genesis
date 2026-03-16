'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { seasons } from '@/data/seasons';

export function RoadmapTimeline() {
  return (
    <div data-testid="roadmap-timeline" className="relative">
      {/* Vertical connecting line */}
      <div className="absolute left-6 md:left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-white/10 to-transparent" />

      <div className="flex flex-col gap-0">
        {seasons.map((season, i) => {
          const isLeft = i % 2 === 0;
          return (
            <motion.div
              key={season.id}
              initial={{ opacity: 0, x: isLeft ? -40 : 40 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: '-80px' }}
              transition={{ duration: 0.5, delay: i * 0.05 }}
              className="relative py-6 md:py-8"
            >
              {/* Node dot */}
              <div
                className="absolute left-6 md:left-1/2 top-1/2 -translate-y-1/2 -translate-x-1/2 z-10"
              >
                <div
                  className="w-4 h-4 rounded-full border-2 transition-all duration-300 hover:scale-150"
                  style={{
                    borderColor: season.color,
                    backgroundColor: `${season.color}40`,
                    boxShadow: `0 0 20px ${season.color}40`,
                  }}
                />
              </div>

              {/* Content card */}
              <div className={`md:w-[calc(50%-40px)] ${isLeft ? 'ml-16 md:ml-0 md:mr-auto' : 'ml-16 md:ml-auto'}`}>
                <Link
                  href={`/season/${season.id}`}
                  data-testid={`roadmap-season-${season.id}`}
                  className="group block"
                >
                  <div
                    className="glass-card p-5 transition-all duration-300 hover:translate-y-[-2px]"
                    style={{
                      borderColor: `${season.color}15`,
                    }}
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <span
                        className="font-accent text-[10px] font-bold tracking-widest px-2 py-0.5 rounded-full"
                        style={{
                          color: season.color,
                          backgroundColor: `${season.color}15`,
                          border: `1px solid ${season.color}25`,
                        }}
                      >
                        S{season.id}
                      </span>
                      <h4 className="font-heading font-semibold text-sm text-white">
                        {season.subtitle}
                      </h4>
                    </div>
                    <p className="text-xs text-genesis-muted leading-relaxed line-clamp-2">
                      {season.description}
                    </p>
                    <div className="mt-3 text-[10px] text-zinc-600">
                      {season.episodes.length} episodes
                    </div>
                  </div>
                </Link>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
