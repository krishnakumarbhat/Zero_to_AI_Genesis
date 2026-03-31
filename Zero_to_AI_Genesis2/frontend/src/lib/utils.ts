import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export const SEASON_COLORS = [
  '#4CAF50',
  '#2196F3',
  '#FF9800',
  '#9C27B0',
  '#F44336',
  '#00BCD4',
  '#FF5722',
  '#673AB7',
] as const;

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}