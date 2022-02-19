import requests
import objectpath
from fetched_data_processing import predict_salary


def predict_rub_salary_hh(vacancy, area):
    average_salaries = []
    for salary in fetch_all_hh_salaries(vacancy, area):
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


def fetch_hh_areas(**params):
    url = "https://api.hh.ru/areas"
    response = requests.get(url, params=params)
    response.raise_for_status()
    decoded_response = response.json()
    if "error" in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response["error"])
    return decoded_response


def fetch_hh_area_id(area_name):
    tree_obj = objectpath.Tree(fetch_hh_areas())
    try:
        return tuple(tree_obj.execute(f"$..areas[@.name is {area_name}]"))[0]["id"]
    except IndexError:
        return None


def fetch_all_hh_salaries(search_query, area):
    hh_area_id = fetch_hh_area_id(area)
    pages_found = fetch_hh_vacancies_pages_amount(search_query, area)
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


def fetch_hh_vacancies_amount(search_query, area):
    hh_area_id = fetch_hh_area_id(area)
    vacancies = fetch_hh_vacancies(text=search_query, area=hh_area_id)
    return vacancies["found"]


def fetch_hh_vacancies_pages_amount(search_query, area):
    hh_area_id = fetch_hh_area_id(area)
    vacancies = fetch_hh_vacancies(text=search_query, area=hh_area_id)
    return vacancies["pages"]
