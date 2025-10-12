Boys = []
Girls = []

while True:
    Boy_name = input("Введи мужское имя или End, если хочешь продолжить: ")
    if Boy_name == "end":
        break
    Boys.append(Boy_name)
    print("Мужские имена:" + str(Boys))

while True:
    Girl_name = input("Введи женское имя имя или End, если хочешь продолжить: ")
    if Girl_name == "end":
        break
    Girls.append(Girl_name)
    print("Женские имена:" + str(Girls))

Boys.sort()
Girls.sort()

print("Мужские имена:" + str(Boys))
print("Женские имена:" + str(Girls))