export interface TradingConfig {
  position_size: {
    min_amount: number;
    max_amount: number;
  };
  stop_loss: {
    percentage: number;
  };
  take_profit: {
    percentage: number;
  };
  entry_price_adjustment: number;
}

export interface OptionData {
  option_class: string;
  symbol: string;
  strike: string;
  option_type: string;
  expiration: string;
  price: string;
  side: string;
  option_symbol: string;
}

export interface Trade {
  id: string;
  symbol: string;
  strike: number;
  option_type: 'Calls' | 'Puts';
  expiration: string;
  entry_price: number;
  current_price?: number;
  quantity: number;
  status: 'pending' | 'filled' | 'cancelled' | 'expired';
  created_at: string;
  stop_loss?: number;
  take_profit?: number;
}

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  message?: string;
} 