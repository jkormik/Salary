import os
from dotenv import load_dotenv
from fetch_headhunter import fetch_hh_vacancies_amount, predict_rub_salary_hh
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

    for language in programming_languages:

        average_hh_salaries = predict_rub_salary_hh(f"Программист {language}",
                                                    town)
        average_sj_salaries = predict_rub_salary_sj(superjob_secret_key,
                                                    f"Программист {language}",
                                                    town)

        hh_vacancies_processed = len(average_hh_salaries)
        sj_vacancies_processed = len(average_sj_salaries)

        if hh_vacancies_processed != 0:
            everage_hh_salary = int(sum(average_hh_salaries)/hh_vacancies_processed)
        else:
            everage_hh_salary = None

        if sj_vacancies_processed != 0:
            everage_sj_salary = int(sum(average_sj_salaries)/sj_vacancies_processed)
        else:
            everage_sj_salary = None

        hh_language_popularity[language] = {
                "vacancies_found": fetch_hh_vacancies_amount(
                                                    f"Программист {language}",
                                                    town
                                                            ),
                "vacancies_processed": hh_vacancies_processed,
                "average_salary": everage_hh_salary
            }

        sj_language_popularity[language] = {
                "vacancies_found": fetch_sj_vacancies_amount(
                                                    superjob_secret_key,
                                                    f"Программист {language}",
                                                    town
                                                            ),
                "vacancies_processed": sj_vacancies_processed,
                "average_salary": everage_sj_salary
            }

    print_asciitable(hh_language_popularity, "HeadHunter Moscow")
    print_asciitable(sj_language_popularity, "Superjob Moscow")


if __name__ == "__main__":
    main()
