`npm run typecheck` fails in src/service.ts.

Make it pass without changing the generated client, without type assertions or
casts, and without suppressing the compiler. The fix belongs on the consuming
side.
