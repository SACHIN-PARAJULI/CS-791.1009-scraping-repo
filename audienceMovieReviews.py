import json
import requests
import pandas as pd
import os

FOLDER_PATH = "data/audience"
FILE_EXT = "audience.csv"
PAGE_COUNT = 100

def load_data_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def fetch_data(url):
    print(f"Fetching data from URL: {url}")
    res = requests.get(url)
    print(f"Status code: {res.status_code}")
    return res.json()

def process_page_info(res):
    print("Checking page information...")
    pageInfo = res.get("pageInfo", {})
    if not pageInfo:
        return False, None
    hasNextPage = pageInfo.get("hasNextPage", False)
    nextPage = pageInfo.get("endCursor")
    return hasNextPage, nextPage

def save_data(data, filename):
    print(f"Saving data to '{filename}...")
    df_list = []
    for item in data:
        reviews = item.get("reviews", [])
        df_list.append(pd.DataFrame(reviews))
    df = pd.concat(df_list, ignore_index=True)

    # Check if file exists to avoid writing header multiple times
    write_header = not os.path.exists(filename)

    df.to_csv(filename, mode='a', header=write_header, index=False)

def main():
    print("Fetching data...")
    newdict = load_data_from_json("data.json")
    for movie in newdict:
        emsId = movie['emsId']
        initial_url = f"https://www.rottentomatoes.com/napi/movie/{emsId}/reviews/user?after=MA&pageCount={PAGE_COUNT}"
        initial_res = fetch_data(initial_url)
        hasNextPage, nextPage = process_page_info(initial_res)
        result = [initial_res]
        save_data(
            [initial_res], f"{FOLDER_PATH}/{movie['title'].replace(' ', '_')}_{FILE_EXT}")

        print(f"Fetching remaining data for movie {movie['title']}...")
        while hasNextPage:
            url = f"https://www.rottentomatoes.com/napi/movie/{emsId}/reviews/user?after={nextPage}&pageCount={PAGE_COUNT}"
            res = fetch_data(url)
            result.append(res)
            save_data(
                [res], f"{FOLDER_PATH}/{movie['title'].replace(' ', '_')}_{FILE_EXT}")
            hasNextPage, nextPage = process_page_info(res)
    print("Done.")

if __name__ == "__main__":
    main()