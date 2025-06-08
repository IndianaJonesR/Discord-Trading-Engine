# Options Trading Bot - React Frontend

A modern React frontend for the Options Trading Bot, built with TypeScript, Tailwind CSS, and shadcn/ui components.

## Features

- **Dashboard**: Overview of trading performance with key metrics
- **Settings**: Configure trading parameters (position sizing, stop loss, take profit)
- **Trade Entry**: Manual trade entry form with real-time calculations
- **Trade History**: View and manage all your options trades
- **Modern UI**: Built with shadcn/ui components and Tailwind CSS
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **shadcn/ui** for UI components
- **React Router** for navigation
- **Lucide React** for icons

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

### Backend Integration

The frontend is configured to proxy API requests to `http://localhost:5000` where your Python Flask backend should be running.

Make sure your Python backend is running:
```bash
# In the root directory
python web_interface.py
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/           # shadcn/ui components
│   │   └── navigation.tsx
│   ├── pages/
│   │   ├── dashboard.tsx
│   │   ├── settings.tsx
│   │   ├── trade-entry.tsx
│   │   └── trades.tsx
│   ├── lib/
│   │   └── utils.ts      # Utility functions
│   ├── types/
│   │   └── index.ts      # TypeScript types
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── public/
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## API Integration

The frontend expects the following API endpoints from your Python backend:

- `GET /api/config` - Get trading configuration
- `POST /api/position` - Update position sizing
- `POST /api/stop-loss` - Update stop loss settings
- `POST /api/take-profit` - Update take profit settings
- `POST /api/entry-adjustment` - Update entry price adjustment
- `POST /api/reset` - Reset configuration to defaults
- `POST /api/trades` - Submit new trade (to be implemented)

## Customization with v0

This frontend is designed to work seamlessly with v0.dev for UI customization:

1. Copy any component code from the `src/components` or `src/pages` directories
2. Paste it into v0.dev
3. Describe your desired changes
4. Copy the improved code back to your project

The components follow shadcn/ui patterns, making them highly compatible with v0's design system.

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set the build command to `npm run build`
4. Set the output directory to `dist`
5. Add environment variables if needed

## Environment Variables

Create a `.env` file in the frontend directory for any environment-specific configuration:

```env
VITE_API_URL=http://localhost:5000
```

## Contributing

1. Follow the existing code style
2. Use TypeScript for type safety
3. Follow shadcn/ui component patterns
4. Test your changes thoroughly

## License

This project is part of the Options Trading Bot system. 