msc_price = 13_000
spb_price = 10_000
ekb_price = 8_000

dist = input("Введите пункт назначения (msc,spb,ekb): ")
adults = int(input("Введите количество взрослых: "))
kids = int(input("Введите количество детей: "))
if dist == "msc":
    dist_price = msc_price
elif dist == "spb":
    dist_price = spb_price
else:
    dist_price = ekb_price

total = dist_price * (2 * adults + kids) //2

#price = msc_price * (2 * adults + kids) //2

print("Цена поездки:", total)