import os
from dotenv import load_dotenv
from fetch_headhunter import fetch_hh_vacancies_amount, predict_rub_salary_hh, fetch_hh_area_id
from fetch_superjob import predict_rub_salary_sj, fetch_sj_vacancies_amount
from fetched_data_processing import print_asciitable


def main():
    load_dotenv()
    superjob_secret_key = os.getenv("SUPERJOB_SECRET_KEY")

    programming_languages = [
        "Python",
        "Java",
        "JavaScript",
        "Ruby",
        "PHP",
        "C++",
        "C#",
        "GO"
    ]

    town = "Москва"
    hh_language_popularity = {}
    sj_language_popularity = {}

    hh_area_id = fetch_hh_area_id(town)

    for language in programming_languages:

        average_hh_salaries = predict_rub_salary_hh( # кол-во страниц
            f"Программист {language}",
            hh_area_id
        )
        average_sj_salaries = predict_rub_salary_sj(
            superjob_secret_key,
            f"Программист {language}",
            town
        )

        hh_vacancies_processed = len(average_hh_salaries)
        sj_vacancies_processed = len(average_sj_salaries)

        if hh_vacancies_processed:
            average_hh_salary = int(
                sum(average_hh_salaries) / hh_vacancies_processed
            )
        else:
            average_hh_salary = None

        if sj_vacancies_processed:
            average_sj_salary = int(
                sum(average_sj_salaries) / sj_vacancies_processed
            )
        else:
            average_sj_salary = None

        hh_language_popularity[language] = {
                "vacancies_found": fetch_hh_vacancies_amount( # кол-во вакансий
                    f"Программист {language}",
                    hh_area_id
                ),
                "vacancies_processed": hh_vacancies_processed,
                "average_salary": average_hh_salary
            }

        sj_language_popularity[language] = {
                "vacancies_found": fetch_sj_vacancies_amount(
                    superjob_secret_key,
                    f"Программист {language}",
                    town
                ),
                "vacancies_processed": sj_vacancies_processed,
                "average_salary": average_sj_salary
            }

    print_asciitable(hh_language_popularity, "HeadHunter Moscow")
    print_asciitable(sj_language_popularity, "Superjob Moscow")


if __name__ == "__main__":
    main()
