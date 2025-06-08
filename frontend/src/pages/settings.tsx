import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { TradingConfig } from '@/types'
import { formatCurrency, formatPercentage } from '@/lib/utils'
import { Save, RotateCcw } from 'lucide-react'

export function Settings() {
  const [config, setConfig] = useState<TradingConfig>({
    position_size: {
      min_amount: 100,
      max_amount: 120
    },
    stop_loss: {
      percentage: 20
    },
    take_profit: {
      percentage: 30
    },
    entry_price_adjustment: 1.05
  })

  const [isLoading, setIsLoading] = useState(false)

  // Load configuration from API
  useEffect(() => {
    const loadConfig = async () => {
      try {
        const response = await fetch('/api/config')
        if (response.ok) {
          const data = await response.json()
          setConfig(data)
        }
      } catch (error) {
        console.error('Failed to load config:', error)
      }
    }
    loadConfig()
  }, [])

  // Save configuration to API
  const handleSave = async () => {
    setIsLoading(true)
    try {
      // Save position size
      await fetch('/api/position', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config.position_size)
      })

      // Save stop loss
      await fetch('/api/stop-loss', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config.stop_loss)
      })

      // Save take profit
      await fetch('/api/take-profit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config.take_profit)
      })

      // Save entry adjustment
      const adjustmentPercentage = (config.entry_price_adjustment - 1) * 100
      await fetch('/api/entry-adjustment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ percentage: adjustmentPercentage })
      })

      alert('Settings saved successfully!')
    } catch (error) {
      console.error('Failed to save config:', error)
      alert('Failed to save settings')
    } finally {
      setIsLoading(false)
    }
  }

  // Reset to defaults
  const handleReset = async () => {
    setIsLoading(true)
    try {
      await fetch('/api/reset', { method: 'POST' })
      // Reload the page to get fresh defaults
      window.location.reload()
    } catch (error) {
      console.error('Failed to reset config:', error)
      alert('Failed to reset settings')
    } finally {
      setIsLoading(false)
    }
  }

  const updateConfig = (section: keyof TradingConfig, field: string, value: number) => {
    setConfig(prev => ({
      ...prev,
      [section]: typeof prev[section] === 'object' && prev[section] !== null
        ? { ...prev[section], [field]: value }
        : value
    }))
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Configure your trading parameters and risk management
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Position Sizing</CardTitle>
            <CardDescription>
              Set your minimum and maximum position sizes
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="min-amount">Minimum Amount</Label>
              <Input
                id="min-amount"
                type="number"
                value={config.position_size.min_amount}
                onChange={(e) => updateConfig('position_size', 'min_amount', parseFloat(e.target.value) || 0)}
              />
              <p className="text-sm text-muted-foreground">
                Current: {formatCurrency(config.position_size.min_amount)}
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="max-amount">Maximum Amount</Label>
              <Input
                id="max-amount"
                type="number"
                value={config.position_size.max_amount}
                onChange={(e) => updateConfig('position_size', 'max_amount', parseFloat(e.target.value) || 0)}
              />
              <p className="text-sm text-muted-foreground">
                Current: {formatCurrency(config.position_size.max_amount)}
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Risk Management</CardTitle>
            <CardDescription>
              Configure stop loss and take profit percentages
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="stop-loss">Stop Loss Percentage</Label>
              <Input
                id="stop-loss"
                type="number"
                value={config.stop_loss.percentage}
                onChange={(e) => updateConfig('stop_loss', 'percentage', parseFloat(e.target.value) || 0)}
              />
              <p className="text-sm text-muted-foreground">
                Current: {formatPercentage(config.stop_loss.percentage)} below entry
              </p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="take-profit">Take Profit Percentage</Label>
              <Input
                id="take-profit"
                type="number"
                value={config.take_profit.percentage}
                onChange={(e) => updateConfig('take_profit', 'percentage', parseFloat(e.target.value) || 0)}
              />
              <p className="text-sm text-muted-foreground">
                Current: {formatPercentage(config.take_profit.percentage)} above entry
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Entry Price Adjustment</CardTitle>
            <CardDescription>
              Adjust entry price above market price
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="entry-adjustment">Entry Price Multiplier</Label>
              <Input
                id="entry-adjustment"
                type="number"
                step="0.01"
                value={config.entry_price_adjustment}
                onChange={(e) => updateConfig('entry_price_adjustment', '', parseFloat(e.target.value) || 1)}
              />
              <p className="text-sm text-muted-foreground">
                Current: {formatPercentage((config.entry_price_adjustment - 1) * 100)} above market
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Actions</CardTitle>
            <CardDescription>
              Save your settings or reset to defaults
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex space-x-2">
              <Button onClick={handleSave} disabled={isLoading}>
                <Save className="mr-2 h-4 w-4" />
                Save Settings
              </Button>
              <Button variant="outline" onClick={handleReset} disabled={isLoading}>
                <RotateCcw className="mr-2 h-4 w-4" />
                Reset to Defaults
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 