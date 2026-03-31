'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowRight, Cpu, Eye, Search, Database, GraduationCap, Bot, Gamepad2, Brain, type LucideIcon } from 'lucide-react';
import type { Season } from '@/data/seasons';

const iconMap: Record<string, LucideIcon> = {
  Cpu, Eye, Search, Database, GraduationCap, Bot, Gamepad2, Brain,
};

export function SeasonCard({ season, index }: { season: Season; index: number }) {
  const Icon = iconMap[season.icon] || Cpu;

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{ duration: 0.5, delay: index * 0.08 }}
    >
      <Link
        href={`/season/${season.id}`}
        data-testid={`season-card-${season.id}`}
        className="group block h-full"
      >
        <div
          className="glass-card h-full p-6 md:p-8 transition-all duration-500 hover:translate-y-[-4px] glow"
          style={{ '--glow-color': `${season.color}30` } as React.CSSProperties}
        >
          <div className="flex items-start justify-between mb-6">
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center transition-transform duration-300 group-hover:scale-110"
              style={{ backgroundColor: `${season.color}15`, border: `1px solid ${season.color}30` }}
            >
              <Icon className="w-6 h-6" style={{ color: season.color }} />
            </div>
            <span
              className="font-accent text-xs font-bold tracking-widest uppercase"
              style={{ color: season.color }}
              data-testid={`season-badge-${season.id}`}
            >
              S{season.id}
            </span>
          </div>

          <h3 className="font-heading font-bold text-xl mb-1 text-white group-hover:text-white transition-colors">
            {season.title}
          </h3>
          <p className="text-sm font-medium mb-3" style={{ color: season.color }}>
            {season.subtitle}
          </p>
          <p className="text-sm text-genesis-muted leading-relaxed mb-6 line-clamp-3">
            {season.description}
          </p>

          <div className="flex items-center justify-between">
            <span className="text-xs text-zinc-600">
              {season.episodes.length} episodes
            </span>
            <div
              className="flex items-center gap-1 text-xs font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300"
              style={{ color: season.color }}
            >
              Explore <ArrowRight className="w-3 h-3" />
            </div>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
