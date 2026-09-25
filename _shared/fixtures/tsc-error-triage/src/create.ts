import type { Ticket } from './types';

export function openTicket(id: string): Ticket {
  return { id, priority: 'high' };
}
