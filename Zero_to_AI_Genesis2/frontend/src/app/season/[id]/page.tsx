import { notFound } from 'next/navigation';
import { SeasonPageClient } from '@/components/SeasonPageClient';
import { seasons } from '@/data/seasons';

export function generateStaticParams() {
  return seasons.map((season) => ({ id: season.id.toString() }));
}

export const dynamicParams = false;

export default function SeasonPage({ params }: { params: { id: string } }) {
  const seasonId = Number(params.id);
  const season = seasons.find((s) => s.id === seasonId);

  if (!season) {
    notFound();
  }

  return <SeasonPageClient seasonId={seasonId} />;
}
