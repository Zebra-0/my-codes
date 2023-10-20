import re
import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://rjempregos.net/vagas/home-office"
base_url_vaga = "https://rjempregos.net/vagasrio/"
header = "h2"

def request_data(link):
    # print(f"Escaneando link: {link}...")
    response = requests.get(link)
    if response.status_code != 200:
        print("Pagina fora do ar ou link inválido")
        return None
    return BeautifulSoup(response.text, "html.parser")

def parse_titles(soup):
    titles = soup.find_all(header)
    black_list = ['Navegação por posts', 'Ultimas Notícias', 'Veja Todas as Notícias']
    print([title.text for title in titles if title.text not in black_list])
    return [title.text for title in titles if title.text not in black_list]

def parse_links(soup):
    links = soup.find_all("a", href=re.compile(f"^{base_url_vaga}"))
    # print(f"encontrao link com {links}")
    # print(list(set([link["href"] for link in links])))
    return list(set([link["href"] for link in links]))

# def get_job_info(num_of_pages):
#     jobs = []
#     links = []
#     for page in range(1, num_of_pages+1):
#         if not page != 1:
#             url = base_url
#         else:
#             url = f"{base_url}/page/{page}/"
#         soup = request_data(url)
#         # print(soup)
#         if not soup:
#             print("algo acontece")
#             continue
#         jobs += parse_titles(soup)
#         links += parse_links(soup)
#     job_info = dict(zip(jobs, links))
#
#     # Removing title-link pairs that have low keyword similarity
#     for title, link in list(job_info.items()):
#         if not any(keyword in link for keyword in title.split()):
#             del job_info[title]
#     return job_info

def get_job_info(num_of_pages):
    jobs = []
    links = []
    for page in range(1, num_of_pages + 1):
        if not page != 1:
            url = base_url
        else:
            url = f"{base_url}/page/{page}/"
        soup = request_data(url)
        if not soup:
            continue
        jobs += parse_titles(soup)
        links += parse_links(soup)
    job_info = dict(zip(jobs, links))

    # Removing title-link pairs that have low keyword similarity
    for title, link in list(job_info.items()):
        if not any(keyword in link for keyword in title.split()):
            del job_info[title]
    return job_info


def save_to_csv(job_info):
    with open('job_info.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['index', 'title', 'link'])
        for index, (title, link) in enumerate(job_info.items()):
            writer.writerow([index+1, title, link])

job_info = get_job_info(1)
# save_to_csv(job_info)
print(job_info)
