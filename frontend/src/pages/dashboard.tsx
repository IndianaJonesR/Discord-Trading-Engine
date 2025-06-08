import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { formatCurrency, formatPercentage } from '@/lib/utils'
import { TrendingUp, TrendingDown, DollarSign, Activity } from 'lucide-react'

interface DashboardStats {
  totalValue: number
  totalGainLoss: number
  totalGainLossPercentage: number
  activeTrades: number
}

export function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalValue: 0,
    totalGainLoss: 0,
    totalGainLossPercentage: 0,
    activeTrades: 0,
  })

  // This would normally fetch from your API
  useEffect(() => {
    // Mock data for demonstration
    setStats({
      totalValue: 12500,
      totalGainLoss: 850,
      totalGainLossPercentage: 7.3,
      activeTrades: 5,
    })
  }, [])

  const isPositive = stats.totalGainLoss >= 0

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Overview of your options trading performance
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Portfolio Value</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(stats.totalValue)}</div>
            <p className="text-xs text-muted-foreground">
              +2.1% from last month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total P&L</CardTitle>
            {isPositive ? (
              <TrendingUp className="h-4 w-4 text-green-600" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-600" />
            )}
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {formatCurrency(stats.totalGainLoss)}
            </div>
            <p className="text-xs text-muted-foreground">
              {formatPercentage(stats.totalGainLossPercentage)} return
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Trades</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activeTrades}</div>
            <p className="text-xs text-muted-foreground">
              Currently open positions
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Win Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">68%</div>
            <p className="text-xs text-muted-foreground">
              Last 30 trades
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Recent Performance</CardTitle>
            <CardDescription>
              Your trading performance over the last 30 days
            </CardDescription>
          </CardHeader>
          <CardContent className="pl-2">
            <div className="h-[200px] w-full bg-muted/20 rounded flex items-center justify-center">
              <p className="text-muted-foreground">Performance chart would go here</p>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Recent Trades</CardTitle>
            <CardDescription>
              Your latest options trades
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center">
                <div className="ml-4 space-y-1">
                  <p className="text-sm font-medium leading-none">SPY 420C 1/19</p>
                  <p className="text-sm text-muted-foreground">+$125.00</p>
                </div>
                <div className="ml-auto font-medium">+8.3%</div>
              </div>
              <div className="flex items-center">
                <div className="ml-4 space-y-1">
                  <p className="text-sm font-medium leading-none">QQQ 350P 1/26</p>
                  <p className="text-sm text-muted-foreground">-$45.00</p>
                </div>
                <div className="ml-auto font-medium">-2.1%</div>
              </div>
              <div className="flex items-center">
                <div className="ml-4 space-y-1">
                  <p className="text-sm font-medium leading-none">TSLA 180C 2/2</p>
                  <p className="text-sm text-muted-foreground">+$320.00</p>
                </div>
                <div className="ml-auto font-medium">+15.2%</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
} 