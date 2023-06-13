import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
import os

# Set the PYTHONIOENCODING environment variable
os.environ['PYTHONIOENCODING'] = 'UTF-8'

# Set the log file path
log_file = "scraping.log"

# Configure logging to write to the log file
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")

try:
    url = "https://www.imdb.com/chart/top/"
    source = requests.get(url=url)
    source.raise_for_status()

    soup = BeautifulSoup(source.text, "html.parser")

    movies = soup.find("tbody", class_="lister-list").find_all("tr")

    movie_data = []

    for movie in movies:
        name_element = movie.find("td", class_="titleColumn").a.text
        logging.info(f"The name_element is inserted")

        rank = movie.find("td", class_="titleColumn").get_text(strip=True).split(".")[0]
        logging.info(f"The rank is inserted in the list")

        year = movie.find("td", class_="titleColumn").span.text.strip("()")
        logging.info(f"The year is inserted")

        rating = movie.find("td", class_="ratingColumn").strong.text
        logging.info(f"The rating is inserted")

        movie_data.append({"Ranking": rank, "name_of_movie": name_element, "year": year, "rating": rating})

    df = pd.DataFrame(movie_data)
    df.to_csv("imdb.csv", index=False)

    logging.info("Import and scraping are done")
except Exception as e:
    print(e)
    logging.error(str(e))
