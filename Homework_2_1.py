word = input("Введите слово: ")
if len(word) % 2 != 0:
    letter = word[len(word)//2]
    print(letter)
else:
    letter = word[len(word)//2-1]+word[len(word)//2]
    print(letter)
