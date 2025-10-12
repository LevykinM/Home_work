year = int(input("Введите год:"))

if 1000 <= year <= 9999:
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        print ("Високосный год")
    else:
        print ("Обычный год")
else:
    print("Ошибка! Введите четыёхзначное число")
