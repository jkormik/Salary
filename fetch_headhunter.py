import requests
import objectpath
from fetched_data_processing import predict_salary


def predict_rub_salary_hh(vacancy, hh_area_id):
    average_salaries = []
    for salary in fetch_all_hh_salaries(vacancy, hh_area_id):
        if salary and salary["currency"] == "RUR":
            average_salaries.append(predict_salary(
                salary["from"],
                salary["to"]
            ))
    return list(filter(lambda average_salary:
        average_salary,
        average_salaries
        ))


def fetch_hh_vacancies(**params):
    url = "https://api.hh.ru/vacancies"
    response = requests.get(url, params=params)
    response.raise_for_status()
    decoded_response = response.json()
    if "error" in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response["error"])
    return decoded_response


def fetch_hh_area_id(**params):
    url = "https://api.hh.ru/suggests/areas"
    response = requests.get(url, params=params)
    response.raise_for_status()
    decoded_response = response.json()
    if "error" in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response["error"])
    return decoded_response["items"][0]["id"]


def fetch_all_hh_salaries(search_query, hh_area_id):
    pages_found = fetch_hh_vacancies_pages_amount(search_query, hh_area_id)
    all_hh_salaries = []
    for page in range(pages_found):
        vacancies = fetch_hh_vacancies(
            text=search_query,
            area=hh_area_id,
            page=page
        )
        tree_obj = objectpath.Tree(vacancies)
        all_hh_salaries += list(tree_obj.execute("$..salary"))
    return all_hh_salaries


def fetch_hh_vacancies_amount(search_query, hh_area_id):
    vacancies = fetch_hh_vacancies(text=search_query, area=hh_area_id)
    return vacancies["found"]


def fetch_hh_vacancies_pages_amount(search_query, hh_area_id):
    vacancies = fetch_hh_vacancies(text=search_query, area=hh_area_id)
    return vacancies["pages"]
