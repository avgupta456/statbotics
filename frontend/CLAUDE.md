# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in the `frontend/` directory.

## Commands (run from `frontend/`)

```bash
yarn install       # Install dependencies
yarn dev           # Dev server at localhost:3000
yarn build         # Production build
yarn lint          # ESLint
yarn prettier      # Format with Prettier
```

Note: `yarn dev` sets `NODE_OPTIONS=--max_old_space_size=3072` to avoid OOM on large builds.

## Tech Stack

Next.js 13 (Pages Router), TypeScript, Tailwind CSS, DaisyUI, Nivo/Highcharts (charts), TanStack Table (v8).

## Structure

- **`src/pages/`** — Page routes. Key pages:
  - `teams/` — Team rankings table with filters
  - `team/[team]/` — Individual team page (EPA history, event results)
  - `events/` — Events list
  - `event/[event]/` — Individual event page (team standings, match results, simulation)
  - `matches/` — Match list
  - `match/[match]/` — Individual match page (breakdown, predictions)
  - `compare/` — Side-by-side team comparison
  - `blog/` and `docs/` — Markdown-rendered content pages

- **`src/components/`** — Shared components:
  - `Figures/` — Chart components (Line, Bar, Bubble, Scatter, YearLine, EventLine, TeamLine) built on Nivo/Highcharts
  - `Table/` — TanStack Table wrapper with sorting/filtering, `BreakdownTable`, `InsightsTable`
  - `MatchTable.tsx` — Match listing component
  - `filter.tsx`, `filterBar.tsx`, `filterConstants.tsx`, `multiSelect.tsx` — Filter UI

- **`src/api/`** — Data fetching:
  - `storage.tsx` — Core fetch function. Tries GCS bucket first, falls back to backend API. Uses IndexedDB (`idb-keyval`) to cache responses client-side with a TTL. Data is zlib-compressed; decompressed with `pako`.
  - `teams.tsx`, `events.tsx`, `matches.tsx`, `team.tsx`, `event.tsx`, `match.tsx` — Entity-specific fetch wrappers.
  - `header.tsx` — Fetches site-wide header data.

- **`src/layouts/`** — `siteLayout.tsx` (main nav/footer wrapper), `blogLayout.tsx`.

- **`src/constants.tsx`** — **Update this each season.** Contains:
  - `CURR_YEAR`, `CURR_WEEK`
  - `BACKEND_URL` and `BUCKET_URL` (GCS) — controlled by `PROD` env var
  - `RP_KEYS` / `RP_NAMES` — year-keyed ranking point names for the filter/display layer
  - `BREAKDOWN_YEARS` — years with full match breakdown support
  - Event name shortening maps and division-to-parent-event mappings

## Data Flow

Pages fetch data via `src/api/` functions, which:
1. Check IndexedDB for a non-expired cached response
2. Try fetching the compressed blob from GCS (`BUCKET_URL`)
3. Fall back to the live backend site API (`BACKEND_URL`)

All responses are JSON compressed with zlib (pako-compatible). The frontend decompresses in the browser.

## Environment

- **Dev**: `PROD` is unset; `BACKEND_URL` points to `http://127.0.0.1:8000/v3/site` and `BUCKET_URL` to the dev GCS bucket.
- **Prod**: Set `PROD=True`; deployed on Vercel, auto-deploys on push to `master`.

Note: uses `127.0.0.1` instead of `localhost` in dev due to a Node.js `undici` bug.

## Season Prep

1. Update `CURR_YEAR` and `CURR_WEEK` in `src/constants.tsx`
2. Add the new year to `RP_KEYS` and `RP_NAMES` in `src/constants.tsx`
3. Add the new year to `BREAKDOWN_YEARS` once breakdown parsing is implemented in the backend
4. Add a year-specific case to `getRandomTiebreaker()` in `src/pagesContent/event/[event_id]/worker.ts` — set a cold-start range based on preseason match data (e.g. `BASE + Math.round(Math.random() * RANGE)`). The tiebreaker value is year-specific; check `clean_breakdown_{year}()` in `backend/src/tba/breakdown.py` to confirm what it represents.
