import requests
import objectpath
from fetched_data_processing import predict_salary


def fetch_sj_vacancies(superjob_secret_key, **params):
    headers = {
        "X-Api-App-Id": superjob_secret_key
    }
    url = "https://api.superjob.ru/2.0/vacancies"
    response = requests.get(url, headers=headers, params=params)
    return response.json(), response.text


def predict_rub_salary_sj(superjob_secret_key, vacancy, area):
    average_salaries = []
    for salary in fetch_all_sj_salaries(superjob_secret_key, vacancy, area):
        if salary and salary[2] == "rub" and (salary[1]+salary[0]):
            average_salaries.append(predict_salary(
                int(salary[0]),
                int(salary[1])
            ))

    return list(filter(lambda average_salary:
        average_salary,
        average_salaries
        ))


def fetch_sj_vacancies_pages_amount(superjob_secret_key, search_query, area):
    amount_of_vacancies = fetch_sj_vacancies_amount(
        superjob_secret_key,
        search_query, area
    )
    return (amount_of_vacancies//20) + 1


def fetch_sj_vacancies_amount(superjob_secret_key, search_query, area):
    vacancies = fetch_sj_vacancies(
        superjob_secret_key,
        keyword=search_query,
        town=area
    )
    tree_obj = objectpath.Tree(vacancies[0])
    return list(tree_obj.execute("$..total"))[0]


def fetch_all_sj_salaries(superjob_secret_key, search_query, area):
    pages_found = fetch_sj_vacancies_pages_amount(
        superjob_secret_key,
        search_query,
        area
    )
    all_sj_salaries = []
    for page in range(pages_found):
        vacancies = fetch_sj_vacancies(
            superjob_secret_key,
            keyword=search_query,
            town=area,
            page=page
        )
        tree_obj = objectpath.Tree(vacancies[0])
        all_sj_salaries_from = list(tree_obj.execute("$..payment_from"))
        all_sj_salaries_to = list(tree_obj.execute("$..payment_to"))
        all_sj_salary_currencies = list(tree_obj.execute("$..currency"))
        all_sj_salaries += zip(
            all_sj_salaries_from,
            all_sj_salaries_to,
            all_sj_salary_currencies
        )
    return all_sj_salaries
