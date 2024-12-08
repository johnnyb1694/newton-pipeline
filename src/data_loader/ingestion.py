"""Extracts data from a given publication outlet and flattens the resultant JSON into 
a pipe-delimited CSV format, ready for ingestion.

Note that "New York Times 'Archive Search'" is often abbreviated to "NYTAS" for brevity!
"""
import requests
import logging
import csv
from pathlib import Path
from transformation import (
    nytas_transform_author,
    nytas_transform_date
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def construct_nyt_archive_search_url(
    year: int,
    month: int,
    version: str = "v1"
) -> str:
    """Constructs the New York Times 'Archive Search' ("NYTAS") URL string.

    :param year: year of interest
    :param month: month of interest
    :param version: version tag of the API e.g. 'v1'
    :return: a formatted URL string
    """
    return f"https://api.nytimes.com/svc/archive/{version}/{year}/{month}.json"


def extract_nyt_archive(
    api_key: str,
    year: int,
    month: int
):
    """Extracts metadata 'archive' from NYTAS (for a given year and month).

    :param api_key: API key
    :param year: year of interest
    :param month: month of interest
    :return: a dictionary-encoded collection of name-value pairs in the JSON response
    """
    url = construct_nyt_archive_search_url(year, month)
    try:
        res = requests.get(url, params={'api-key': api_key})
        res.raise_for_status()
        return res.json()
    except requests.RequestException as err: 
        logging.error(f"Bad API request to NYT 'Archive Search': '{err}'")   


def filter_nyt_archive(
    res: dict
) -> list[dict]:
    """Filters the NYTAS response on the following relevant fields:

    * `headline`
    * `publication_date`
    * `author`
    * `news_desk`
    * `url`

    :param res: JSON encoded response from NYTAS (cf. `extract_nyt_archive()`)
    :return: a filtered dictionary-encoded collection of name-value pairs in the JSON response
    """
    try:
        articles = res["response"]["docs"]
        return [
            {
                "headline": article["headline"]["main"],
                "publication_date": nytas_transform_date(article["pub_date"]),
                "author": nytas_transform_author(article["byline"]["original"]),
                "news_desk": article["news_desk"],
                "url": article["web_url"]
            } 
            for article in articles
        ]
    except KeyError as err:
        logging.error(f"Unable to process `res` input (reconsider input structure): '{err}'")


def stage(
    records: list[dict],
    field_names: list[str],
    path: Path
) -> None:
    """Stage filtered JSON records as a pipe-delimited CSV file for further manipulation downstream.

    :param records: an iterable list of dictionary-based 'records'
    :param field_names: the names of the fields contained in each record (i.e. the dictionary keys)
    :param path: file path to act as a staging area
    """
    with open(path, 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=field_names, delimiter="|") 
        writer.writeheader() 
        writer.writerows(records)


if __name__ == "__main__":
    pass



