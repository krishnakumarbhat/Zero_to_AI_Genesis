# Zero to AI Genesis - PRD

## Original Problem Statement
Build an interactive, highly animated frontend for the "Zero to AI Genesis" educational AI learning repository, plus expand the README.md with detailed Mermaid flowcharts for all 8 seasons.

## Architecture
- **Frontend**: Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **Visualization**: React Flow (architecture diagrams), Framer Motion (UI animations)
- **Backend**: Minimal FastAPI (health endpoint only)
- **Theme**: Dark futuristic "AI Lab" with season-specific neon accents

## User Personas
- AI/ML students learning from scratch
- Developers exploring algorithm internals
- Researchers reviewing foundational implementations

## Core Requirements (Static)
1. Interactive frontend with season/episode navigation
2. Animated algorithm flow diagrams for every episode
3. Dark futuristic theme with glassmorphism and glow effects
4. Expanded README.md with Mermaid flowcharts for all 8 seasons
5. Responsive design (mobile + desktop)

## What's Been Implemented (2026-03-15)
- [x] Next.js App Router setup with TypeScript + Tailwind CSS
- [x] Landing page with hero, roadmap timeline, season cards grid, setup section, equations section, project structure
- [x] Season pages (/season/0 through /season/7) with episode accordion
- [x] React Flow algorithm diagrams for every episode across all 8 seasons
- [x] 50+ episodes with detailed descriptions, concepts, key equations, and flow nodes
- [x] Framer Motion page transitions and micro-interactions
- [x] Glassmorphism cards, glow effects, noise overlay, grid background
- [x] Navbar with mobile responsive menu
- [x] Footer with season links and GitHub link
- [x] Expanded README.md with Mermaid flowcharts for S0-S7
- [x] Season navigation (prev/next) on season pages

## Prioritized Backlog
### P0 - None remaining
### P1
- D3.js mathematical visualizations (gradient descent, Q-table updates, loss surfaces)
- KaTeX rendering for inline LaTeX equations
### P2
- Search/filter functionality across episodes
- Dark/light mode toggle (user mentioned dark only for now)
- Episode bookmarking / progress tracking
- Code syntax highlighting for algorithm source code display

## Next Tasks
1. Add D3.js interactive algorithm visualizers (Q-learning table animation, gradient descent steps, loss surface visualization)
2. Implement KaTeX for proper LaTeX equation rendering
3. Add episode source code viewer with syntax highlighting
4. Consider adding a search bar for finding specific topics across seasons
