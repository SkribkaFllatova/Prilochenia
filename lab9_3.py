def calculate_shipping(country, weight):
    rates = {
        "USA": (10, 20),
        "Canada": (15, 25),
        "Other": (30, 50)
    }
    rate = rates.get(country, rates["Other"])
    return rate[0] if weight < 5 else rate[1]
