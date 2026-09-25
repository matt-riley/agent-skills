import type { Ticket } from './types';

export function demote(ticket: Ticket): Ticket {
  return { ...ticket, priority: 'low' };
}
