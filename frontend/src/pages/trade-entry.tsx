import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { formatCurrency } from '@/lib/utils'
import { PlusCircle, Calculator } from 'lucide-react'

interface TradeForm {
  symbol: string
  strike: string
  option_type: 'Calls' | 'Puts'
  expiration: string
  price: string
}

export function TradeEntry() {
  const [form, setForm] = useState<TradeForm>({
    symbol: '',
    strike: '',
    option_type: 'Calls',
    expiration: '',
    price: ''
  })

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [calculation, setCalculation] = useState({
    quantity: 0,
    totalCost: 0,
    stopLoss: 0,
    takeProfit: 0
  })

  const handleInputChange = (field: keyof TradeForm, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }))
    calculateTrade({ ...form, [field]: value })
  }

  const calculateTrade = (tradeData: TradeForm) => {
    const price = parseFloat(tradeData.price) || 0
    const entryPrice = price * 1.05 // 5% above market price
    const quantity = Math.floor(110 / (entryPrice * 100)) || 0
    const totalCost = quantity * entryPrice * 100
    const stopLoss = entryPrice * 0.8 // 20% below entry
    const takeProfit = entryPrice * 1.3 // 30% above entry

    setCalculation({
      quantity,
      totalCost,
      stopLoss,
      takeProfit
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      // This would call your backend API to place the trade
      const response = await fetch('/api/trades', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })

      if (response.ok) {
        alert('Trade submitted successfully!')
        setForm({
          symbol: '',
          strike: '',
          option_type: 'Calls',
          expiration: '',
          price: ''
        })
        setCalculation({
          quantity: 0,
          totalCost: 0,
          stopLoss: 0,
          takeProfit: 0
        })
      } else {
        alert('Failed to submit trade')
      }
    } catch (error) {
      console.error('Error submitting trade:', error)
      alert('Error submitting trade')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Manual Trade Entry</h1>
        <p className="text-muted-foreground">
          Enter option trade details manually
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Trade Details</CardTitle>
            <CardDescription>
              Enter the option trade information
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="symbol">Symbol</Label>
                <Input
                  id="symbol"
                  placeholder="SPY"
                  value={form.symbol}
                  onChange={(e) => handleInputChange('symbol', e.target.value.toUpperCase())}
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="strike">Strike Price</Label>
                  <Input
                    id="strike"
                    type="number"
                    placeholder="420"
                    value={form.strike}
                    onChange={(e) => handleInputChange('strike', e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="option-type">Option Type</Label>
                  <Select value={form.option_type} onValueChange={(value) => handleInputChange('option_type', value)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Calls">Calls</SelectItem>
                      <SelectItem value="Puts">Puts</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="expiration">Expiration (MM/DD)</Label>
                <Input
                  id="expiration"
                  placeholder="3/15"
                  value={form.expiration}
                  onChange={(e) => handleInputChange('expiration', e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="price">Option Price</Label>
                <Input
                  id="price"
                  type="number"
                  step="0.01"
                  placeholder="1.25"
                  value={form.price}
                  onChange={(e) => handleInputChange('price', e.target.value)}
                  required
                />
              </div>

              <Button type="submit" className="w-full" disabled={isSubmitting}>
                <PlusCircle className="mr-2 h-4 w-4" />
                {isSubmitting ? 'Submitting...' : 'Submit Trade'}
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Trade Calculation</CardTitle>
            <CardDescription>
              Preview of your trade with current settings
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Quantity:</span>
              <span className="font-medium">{calculation.quantity} contracts</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Total Cost:</span>
              <span className="font-medium">{formatCurrency(calculation.totalCost)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Stop Loss:</span>
              <span className="font-medium text-red-600">{formatCurrency(calculation.stopLoss)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Take Profit:</span>
              <span className="font-medium text-green-600">{formatCurrency(calculation.takeProfit)}</span>
            </div>
            
            <div className="pt-4 border-t">
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Calculator className="h-4 w-4" />
                <span>Calculations based on current settings</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 