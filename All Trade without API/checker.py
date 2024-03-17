import json
from collections import defaultdict
from prettytable import PrettyTable

with open('data.json') as f:
    data = json.load(f)

total_fee = 0
total_volume = 0
unique_trade_ids = set()
fee_by_symbol = defaultdict(float)
volume_by_symbol = defaultdict(lambda: {'volume': 0, 'fee': 0}) 


for transaction in data:
    fee = float(transaction['fee'])
    fee_symbol = transaction['feeSymbol']
    price = float(transaction['price'])
    quantity = float(transaction['quantity'])
    trade_id = transaction['tradeId']
    symbol = transaction['symbol']
    timestamp = transaction['timestamp']

    if fee_symbol != 'USDC':
        total_fee += fee * price
    else:
        total_fee += fee

    total_volume += quantity * price

    unique_trade_ids.add(trade_id)

    fee_by_symbol[fee_symbol] += fee

    volume_by_symbol[symbol]['volume'] += quantity * price
    volume_by_symbol[symbol]['fee'] += fee

table_stats = PrettyTable(["Type", "Quanity"])
table_stats.add_row(["Total Fee", "${:.2f}".format(total_fee)])
table_stats.add_row(["Total Volume", "${:.2f}".format(total_volume)])
table_stats.add_row(["Total Trades", len(unique_trade_ids)])
table_stats.hrules = 1
table_stats.align["Type"] = "l"
print(table_stats)

table_fee_symbol = PrettyTable()
table_fee_symbol.field_names = ["FeeSymbol", "Fee"]
for symbol, fee in fee_by_symbol.items():
    table_fee_symbol.add_row([symbol, "${:.2f}".format(fee)])
print(table_fee_symbol)

table_volume_symbol = PrettyTable()
table_volume_symbol.field_names = ["Symbol", "Volume", "Fee"]
for symbol, data in volume_by_symbol.items():
    table_volume_symbol.add_row([symbol, "${:.2f}".format(data['volume']), "${:.2f}".format(data['fee'])])
print(table_volume_symbol)