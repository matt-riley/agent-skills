import { getUser } from './generated/api-client';

export function displayName(id: string): string {
  const user = getUser(id);
  return user.name;
}
