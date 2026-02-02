import sys
from oil_price_celenium import get_oil_price

if __name__ == "__main__":
    date = sys.argv[1]   # YYYY-mm-dd
    y, m, d = date.split("-")

    price = get_oil_price(y, m, d)
    print(price)