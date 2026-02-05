/**
 * Stock Market Tools - Yahoo Finance API Client
 */

interface PriceResult {
  success: boolean;
  data?: {
    symbol: string;
    name: string;
    price: number;
    currency: string;
    change: number;
    change_percent: number;
    market_time: string;
    volume: number;
    market_cap?: string;
    day_high?: number;
    day_low?: number;
    year_high?: number;
    year_low?: number;
  };
  error?: string;
  timestamp: string;
}

interface SearchResult {
  success: boolean;
  data?: Array<{
    symbol: string;
    name: string;
    exchange: string;
    type: string;
  }>;
  error?: string;
  timestamp: string;
}

interface HistoricalResult {
  success: boolean;
  data?: Array<{
    date: string;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
  }>;
  error?: string;
  timestamp: string;
}

function formatMarketCap(value: number): string {
  if (value >= 1e12) return `${(value / 1e12).toFixed(2)}T`;
  if (value >= 1e9) return `${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
  return value.toString();
}

function formatNumber(num: number): number {
  return Math.round(num * 100) / 100;
}

// Common Thai SET stock symbols that require .BK suffix
const THAI_STOCK_SYMBOLS = new Set([
  'PTT', 'AOT', 'SCB', 'KBANK', 'CPALL', 'BDMS', 'ADVANC', 'TRUE', 'INTUCH',
  'BBL', 'KTB', 'PTTEP', 'TOP', 'SPRC', 'ESSO', 'IRPC', 'GPSC', 'GULF',
  'EA', 'BANPU', 'MINT', 'CENTEL', 'CPN', 'LH', 'SIRI', 'SPALI', 'PSH',
  'OR', 'COM7', 'GLOBAL', 'HANA', 'DELTA', 'KTC', 'MIDA', 'NER', 'OSP',
  'SCC', 'CPF', 'TU', 'GFPT', 'AAV', 'BA', 'NOK', 'AICC', 'THAI'
]);

/**
 * Detect if symbol is a known Thai stock without .BK suffix
 */
function isThaiStockWithoutSuffix(symbol: string): boolean {
  const upperSymbol = symbol.toUpperCase();
  // Only check explicit list of known Thai stocks
  // Don't use pattern matching to avoid false positives with US stocks
  return THAI_STOCK_SYMBOLS.has(upperSymbol);
}

/**
 * Get current price and key metrics for a symbol
 */
export async function getPrice(params: { symbol: string }): Promise<PriceResult> {
  let { symbol } = params;
  
  // Auto-append .BK for Thai stocks without suffix
  const originalSymbol = symbol;
  if (isThaiStockWithoutSuffix(symbol)) {
    symbol = `${symbol.toUpperCase()}.BK`;
  }
  
  try {
    // Use Yahoo Finance unofficial API
    const response = await fetch(`https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?interval=1d&range=1d`, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch data for ${symbol}: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.chart || !data.chart.result || data.chart.result.length === 0) {
      throw new Error(`Symbol not found: ${symbol}`);
    }
    
    const result = data.chart.result[0];
    const meta = result.meta;
    const quote = result.indicators?.quote?.[0];
    
    // Get the latest price
    const currentPrice = meta.regularMarketPrice || meta.previousClose;
    const previousClose = meta.previousClose || meta.chartPreviousClose;
    const change = currentPrice - previousClose;
    const changePercent = (change / previousClose) * 100;
    
    const wasAutoCorrected = originalSymbol.toUpperCase() !== symbol.toUpperCase();
    
    return {
      success: true,
      data: {
        symbol: symbol.toUpperCase(),
        name: meta.shortName || meta.longName || symbol,
        price: formatNumber(currentPrice),
        currency: meta.currency || 'USD',
        change: formatNumber(change),
        change_percent: formatNumber(changePercent),
        market_time: new Date(meta.regularMarketTime * 1000).toISOString(),
        volume: meta.regularMarketVolume || 0,
        market_cap: meta.marketCap ? formatMarketCap(meta.marketCap) : undefined,
        day_high: meta.regularMarketDayHigh ? formatNumber(meta.regularMarketDayHigh) : undefined,
        day_low: meta.regularMarketDayLow ? formatNumber(meta.regularMarketDayLow) : undefined,
        year_high: meta.fiftyTwoWeekHigh ? formatNumber(meta.fiftyTwoWeekHigh) : undefined,
        year_low: meta.fiftyTwoWeekLow ? formatNumber(meta.fiftyTwoWeekLow) : undefined,
      },
      ...(wasAutoCorrected && {
        warning: `Symbol "${originalSymbol}" was auto-corrected to "${symbol}" for Thai SET market. Use .BK suffix explicitly for best results.`,
        original_symbol: originalSymbol
      }),
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Get prices for multiple symbols
 */
export async function getMultiplePrices(params: { symbols: string[] }): Promise<any> {
  const { symbols } = params;
  
  if (!Array.isArray(symbols) || symbols.length === 0) {
    return {
      success: false,
      error: 'symbols must be a non-empty array',
      timestamp: new Date().toISOString()
    };
  }
  
  try {
    const results = await Promise.all(
      symbols.map(async (symbol) => {
        const result = await getPrice({ symbol });
        return {
          symbol,
          ...(result.success ? result.data : { error: result.error })
        };
      })
    );
    
    return {
      success: true,
      data: results,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Search for stock/ETF symbols by company name
 */
export async function searchSymbol(params: { query: string }): Promise<SearchResult> {
  const { query } = params;
  
  try {
    // Use Yahoo Finance search API
    const response = await fetch(`https://query1.finance.yahoo.com/v1/finance/search?q=${encodeURIComponent(query)}&quotesCount=10&newsCount=0`, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Search failed: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.quotes || data.quotes.length === 0) {
      return {
        success: true,
        data: [],
        timestamp: new Date().toISOString()
      };
    }
    
    const results = data.quotes.map((quote: any) => ({
      symbol: quote.symbol,
      name: quote.shortname || quote.longname || quote.name || quote.symbol,
      exchange: quote.exchange || 'N/A',
      type: quote.quoteType || 'EQUITY'
    }));
    
    return {
      success: true,
      data: results,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Get major market indices summary
 */
export async function getMarketSummary(): Promise<any> {
  const indices = [
    '^GSPC',  // S&P 500
    '^IXIC',  // NASDAQ
    '^DJI',   // Dow Jones
    '^SET.BK', // Thai SET
    '^N225',  // Nikkei
    '^FTSE',  // FTSE 100
  ];
  
  try {
    const results = await Promise.all(
      indices.map(async (symbol) => {
        const result = await getPrice({ symbol });
        return {
          symbol,
          name: getIndexName(symbol),
          ...(result.success ? result.data : { error: result.error })
        };
      })
    );
    
    return {
      success: true,
      data: results,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      timestamp: new Date().toISOString()
    };
  }
}

function getIndexName(symbol: string): string {
  const names: Record<string, string> = {
    '^GSPC': 'S&P 500',
    '^IXIC': 'NASDAQ',
    '^DJI': 'Dow Jones',
    '^SET.BK': 'SET Index',
    '^N225': 'Nikkei 225',
    '^FTSE': 'FTSE 100',
  };
  return names[symbol] || symbol;
}

/**
 * Get historical price data
 */
export async function getHistorical(params: { 
  symbol: string; 
  period?: string;  // 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
  interval?: string; // 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
}): Promise<HistoricalResult> {
  const { symbol, period = '1mo', interval = '1d' } = params;
  
  try {
    const response = await fetch(
      `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?interval=${interval}&range=${period}`,
      {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
      }
    );
    
    if (!response.ok) {
      throw new Error(`Failed to fetch historical data: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.chart || !data.chart.result || data.chart.result.length === 0) {
      throw new Error(`No historical data found for ${symbol}`);
    }
    
    const result = data.chart.result[0];
    const timestamps = result.timestamp || [];
    const quote = result.indicators?.quote?.[0] || {};
    
    const prices = timestamps.map((ts: number, i: number) => ({
      date: new Date(ts * 1000).toISOString().split('T')[0],
      open: formatNumber(quote.open?.[i] || 0),
      high: formatNumber(quote.high?.[i] || 0),
      low: formatNumber(quote.low?.[i] || 0),
      close: formatNumber(quote.close?.[i] || 0),
      volume: quote.volume?.[i] || 0
    }));
    
    return {
      success: true,
      data: prices,
      timestamp: new Date().toISOString()
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : String(error),
      timestamp: new Date().toISOString()
    };
  }
}
