# Statbotics Frontend

The Statbotics frontend is a NextJS 13 (Beta, experimental `app/`) project that displays EPA data and allows users to explore and compare teams, events, and matches. The tech stack also includes TypeScript, Tailwind CSS, Nivo, and React Table. The frontend is deployed on Vercel.

## Setup

Requires Node 18+.

1. Install dependencies: `yarn install`
2. Run the development server: `yarn dev`
3. Open the app at `localhost:3000`
4. Build the app: `yarn build`
5. Run the production server: `yarn start`

## Deployment

The frontend is deployed on Vercel. Vercel automatically deploys the frontend upon pushing to the `master` branch.

## Structure

The frontend is structured as follows:

- `app/`: The NextJS app pages.
  - `(docs)`: The documentation pages, including the blog and API docs.
  - `(site)`: The main pages, including the team, event, and match pages.
- `assets/`: Static assets (not used in production).
- `components/`: React components including Figures, Tables, Filters, and more.
- `docs/`: Informal documentation for the frontend (not used in production).
- `public/`: Static assets used in production.

## Contributing

Contributions are welcome! Please open an issue or pull request.
