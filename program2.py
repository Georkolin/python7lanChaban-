import pandas as pd
from datetime import datetime
import os

def calculate_age(born_str):
    # Перетворюємо рядок дати у об'єкт datetime
    born = datetime.strptime(born_str, "%Y-%m-%d")
    today = datetime.today()
    # Рахуємо повних років
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def process_employees():
    csv_file = "employees.csv"
    xlsx_file = "employees.xlsx"

    if not os.path.exists(csv_file):
        print(f"Помилка: Файл {csv_file} не знайдено!")
        return

    try:
        df = pd.read_csv(csv_file)
        df['Вік'] = df['Дата народження'].apply(calculate_age)

        # Створюємо Excel writer
        with pd.ExcelWriter(xlsx_file, engine='openpyxl') as writer:
            
            # Аркуш "all": всі дані (без колонки Вік, як у вихідному файлі, або з нею - зазвичай копіюють все)
            df.drop(columns=['Вік']).to_excel(writer, sheet_name='all', index=False)
            columns_to_show = ["Прізвище", "Ім'я", "По батькові", "Дата народження", "Вік"]

            categories = {
                "younger_18": df[df['Вік'] < 18],
                "18-45": df[(df['Вік'] >= 18) & (df['Вік'] <= 45)],
                "45-70": df[(df['Вік'] > 45) & (df['Вік'] <= 70)],
                "older_70": df[df['Вік'] > 70]
            }

            for sheet, filtered_df in categories.items():
                output_df = filtered_df[columns_to_show].copy()
                output_df.insert(0, '№', range(1, len(output_df) + 1))
                
                output_df.to_excel(writer, sheet_name=sheet, index=False)

        print("Ok")

    except PermissionError:
        print(f"Помилка: Неможливо створити або записати у {xlsx_file}. Можливо, він відкритий в іншій програмі?")
    except Exception as e:
        print(f"Помилка при обробці файлу: {e}")

if __name__ == "__main__":
    process_employees()