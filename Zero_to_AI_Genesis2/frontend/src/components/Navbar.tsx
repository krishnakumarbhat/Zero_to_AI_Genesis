'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Brain, Menu, X } from 'lucide-react';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';

export function Navbar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  const links = [
    { href: '/', label: 'Home' },
    { href: '/#roadmap', label: 'Roadmap' },
    { href: '/#seasons', label: 'Seasons' },
    { href: '/#equations', label: 'Equations' },
  ];

  return (
    <nav
      data-testid="navbar"
      className="fixed top-0 left-0 right-0 z-50 h-16 flex items-center justify-between px-6 md:px-12 bg-black/60 backdrop-blur-xl border-b border-white/5"
    >
      <Link href="/" className="flex items-center gap-3 group" data-testid="nav-logo">
        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-season-7 to-season-1 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
          <Brain className="w-5 h-5 text-white" />
        </div>
        <span className="font-heading font-bold text-lg tracking-tight hidden sm:block">
          Zero to AI <span className="text-season-7">Genesis</span>
        </span>
      </Link>

      <div className="hidden md:flex items-center gap-8">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            data-testid={`nav-link-${link.label.toLowerCase()}`}
            className={cn(
              'text-sm font-medium tracking-wide transition-colors duration-200 hover:text-white',
              pathname === link.href ? 'text-white' : 'text-genesis-muted'
            )}
          >
            {link.label}
          </Link>
        ))}
      </div>

      <button
        data-testid="mobile-menu-toggle"
        className="md:hidden p-2 text-genesis-muted hover:text-white transition-colors"
        onClick={() => setMobileOpen(!mobileOpen)}
      >
        {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute top-16 left-0 right-0 bg-black/95 backdrop-blur-xl border-b border-white/5 md:hidden"
          >
            <div className="flex flex-col p-6 gap-4">
              {links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className="text-sm font-medium text-genesis-muted hover:text-white transition-colors"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
