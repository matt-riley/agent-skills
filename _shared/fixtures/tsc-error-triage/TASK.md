`npm run typecheck` fails with several errors.

Find the single root cause and fix it. Do not silence the compiler with
@ts-nocheck, @ts-ignore, or `as any` casts, and keep the Priority type a union.
