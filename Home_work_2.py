number = int(input("Введите шестизначный номер билета: "))

num_str = str(number)
if len(num_str) == 6:
    sum_first = int(str(number)[0]) + int(str(number)[1]) + int(str(number)[2])
    sum_second = int(str(number)[3]) + int(str(number)[4]) + int(str(number)[5])

    if sum_first == sum_second:
        print("Счастливый билет")
    else:
        print("Несчастливый билет")
else:
    print ("Ошибка! Введите шестизначный номер билета")