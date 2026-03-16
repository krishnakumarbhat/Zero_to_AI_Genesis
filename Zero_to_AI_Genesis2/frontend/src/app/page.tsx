'use client';

import { motion } from 'framer-motion';
import { ArrowDown, Terminal, BookOpen, Beaker, Github, ChevronRight, Zap, Code, Layers } from 'lucide-react';
import Link from 'next/link';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { SeasonCard } from '@/components/SeasonCard';
import { RoadmapTimeline } from '@/components/RoadmapTimeline';
import { seasons } from '@/data/seasons';
import { SEASON_COLORS } from '@/lib/utils';

const stagger = {
  animate: { transition: { staggerChildren: 0.1 } },
};

const fadeUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.6, ease: 'easeOut' } },
};

export default function HomePage() {
  return (
    <main className="min-h-screen" data-testid="home-page">
      <Navbar />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden grid-bg" data-testid="hero-section">
        {/* Animated glow orbs */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full opacity-20 blur-[120px] animate-float" style={{ background: SEASON_COLORS[7] }} />
          <div className="absolute bottom-1/3 right-1/4 w-80 h-80 rounded-full opacity-15 blur-[100px] animate-float" style={{ background: SEASON_COLORS[1], animationDelay: '2s' }} />
          <div className="absolute top-2/3 left-1/2 w-64 h-64 rounded-full opacity-10 blur-[80px] animate-float" style={{ background: SEASON_COLORS[0], animationDelay: '4s' }} />
        </div>

        <motion.div
          initial="initial"
          animate="animate"
          variants={stagger}
          className="relative z-10 max-w-5xl mx-auto px-6 md:px-12 text-center pt-24"
        >
          <motion.div variants={fadeUp} className="mb-6">
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-medium tracking-wide border border-white/10 bg-white/5 text-genesis-muted">
              <Zap className="w-3 h-3 text-season-0" />
              8 Seasons &middot; 50+ Episodes &middot; From Scratch
            </span>
          </motion.div>

          <motion.h1 variants={fadeUp} className="font-heading font-extrabold text-5xl sm:text-6xl md:text-8xl tracking-tighter leading-[0.9] mb-6">
            <span className="gradient-text">Zero to AI</span>
            <br />
            <span className="text-white">Genesis</span>
          </motion.h1>

          <motion.p variants={fadeUp} className="text-lg md:text-xl text-genesis-muted max-w-2xl mx-auto mb-10 leading-relaxed">
            An educational from-scratch AI learning repository spanning 7+ seasons.
            From classic ML to LLM alignment, with explicit equations and lightweight implementations.
          </motion.p>

          <motion.div variants={fadeUp} className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link
              href="#seasons"
              data-testid="explore-seasons-btn"
              className="group relative px-8 py-3.5 rounded-full font-heading font-semibold text-sm tracking-wide bg-white text-black hover:bg-zinc-200 transition-all duration-300 hover:scale-105 active:scale-95 shadow-[0_0_30px_rgba(255,255,255,0.2)]"
            >
              Explore Seasons
              <ChevronRight className="w-4 h-4 inline-block ml-1 group-hover:translate-x-1 transition-transform" />
            </Link>
            <a
              href="https://github.com/krishnakumarbhat/Zero_to_AI_Genesis"
              target="_blank"
              rel="noopener noreferrer"
              data-testid="github-btn"
              className="flex items-center gap-2 px-8 py-3.5 rounded-full font-heading font-semibold text-sm tracking-wide border border-white/15 text-white hover:bg-white/5 hover:border-white/30 transition-all duration-300"
            >
              <Github className="w-4 h-4" /> GitHub
            </a>
          </motion.div>

          <motion.div variants={fadeUp}>
            <Link href="#roadmap" className="inline-flex flex-col items-center gap-2 text-genesis-dim hover:text-genesis-muted transition-colors">
              <span className="text-xs tracking-wider uppercase">Scroll to explore</span>
              <ArrowDown className="w-4 h-4 animate-bounce" />
            </Link>
          </motion.div>
        </motion.div>
      </section>

      {/* Tech Stack Section */}
      <section className="py-24 border-t border-white/5">
        <div className="max-w-7xl mx-auto px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-4 gap-6"
          >
            {[
              { icon: Code, label: 'NumPy First', desc: 'Pure Python & NumPy', color: SEASON_COLORS[0] },
              { icon: Layers, label: 'PyTorch Minimal', desc: 'Deep Learning Core', color: SEASON_COLORS[1] },
              { icon: Beaker, label: 'LaTeX Inline', desc: 'Explicit Equations', color: SEASON_COLORS[3] },
              { icon: Terminal, label: 'From Scratch', desc: 'No High-Level Frameworks', color: SEASON_COLORS[6] },
            ].map((item, i) => (
              <motion.div
                key={item.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="glass-card p-6 text-center"
              >
                <item.icon className="w-6 h-6 mx-auto mb-3" style={{ color: item.color }} />
                <h4 className="font-heading font-semibold text-sm text-white mb-1">{item.label}</h4>
                <p className="text-xs text-genesis-dim">{item.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Roadmap Section */}
      <section id="roadmap" className="py-24 md:py-32" data-testid="roadmap-section">
        <div className="max-w-5xl mx-auto px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <span className="text-xs font-accent tracking-[0.2em] uppercase text-season-7 mb-4 block">Learning Path</span>
            <h2 className="font-heading font-bold text-3xl md:text-5xl tracking-tight text-white">
              The Roadmap
            </h2>
            <p className="mt-4 text-genesis-muted max-w-xl">
              A structured journey through the entire landscape of AI and ML, from NumPy-first implementations to cutting-edge LLM alignment.
            </p>
          </motion.div>

          <RoadmapTimeline />
        </div>
      </section>

      {/* Seasons Grid */}
      <section id="seasons" className="py-24 md:py-32 border-t border-white/5" data-testid="seasons-section">
        <div className="max-w-7xl mx-auto px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <span className="text-xs font-accent tracking-[0.2em] uppercase text-season-1 mb-4 block">Curriculum</span>
            <h2 className="font-heading font-bold text-3xl md:text-5xl tracking-tight text-white">
              All Seasons
            </h2>
            <p className="mt-4 text-genesis-muted max-w-xl">
              Each season builds on the previous, with hands-on implementations and explicit mathematical foundations.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {seasons.map((season, i) => (
              <SeasonCard key={season.id} season={season} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* Setup Section */}
      <section className="py-24 md:py-32 border-t border-white/5" data-testid="setup-section">
        <div className="max-w-4xl mx-auto px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12"
          >
            <span className="text-xs font-accent tracking-[0.2em] uppercase text-season-5 mb-4 block">Quick Start</span>
            <h2 className="font-heading font-bold text-3xl md:text-5xl tracking-tight text-white">
              Setup & Run
            </h2>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass-card p-6 md:p-8 font-mono text-sm space-y-2"
          >
            <div className="flex items-center gap-2 mb-4 text-genesis-dim">
              <Terminal className="w-4 h-4" />
              <span className="text-xs font-accent tracking-wider">TERMINAL</span>
            </div>
            <p><span className="text-season-0">$</span> <span className="text-zinc-400">python3 -m venv .venv</span></p>
            <p><span className="text-season-0">$</span> <span className="text-zinc-400">source .venv/bin/activate</span></p>
            <p><span className="text-season-0">$</span> <span className="text-zinc-400">pip install -r requirements.txt</span></p>
            <p><span className="text-season-0">$</span> <span className="text-zinc-400">python3 src/data/make_dummy_data.py</span></p>
            <div className="border-t border-white/5 my-4" />
            <p className="text-genesis-dim text-xs mb-2"># Running episodes</p>
            <p><span className="text-season-6">$</span> <span className="text-zinc-400">python3 src/season_6/episode_00_exploration_foundations.py</span></p>
            <p><span className="text-season-7">$</span> <span className="text-zinc-400">python3 src/season_7/episode_00_sft.py</span></p>
          </motion.div>
        </div>
      </section>

      {/* Key Equations Section */}
      <section id="equations" className="py-24 md:py-32 border-t border-white/5" data-testid="equations-section">
        <div className="max-w-5xl mx-auto px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12"
          >
            <span className="text-xs font-accent tracking-[0.2em] uppercase text-season-4 mb-4 block">Mathematics</span>
            <h2 className="font-heading font-bold text-3xl md:text-5xl tracking-tight text-white">
              Key Equations
            </h2>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* RL Equations */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="glass-card p-6 md:p-8"
              style={{ borderColor: `${SEASON_COLORS[6]}15` }}
            >
              <div className="flex items-center gap-2 mb-6">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${SEASON_COLORS[6]}15` }}>
                  <BookOpen className="w-4 h-4" style={{ color: SEASON_COLORS[6] }} />
                </div>
                <h3 className="font-heading font-semibold" style={{ color: SEASON_COLORS[6] }}>RL Core (Season 6)</h3>
              </div>
              <div className="space-y-4 font-mono text-sm">
                <div className="p-3 rounded-lg bg-white/[0.02] border border-white/5">
                  <span className="text-[10px] text-genesis-dim block mb-1">Expected Return</span>
                  <span className="text-zinc-300">{`G_t = sum(gamma^k * R_{t+k+1})`}</span>
                </div>
                <div className="p-3 rounded-lg bg-white/[0.02] border border-white/5">
                  <span className="text-[10px] text-genesis-dim block mb-1">Bellman Optimality</span>
                  <span className="text-zinc-300">{`V*(s) = max_a sum P(s',r|s,a)[r + gamma*V*(s')]`}</span>
                </div>
                <div className="p-3 rounded-lg bg-white/[0.02] border border-white/5">
                  <span className="text-[10px] text-genesis-dim block mb-1">PPO Clipped Surrogate</span>
                  <span className="text-zinc-300">{`L_CLIP = E[min(r_t*A_t, clip(r_t,1-e,1+e)*A_t)]`}</span>
                </div>
              </div>
            </motion.div>

            {/* LLM Equations */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="glass-card p-6 md:p-8"
              style={{ borderColor: `${SEASON_COLORS[7]}15` }}
            >
              <div className="flex items-center gap-2 mb-6">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${SEASON_COLORS[7]}15` }}>
                  <BookOpen className="w-4 h-4" style={{ color: SEASON_COLORS[7] }} />
                </div>
                <h3 className="font-heading font-semibold" style={{ color: SEASON_COLORS[7] }}>LLM Alignment (Season 7)</h3>
              </div>
              <div className="space-y-4 font-mono text-sm">
                <div className="p-3 rounded-lg bg-white/[0.02] border border-white/5">
                  <span className="text-[10px] text-genesis-dim block mb-1">DPO Loss</span>
                  <span className="text-zinc-300">{`L_DPO = -E[log sigma(beta*log(pi/pi_ref)(y_w) - beta*log(pi/pi_ref)(y_l))]`}</span>
                </div>
                <div className="p-3 rounded-lg bg-white/[0.02] border border-white/5">
                  <span className="text-[10px] text-genesis-dim block mb-1">LoRA</span>
                  <span className="text-zinc-300">{`W = W_0 + delta_W = W_0 + BA, r << d,k`}</span>
                </div>
                <div className="p-3 rounded-lg bg-white/[0.02] border border-white/5">
                  <span className="text-[10px] text-genesis-dim block mb-1">GRPO Advantage</span>
                  <span className="text-zinc-300">{`A_i = (r_i - mean(r_1..r_G)) / std(r_1..r_G)`}</span>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Project Structure Section */}
      <section className="py-24 md:py-32 border-t border-white/5" data-testid="structure-section">
        <div className="max-w-4xl mx-auto px-6 md:px-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-12"
          >
            <span className="text-xs font-accent tracking-[0.2em] uppercase text-season-2 mb-4 block">Architecture</span>
            <h2 className="font-heading font-bold text-3xl md:text-5xl tracking-tight text-white">
              Project Structure
            </h2>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass-card p-6 md:p-8 font-mono text-sm leading-loose"
          >
            <pre className="text-zinc-400 whitespace-pre overflow-x-auto">
{`Zero_to_AI_Genesis/
├── frontend/              # Interactive web application
│   ├── src/
│   │   ├── app/           # Next.js App Router pages
│   │   ├── components/    # React components
│   │   └── data/          # Season & episode data
│   └── package.json
├── src/
│   ├── season_0/          # Classic ML (NumPy)
│   ├── season_1/          # Deep Learning & Vision
│   ├── season_2/          # GOFAI (Search/Logic)
│   ├── season_3/          # Retrieval / RAG
│   ├── season_4/          # DL Foundations
│   ├── season_5/          # Agentic Workflows
│   ├── season_6/          # Reinforcement Learning
│   ├── season_7/          # LLM Fine-Tuning & Alignment
│   └── data/              # Dummy data generation
├── requirements.txt
├── .github/workflows/     # CI/CD pipeline
├── .gitignore
└── README.md`}
            </pre>
          </motion.div>
        </div>
      </section>

      {/* Scope Notice */}
      <section className="py-16 border-t border-white/5">
        <div className="max-w-4xl mx-auto px-6 md:px-12 text-center">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="glass-card p-6 inline-block"
            style={{ borderColor: '#eab30815' }}
          >
            <p className="text-sm text-genesis-muted">
              <span className="text-yellow-500 font-medium">Note:</span> These are teaching implementations on dummy/synthetic data.
              For production-grade training, use distributed systems and robust ML frameworks.
            </p>
          </motion.div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
