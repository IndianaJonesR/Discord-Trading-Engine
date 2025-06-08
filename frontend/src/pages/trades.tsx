import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { formatCurrency, formatPercentage } from '@/lib/utils'
import { Trade } from '@/types'

export function Trades() {
  const [trades, setTrades] = useState<Trade[]>([])

  // This would normally fetch from your API
  useEffect(() => {
    // Mock data for demonstration
    setTrades([
      {
        id: '1',
        symbol: 'SPY',
        strike: 420,
        option_type: 'Calls',
        expiration: '1/19',
        entry_price: 1.25,
        current_price: 1.35,
        quantity: 2,
        status: 'filled',
        created_at: '2024-01-15T10:30:00Z',
        stop_loss: 1.00,
        take_profit: 1.63
      },
      {
        id: '2',
        symbol: 'QQQ',
        strike: 350,
        option_type: 'Puts',
        expiration: '1/26',
        entry_price: 2.10,
        current_price: 2.05,
        quantity: 1,
        status: 'filled',
        created_at: '2024-01-14T14:20:00Z',
        stop_loss: 1.68,
        take_profit: 2.73
      },
      {
        id: '3',
        symbol: 'TSLA',
        strike: 180,
        option_type: 'Calls',
        expiration: '2/2',
        entry_price: 3.20,
        current_price: 3.68,
        quantity: 1,
        status: 'filled',
        created_at: '2024-01-13T09:15:00Z',
        stop_loss: 2.56,
        take_profit: 4.16
      }
    ])
  }, [])

  const getStatusColor = (status: Trade['status']) => {
    switch (status) {
      case 'filled':
        return 'bg-green-100 text-green-800'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'cancelled':
        return 'bg-red-100 text-red-800'
      case 'expired':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const calculatePnL = (trade: Trade) => {
    if (!trade.current_price) return 0
    return (trade.current_price - trade.entry_price) * trade.quantity * 100
  }

  const calculatePnLPercentage = (trade: Trade) => {
    if (!trade.current_price) return 0
    return ((trade.current_price - trade.entry_price) / trade.entry_price) * 100
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">My Trades</h1>
        <p className="text-muted-foreground">
          View and manage your options trades
        </p>
      </div>

      <div className="space-y-4">
        {trades.map((trade) => {
          const pnl = calculatePnL(trade)
          const pnlPercentage = calculatePnLPercentage(trade)
          const isPositive = pnl >= 0

          return (
            <Card key={trade.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">
                    {trade.symbol} {trade.strike}{trade.option_type === 'Calls' ? 'C' : 'P'} {trade.expiration}
                  </CardTitle>
                  <Badge className={getStatusColor(trade.status)}>
                    {trade.status.charAt(0).toUpperCase() + trade.status.slice(1)}
                  </Badge>
                </div>
                <CardDescription>
                  {trade.quantity} contract{trade.quantity > 1 ? 's' : ''} • Entered on {new Date(trade.created_at).toLocaleDateString()}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Entry Price</p>
                    <p className="font-medium">{formatCurrency(trade.entry_price)}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Current Price</p>
                    <p className="font-medium">{trade.current_price ? formatCurrency(trade.current_price) : 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">P&L</p>
                    <p className={`font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
                      {formatCurrency(pnl)} ({formatPercentage(pnlPercentage)})
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Total Value</p>
                    <p className="font-medium">
                      {trade.current_price ? formatCurrency(trade.current_price * trade.quantity * 100) : 'N/A'}
                    </p>
                  </div>
                </div>
                
                {(trade.stop_loss || trade.take_profit) && (
                  <div className="mt-4 pt-4 border-t">
                    <div className="grid grid-cols-2 gap-4">
                      {trade.stop_loss && (
                        <div>
                          <p className="text-sm text-muted-foreground">Stop Loss</p>
                          <p className="font-medium text-red-600">{formatCurrency(trade.stop_loss)}</p>
                        </div>
                      )}
                      {trade.take_profit && (
                        <div>
                          <p className="text-sm text-muted-foreground">Take Profit</p>
                          <p className="font-medium text-green-600">{formatCurrency(trade.take_profit)}</p>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )
        })}
      </div>

      {trades.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-muted-foreground">No trades found. Start by entering your first trade!</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
} 