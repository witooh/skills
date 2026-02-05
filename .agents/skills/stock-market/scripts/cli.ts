#!/usr/bin/env bun
/**
 * Stock Market CLI - Fetch real-time stock and ETF prices
 * 
 * Tools:
 * - get_price: Get current price for a symbol
 * - get_multiple_prices: Get prices for multiple symbols
 * - search_symbol: Search for stock symbols by name
 * - get_market_summary: Get major indices summary
 * - get_historical: Get historical price data
 */

import { getPrice, getMultiplePrices, searchSymbol, getMarketSummary, getHistorical } from './tools/stock.js';

const TOOLS: Record<string, Function> = {
  get_price: getPrice,
  get_multiple_prices: getMultiplePrices,
  search_symbol: searchSymbol,
  get_market_summary: getMarketSummary,
  get_historical: getHistorical,
};

function showHelp() {
  console.log(`
Stock Market CLI - Real-time stock and ETF prices

Usage: bunx stock-market <tool> '<json-params>'

Tools:
  get_price              Get current price for a symbol
  get_multiple_prices    Get prices for multiple symbols
  search_symbol          Search for stock symbols by name
  get_market_summary     Get major market indices summary
  get_historical         Get historical price data

Examples:
  bunx stock-market get_price '{"symbol": "AAPL"}'
  bunx stock-market get_price '{"symbol": "PTT.BK"}'
  bunx stock-market get_multiple_prices '{"symbols": ["AAPL", "MSFT", "GOOGL"]}'
  bunx stock-market search_symbol '{"query": "Apple"}'
  bunx stock-market get_market_summary
  bunx stock-market get_historical '{"symbol": "AAPL", "period": "1mo"}'
`);
}

function showTools() {
  console.log(JSON.stringify(Object.keys(TOOLS), null, 2));
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    showHelp();
    process.exit(0);
  }
  
  if (args[0] === '--list') {
    showTools();
    process.exit(0);
  }
  
  const toolName = args[0];
  const tool = TOOLS[toolName];
  
  if (!tool) {
    console.error(`Error: Unknown tool "${toolName}"`);
    console.error(`Available tools: ${Object.keys(TOOLS).join(', ')}`);
    process.exit(1);
  }
  
  let params = {};
  if (args[1]) {
    try {
      params = JSON.parse(args[1]);
    } catch (e) {
      console.error('Error: Invalid JSON parameters');
      console.error(e);
      process.exit(1);
    }
  }
  
  try {
    const result = await tool(params);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error instanceof Error ? error.message : String(error),
      timestamp: new Date().toISOString()
    }, null, 2));
    process.exit(1);
  }
}

main();
