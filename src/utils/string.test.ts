import { describe, it, expect } from 'vitest';
import { getInitials } from './string';

describe('getInitials', () => {
  it('converts a full name to initials', () => {
    expect(getInitials('Camila Cuidado Santos')).toBe('CCS');
  });

  it('handles extra spaces between names', () => {
    expect(getInitials('  John   Doe ')).toBe('JD');
  });
});
