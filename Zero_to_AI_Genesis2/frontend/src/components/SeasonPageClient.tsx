'use client';

import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Cpu, Eye, Search, Database, GraduationCap, Bot, Gamepad2, Brain, type LucideIcon } from 'lucide-react';
import Link from 'next/link';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { EpisodeDetail } from '@/components/EpisodeDetail';
import { seasons } from '@/data/seasons';

const iconMap: Record<string, LucideIcon> = {
  Cpu, Eye, Search, Database, GraduationCap, Bot, Gamepad2, Brain,
};

export function SeasonPageClient({ seasonId }: { seasonId: number }) {
  const season = seasons.find((entry) => entry.id === seasonId);

  if (!season) {
    return null;
  }

  const Icon = iconMap[season.icon] || Cpu;
  const prevSeason = seasons.find((entry) => entry.id === seasonId - 1);
  const nextSeason = seasons.find((entry) => entry.id === seasonId + 1);

  return (
    <main className="min-h-screen grid-bg" data-testid={`season-page-${seasonId}`}>
      <Navbar />

      <section className="relative pt-32 pb-16 overflow-hidden">
        <div className="absolute inset-0 pointer-events-none">
          <div
            className="absolute top-20 right-1/4 w-[500px] h-[500px] rounded-full opacity-15 blur-[150px]"
            style={{ background: season.color }}
          />
        </div>

        <div className="relative z-10 max-w-5xl mx-auto px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Link
              href="/"
              data-testid="back-to-home"
              className="inline-flex items-center gap-2 text-sm text-genesis-muted hover:text-white transition-colors mb-8"
            >
              <ArrowLeft className="w-4 h-4" /> Back to Home
            </Link>

            <div className="flex items-center gap-4 mb-6">
              <div
                className="w-16 h-16 rounded-2xl flex items-center justify-center"
                style={{ backgroundColor: `${season.color}15`, border: `1px solid ${season.color}30` }}
              >
                <Icon className="w-8 h-8" style={{ color: season.color }} />
              </div>
              <div>
                <span
                  className="font-accent text-xs font-bold tracking-[0.2em] uppercase"
                  style={{ color: season.color }}
                >
                  Season {season.id}
                </span>
                <h1 className="font-heading font-extrabold text-3xl md:text-5xl tracking-tight text-white">
                  {season.subtitle}
                </h1>
              </div>
            </div>

            <p className="text-lg text-genesis-muted max-w-3xl leading-relaxed mb-8">
              {season.description}
            </p>

            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2">
                <div
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: season.color, boxShadow: `0 0 8px ${season.color}` }}
                />
                <span className="text-sm text-genesis-muted">
                  {season.episodes.length} Episodes
                </span>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="pb-24" data-testid="episodes-section">
        <div className="max-w-5xl mx-auto px-6 md:px-12">
          <div className="space-y-4">
            {season.episodes.map((episode) => (
              <EpisodeDetail
                key={episode.id}
                episode={episode}
                color={season.color}
                seasonId={season.id}
              />
            ))}
          </div>
        </div>
      </section>

      <section className="pb-24" data-testid="season-navigation">
        <div className="max-w-5xl mx-auto px-6 md:px-12">
          <div className="flex items-center justify-between gap-4">
            {prevSeason ? (
              <Link
                href={`/season/${prevSeason.id}`}
                data-testid="prev-season-link"
                className="group glass-card p-4 flex items-center gap-3 hover:translate-x-[-4px] transition-all duration-300"
              >
                <ArrowLeft className="w-4 h-4 text-genesis-muted group-hover:text-white transition-colors" />
                <div>
                  <span className="text-[10px] font-accent tracking-wider text-genesis-dim block">Previous</span>
                  <span className="text-sm font-heading font-semibold text-white">
                    S{prevSeason.id}: {prevSeason.subtitle}
                  </span>
                </div>
              </Link>
            ) : <div />}

            {nextSeason ? (
              <Link
                href={`/season/${nextSeason.id}`}
                data-testid="next-season-link"
                className="group glass-card p-4 flex items-center gap-3 hover:translate-x-[4px] transition-all duration-300 text-right"
              >
                <div>
                  <span className="text-[10px] font-accent tracking-wider text-genesis-dim block">Next</span>
                  <span className="text-sm font-heading font-semibold text-white">
                    S{nextSeason.id}: {nextSeason.subtitle}
                  </span>
                </div>
                <ArrowRight className="w-4 h-4 text-genesis-muted group-hover:text-white transition-colors" />
              </Link>
            ) : <div />}
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}