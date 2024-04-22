import json
import requests
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor

FOLDER_PATH = "data/critics"
FILE_EXT = "critics.csv"
PAGE_COUNT = 50
THREAD_COUNT = 8


def load_data_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def fetch_data(url):
    print(f"Fetching data from URL: {url}")
    res = requests.get(url)
    print(f"Status code: {res.status_code}")
    return res.json()

def scrapeReviewSite(url):
    print(f"Scraping review from {url}")
    review = ""
    review_url = url
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
    try:    
        response = requests.get(review_url, headers=headers, timeout=3)
        print("Received response from website")
        n_html = response.text
        n_soup = BeautifulSoup(n_html, "html.parser")
        for text in n_soup.find_all('p'):
            punct = text.get_text()[-2:]
            if('.' in punct or '!' in punct or '?' in punct):
                if(len(text.get_text().split()) >= 25):
                    review = review + " " + text.get_text()
                    print(f"Added paragraph to review: {text.get_text()[:50]}...")
    except:
        print("Website could not be opened")
        return review
    print("Finished scraping review")
    return review

def process_page_info(res):
    print("Checking page information...")
    pageInfo = res.get("pageInfo", {})
    if not pageInfo:
        return False, None
    hasNextPage = pageInfo.get("hasNextPage", False)
    nextPage = pageInfo.get("endCursor")
    return hasNextPage, nextPage

def process_review(review):
    try:
        review_url = review.get("reviewUrl")
        scraped_review = scrapeReviewSite(review_url)
        if not scraped_review:
            scraped_review = review.get("quote")
        review["Reviews"] = scraped_review
        return review
    except Exception as e:
        print(f"Error processing review: {e}")
        return None

def save_data(data, filename):
    print(f"Saving data to '{filename}...")
    df_list = []
    for item in data:
        reviews = item.get("reviews", [])
        with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
            reviews = list(executor.map(process_review, reviews))
        df = pd.DataFrame(reviews)
        df = df[['creationDate', 'reviewUrl', 'originalScore', 'scoreSentiment', 'Reviews']]
        df_list.append(df)
    df = pd.concat(df_list, ignore_index=True)
    
    # Check if file exists to avoid writing header multiple times
    write_header = not os.path.exists(filename)
    df.to_csv(filename, mode='a', header=write_header, index=False, escapechar='\\')

def main():
    print("Fetching data...")
    movies_dict = load_data_from_json("data.json")
    for movie in movies_dict:
        emsId = movie['emsId']
        initial_url = f"https://www.rottentomatoes.com/napi/movie/{emsId}/reviews/all?after=MA&pageCount={PAGE_COUNT}"
        initial_res = fetch_data(initial_url)
        hasNextPage, nextPage = process_page_info(initial_res)
        result = [initial_res]
        save_data([initial_res], f"{FOLDER_PATH}/{movie['title'].replace(' ', '_')}_{FILE_EXT}")

        print(f"Fetching remaining data for movie {movie['title']}...")
        while hasNextPage:
            url = f"https://www.rottentomatoes.com/napi/movie/{emsId}/reviews/all?after={nextPage}&pageCount={PAGE_COUNT}"
            res = fetch_data(url)
            result.append(res)
            save_data([res], f"{FOLDER_PATH}/{movie['title'].replace(' ', '_')}_{FILE_EXT}")
            hasNextPage, nextPage = process_page_info(res)
    print("Done.")

if __name__ == "__main__":
    main()
