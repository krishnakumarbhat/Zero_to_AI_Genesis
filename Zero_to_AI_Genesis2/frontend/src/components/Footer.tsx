'use client';

import { Brain, Github, ExternalLink } from 'lucide-react';
import Link from 'next/link';

export function Footer() {
  return (
    <footer data-testid="footer" className="border-t border-white/5 bg-black/40 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-6 md:px-12 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          <div className="md:col-span-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-season-7 to-season-1 flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <span className="font-heading font-bold text-lg">Zero to AI Genesis</span>
            </div>
            <p className="text-sm text-genesis-muted leading-relaxed max-w-md">
              An educational from-scratch AI learning repository spanning 7+ seasons.
              From classic ML to LLM alignment, with explicit equations and lightweight implementations.
            </p>
          </div>

          <div>
            <h4 className="font-heading font-semibold text-sm uppercase tracking-wider mb-4 text-genesis-muted">Seasons</h4>
            <div className="flex flex-col gap-2">
              {Array.from({ length: 8 }, (_, i) => (
                <Link
                  key={i}
                  href={`/season/${i}`}
                  className="text-sm text-zinc-500 hover:text-white transition-colors duration-200"
                >
                  Season {i}
                </Link>
              ))}
            </div>
          </div>

          <div>
            <h4 className="font-heading font-semibold text-sm uppercase tracking-wider mb-4 text-genesis-muted">Links</h4>
            <div className="flex flex-col gap-2">
              <a
                href="https://github.com/krishnakumarbhat/Zero_to_AI_Genesis"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-zinc-500 hover:text-white transition-colors duration-200 flex items-center gap-2"
              >
                <Github className="w-4 h-4" /> GitHub
              </a>
              <a
                href="#"
                className="text-sm text-zinc-500 hover:text-white transition-colors duration-200 flex items-center gap-2"
              >
                <ExternalLink className="w-4 h-4" /> Documentation
              </a>
            </div>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-xs text-zinc-600">Apache 2.0 License</p>
          <p className="text-xs text-zinc-600">
            Teaching implementations on dummy/synthetic data. Not for production.
          </p>
        </div>
      </div>
    </footer>
  );
}
