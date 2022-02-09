import requests
import json
import objectpath
from fetched_data_processing import predict_salary


def predict_rub_salary_hh(vacancy, area):
    average_salaries = []
    for salary in fetch_all_hh_salaries(vacancy, area):
        if salary and salary["currency"] == "RUR":
            average_salaries.append(predict_salary(salary["from"],
                                                   salary["to"]))

    return average_salaries


def fetch_hh_vacancies(**params):
    url = "https://api.hh.ru/vacancies"
    response = requests.get(url, params=params)
    return response.json(), response.text


def fetch_hh_areas(**params):
    url = "https://api.hh.ru/areas"
    response = requests.get(url, params=params)
    return response.json(), response.text


def fetch_hh_area_id(area_name):
    jdata = json.loads(fetch_hh_areas()[1])
    tree_obj = objectpath.Tree(jdata)
    try:
        return tuple(tree_obj.execute(f"$..areas[@.name is {area_name}]"))[0]["id"]
    except IndexError:
        return None


def fetch_all_hh_salaries(search_query, area):
    hh_area_id = fetch_hh_area_id(area)
    pages_found = fetch_hh_vacancies_pages_amount(search_query, area)
    all_hh_salaries = []
    for page in range(pages_found):
        vacancies = fetch_hh_vacancies(text=search_query,
                                       area=hh_area_id,
                                       page=page)
        jdata = json.loads(vacancies[1])
        tree_obj = objectpath.Tree(jdata)
        all_hh_salaries += list(tree_obj.execute("$..salary"))
    return all_hh_salaries


def fetch_hh_vacancies_amount(search_query, area):
    hh_area_id = fetch_hh_area_id(area)
    vacancies = fetch_hh_vacancies(text=search_query, area=hh_area_id)[0]
    return vacancies["found"]


def fetch_hh_vacancies_pages_amount(search_query, area):
    hh_area_id = fetch_hh_area_id(area)
    vacancies = fetch_hh_vacancies(text=search_query, area=hh_area_id)[0]
    return vacancies["pages"]+1
