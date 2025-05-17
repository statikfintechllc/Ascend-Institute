def estimate_tax(position):
    total_value = position["price"] * position["shares"]
    tax_rate = 0.15
    return round(total_value * tax_rate, 2)

