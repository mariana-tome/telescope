import csv
import json
import bs4 as bs
from zenrows import ZenRowsClient


def scrape_page(url):
    client = ZenRowsClient("81b7af95c2741afcf45e00e5f3409eb50f259e64")
    params = {"js_render": "true", "premium_proxy": "true"}

    response = client.get(url, params=params)

    soup = bs.BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text
    sections = soup.find_all("div", {"class": "l5 mb-1"})
    seller_details = sections[1]
    seller_info = seller_details.parent.find_all("div", {"class": "ml-1"})

    result = {
        "title": title,
        "seller": seller_info[0].get_text(separator=":").split(":")[1],
        "year_founded": seller_info[1].get_text(separator=":").split(":")[1],
        "hq_location": seller_info[2].get_text(separator=":").split(":")[1],
        "twitter": seller_info[3].get_text(separator=":").split(":")[1],
        "linkedin_page": json.loads(seller_info[4].find_all_next("a")[0]['data-event-options'])['url']
    }
    print(result)


def main():
    with open('g2crowdurls.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for url in row:
                scrape_page(url)


main()
