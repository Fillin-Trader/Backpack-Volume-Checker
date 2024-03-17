import json
from colorama import Fore, Back, Style

def process_fill_history(fill_history_data):
    total_fee = 0
    total_volume = 0 
    unique_trade_ids = set()
    
    for item in fill_history_data:
        fee = float(item.get('fee', 0))
        fee_symbol = item.get('feeSymbol', '')
        price = float(item.get('price', 0))
        quantity = float(item.get('quantity', 0))
        trade_id = item.get('tradeId', '')

        if fee_symbol == 'USDC':
            total_fee += fee
        else:
            total_fee += fee * price
        
        total_volume += quantity * price
        unique_trade_ids.add(trade_id)
    
    total_trades = len(unique_trade_ids)

    print(Back.WHITE + Fore.BLACK + "🟩 Trading History 🟩" + Style.RESET_ALL)
    print('_____________________________')
    print(f"📍 Total Fee: ${total_fee:.2f}")
    print(f"📍 Total Volume: ${total_volume:.2f}")
    print(f"📍 Total Trades: {total_trades}")
    print()

    levels = {
        'Sybil Tier': 10000,
        'Anti-Sybil Tier': 15000,
        'Street King Tier': 25000,
        'Degen Tier': 50000,
        'ETH Maxi Tier': 100000,
        '1% Tier': 250000,
        'Punk Holders Tier': 2500000,
        'Vilatik Tier': 10000000
    }
    print(Back.GREEN + Fore.BLACK + "🟩 Tier Level 🟩" + Style.RESET_ALL)
    print('_____________________________')
    for level, volume in levels.items():
        remaining = volume - total_volume
        print(f"🟩 Remaining {level}: ${remaining:.2f}")

def process_balance(balance_data):
    usdc_balance = balance_data.get('USDC', {})
    available_amount = float(usdc_balance.get('available', 0))
    return available_amount

def display_balance(balance_data):
    usdc_balance = balance_data.get('USDC', {})
    available_amount = float(usdc_balance.get('available', 0))
    colored_text = Back.BLACK + Fore.GREEN + f"✅ Balance: {available_amount:.2f} $USDC" + Style.RESET_ALL
    return colored_text

def process_deposit_address(deposit_address_data):
    total_quantity = 0
    
    for item in deposit_address_data:
        total_quantity += float(item.get('quantity', 0))
    
    return total_quantity

def calculate_total_quantity_minus_balance(total_quantity, available_amount):
    if total_quantity is None or available_amount is None:
        return None
    else:
        total_quantity_minus_balance = total_quantity - available_amount
        return total_quantity_minus_balance

with open("data.json", "r") as f:
    data = json.load(f)
    
    process_fill_history(data["fill_history_data"])
    print()
    print(Back.CYAN + Fore.BLACK + "🟩 Additional Info 🟩" + Style.RESET_ALL)
    print('_____________________________')
    print(display_balance(data["balance_data"]))
    process_deposit_address(data["deposit_address_data"])

    total_quantity = process_deposit_address(data["deposit_address_data"])
    available_amount = process_balance(data["balance_data"])
    total_quantity_minus_balance = calculate_total_quantity_minus_balance(total_quantity, available_amount)
    if total_quantity_minus_balance is not None:
        print(Fore.RED + f"🟥 Lose Amount: ${total_quantity_minus_balance:.2f}" + Style.RESET_ALL)
    else:
        print("Ошибка: Невозможно вычислить PnL")
