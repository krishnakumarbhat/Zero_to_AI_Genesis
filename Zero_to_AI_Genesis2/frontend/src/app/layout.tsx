import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Zero to AI Genesis',
  description: 'An educational from-scratch AI learning repository spanning 7+ seasons — from classic ML to LLM alignment.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-genesis-bg text-genesis-text font-body antialiased noise-overlay">
        {children}
      </body>
    </html>
  );
}
