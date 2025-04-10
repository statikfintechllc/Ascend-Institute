import json

def phantom_buy_trigger(order):
    log = {
        "symbol": order["symbol"],
        "price": order["price"],
        "amount": order["amount"],
        "datetime": order["datetime"],
        "ghost_tag": True
    }
    with open("phantom_buy_trigger.log", "a") as f:
        f.write(json.dumps(log) + "\n")