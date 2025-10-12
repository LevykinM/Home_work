Boys = []
Girls = []

while True:
    Boy_name = input("Введи мужское имя или End, если хочешь продолжить: ")
    if Boy_name.lower() == "end":
        break
    Boys.append(Boy_name)
    print("Мужские имена:" + str(Boys))

while True:
    Girl_name = input("Введи женское имя имя или End, если хочешь продолжить: ")
    if Girl_name.lower() == "end":
        break
    Girls.append(Girl_name)
    print("Женские имена:" + str(Girls))

Boys.sort()
Girls.sort()
count = len(Girls)

if len(Girls) == len(Boys):
    print("\nРезультат")
    print("Идеальные пары")
    for i in range(len(Boys)):
        print(Boys[i], "и", Girls[i])
else:
    print("\nРезультат")
    print("Внимание, кто-то может остаться без пары.")