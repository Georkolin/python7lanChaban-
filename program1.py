import csv
import random
from faker import Faker

# Ініціалізація Faker з українською локалізацією
fake = Faker(locale='uk_UA')

middle_names_male = [
    "Олександрович", "Іванович", "Петрович", "Миколайович", "Сергійович",
    "Андрійович", "Юрійович", "Дмитрович", "Васильович", "Віталійович",
    "Михайлович", "Володимирович", "Ігорович", "Богданович", "Анатолійович",
    "Романович", "Олегович", "Артемович", "Євгенович", "Максимович"
]

middle_names_female = [
    "Олександрівна", "Іванівна", "Петрівна", "Миколаївна", "Сергіївна",
    "Андріївна", "Юріївна", "Дмитрівна", "Василівна", "Віталіївна",
    "Михайлівна", "Володимирівна", "Ігорівна", "Богданівна", "Анатоліївна",
    "Романівна", "Олегівна", "Артемівна", "Євгенівна", "Максимівна"
]

def generate_employees(count=500):
    employees = []
    male_count = int(count * 0.6)
    female_count = count - male_count
    
    genders = ['Чоловік'] * male_count + ['Жінка'] * female_count
    random.shuffle(genders)

    for gender in genders:
        if gender == 'Чоловік':
            first_name = fake.first_name_male()
            last_name = fake.last_name_male()
            middle_name = random.choice(middle_names_male)
        else:
            first_name = fake.first_name_female()
            last_name = fake.last_name_female()
            middle_name = random.choice(middle_names_female)

        row = {
            "Прізвище": last_name,
            "Ім'я": first_name,
            "По батькові": middle_name,
            "Стать": gender,
            "Дата народження": fake.date_of_birth(minimum_age=15, maximum_age=80).strftime("%Y-%m-%d"),
            "Посада": fake.job(),
            "Місто проживання": fake.city(),
            "Адреса проживання": fake.address().replace("\n", ", "),
            "Телефон": fake.phone_number(),
            "Email": fake.email()
        }
        employees.append(row)
    return employees

# Запис у CSV
def save_to_csv(data, filename="employees.csv"):
    keys = data[0].keys()
    with open(filename, "w", encoding="utf-8", newline="") as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Файл {filename} успішно створено! Згенеровано {len(data)} записів.")

if __name__ == "__main__":
    data = generate_employees(500)
    save_to_csv(data)