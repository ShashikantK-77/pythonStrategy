import csv

def save_backtest_results(strategy_id, symbol, strategy_data, date, ltp, short_term_sma=None, long_term_sma=None, rsi=None):
    fieldnames = ['strategy_id', 'symbol', 'order', 'date','exchange_segment','transaction_type', 'ltp', 'short_term_sma', 'long_term_sma', 'rsi']
    file_exists = 'backtest_results.csv'
    
    with open('backtest_results.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header
        writer.writerow({
            'strategy_id': strategy_id,
            'symbol': symbol,
            'order': strategy_data['actions'][0]['action_name'],
            'date': date,
            'exchange_segment': strategy_data['strategy']['exchange'],
            'transaction_type':strategy_data['actions'][0]['action_type'],
            'ltp': ltp,
            'short_term_sma': short_term_sma,
            'long_term_sma': long_term_sma,
            'rsi': rsi
        })
