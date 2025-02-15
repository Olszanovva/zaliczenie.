import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "dane.json"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    dni = data["data"]["dni"]
    temperatura = data["data"]["temperatura"]
    title = data["title"]
    x_label = data["x_label"]
    y_label = data["y_label"]
    
except FileNotFoundError:
    print(f"Plik {file_path} nie istnieje. Upewnij się, że znajduje się w katalogu projektu.")
    exit()

print("Wybierz rodzaj wykresu:")
print("1 - Liniowy")
print("2 - Słupkowy")
print("3 - Punktowy")
wybor = input("Podaj numer (1/2/3): ")

plt.figure(figsize=(8, 5))

if wybor == "1":
    sns.lineplot(x=dni, y=temperatura, marker="o")
elif wybor == "2":
    plt.bar(dni, temperatura)
elif wybor == "3":
    plt.scatter(dni, temperatura)
else:
    print("Niepoprawny wybór, domyślnie wykres liniowy.")
    sns.lineplot(x=dni, y=temperatura, marker="o")

plt.title(title)
plt.xlabel(x_label)
plt.ylabel(y_label)

print("Czy chcesz edytować dane? (tak/nie)")
odpowiedz = input().lower()
if odpowiedz == "tak":
    index = int(input("Podaj numer dnia do zmiany: "))
    nowa_temp = float(input("Podaj nową wartość temperatury: "))
    temperatura[index - 1] = nowa_temp  
    plt.clf()
    sns.lineplot(x=dni, y=temperatura, marker="o")
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

plt.show()
