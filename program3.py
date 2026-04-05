import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def calculate_age(born_str):
    born = datetime.strptime(born_str, "%Y-%m-%d")
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def analyze_employees():
    csv_file = "employees.csv"

    if not os.path.exists(csv_file):
        print(f"Помилка: Файл {csv_file} не знайдено!")
        return
    
    try:
        df = pd.read_csv(csv_file)
        df['Вік'] = df['Дата народження'].apply(calculate_age)
        print("Ok")

        gender_counts = df['Стать'].value_counts()
        print("\nКількість співробітників за статтю:")
        print(gender_counts)

        bins = [0, 18, 45, 70, 150]
        labels = ['younger_18', '18-45', '45-70', 'older_70']
        df['Категорія'] = pd.cut(df['Вік'], bins=bins, labels=labels, right=False)
        
        category_counts = df['Категорія'].value_counts().reindex(labels)
        print("\nКількість за віковими категоріями:")
        print(category_counts)

        gender_by_category = pd.crosstab(df['Категорія'], df['Стать'])
        print("\nСтать у кожній віковій категорії:")
        print(gender_by_category)

        # ДІАГРАМB
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        # Діаграма 1: Стать
        gender_counts.plot(kind='pie', ax=axes[0], autopct='%1.1f%%', colors=['skyblue', 'pink'], title='Співвідношення статей')
        axes[0].set_ylabel('')

        # Діаграма 2: Вікові категорії
        category_counts.plot(kind='bar', ax=axes[1], color='lightgreen', title='Розподіл за віком')
        axes[1].set_xlabel('Категорія')
        axes[1].set_ylabel('Кількість')

        # Діаграма 3: Стать по категоріях
        gender_by_category.plot(kind='bar', stacked=False, ax=axes[2], title='Стать за категоріями')
        axes[2].set_xlabel('Категорія')
        axes[2].set_ylabel('Кількість')

        plt.tight_layout()
        print("\nЗакрийте вікно з діаграмами, щоб завершити програму.")
        plt.show()

    except Exception as e:
        print(f"Помилка при аналізі даних: {e}")

if __name__ == "__main__":
    analyze_employees()