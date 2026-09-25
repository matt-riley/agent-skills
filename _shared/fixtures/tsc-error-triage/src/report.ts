import type { Priority, Ticket } from './types';

const ORDER: Record<Priority, number> = { urgent: 0, high: 1, low: 2 };

export function byUrgency(tickets: Ticket[]): Ticket[] {
  return [...tickets].sort((a, b) => ORDER[a.priority] - ORDER[b.priority]);
}
