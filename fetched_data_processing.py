from terminaltables import AsciiTable


def print_asciitable(language_popularity, title):
    popularity_table = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]
    for language, values in language_popularity.items():
        popularity_table.append(
            [
                language, values["vacancies_found"],
                values["vacancies_processed"],
                values["average_salary"]
            ]
        )

    table_instance_sj = AsciiTable(popularity_table, title)
    print(table_instance_sj.table)


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        (salary_from+salary_to) / 2
    elif salary_from is None and salary_to is None:
        return None
    elif salary_from in (None, 0):
        return salary_to*0.8
    elif salary_to in (None, 0):
        return salary_from*1.2
