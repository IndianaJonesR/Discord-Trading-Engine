import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import { Navigation } from '@/components/navigation'
import { Dashboard } from '@/pages/dashboard'
import { Settings } from '@/pages/settings'
import { TradeEntry } from '@/pages/trade-entry'
import { Trades } from '@/pages/trades'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/trade-entry" element={<TradeEntry />} />
            <Route path="/trades" element={<Trades />} />
          </Routes>
        </main>
        <Toaster />
      </div>
    </Router>
  )
}

export default App 