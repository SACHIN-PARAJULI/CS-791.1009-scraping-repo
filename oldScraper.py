import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def fetch_data(url):
    print(f"Fetching data from URL: {url}")
    res = requests.get(url)
    print(f"Status code: {res.status_code}")
    return res.json()

def scrapeReviewSite(url):
    review = ""
    review_url = url
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
    try:
        request = Request(review_url, headers=headers)
        review_page = urlopen(request, timeout=3)
        n_html = review_page.read().decode("utf-8")
        n_soup = BeautifulSoup(n_html, "html.parser")
        for text in n_soup.find_all('p'):
            punct = text.get_text()[-2:]
            if('.' in punct or '!' in punct or '?' in punct):
                if(len(text.get_text().split()) >= 25):
                    review = review + " " + text.get_text()
    except:
        print("Website could not be opened")
        return review

    return review

def process_page_info(res):
    print("Checking page information...")
    pageInfo = res.get("pageInfo", {})
    if not pageInfo:
        return False, None
    hasNextPage = pageInfo.get("hasNextPage", False)
    nextPage = pageInfo.get("endCursor")
    return hasNextPage, nextPage
newdict = [
  {
    "title": "Dune: Part Two",
    "emsId": "cecd223d-a20d-3268-bbef-9a4c847c673d"
  },
  {
    "title": "Dune",
    "emsId": "f7c22bab-5d5e-3b2e-a8a6-bd138df977ee"
  },
  {
    "title": "Oppenheimer",
    "emsId": "07d7f9a2-3fa1-342a-b6ca-27fd594e04c6"
  },
  {
    "title": "Puss in Boots: The Last Wish",
    "emsId": "de9ba2bd-3fdd-4b12-a519-a0a07bc30bf4"
  },
  {
    "title": "Godzilla Minus One",
    "emsId": "90c22bee-a1dd-44f6-8345-d1792b4dddc3"
  },
  {
    "title": "Marvel's The Avengers",
    "emsId": "f362b9f5-57e0-3021-a310-ececbcf2f49f"
  },
  {
    "title": "Mad Max: Fury Road",
    "emsId": "680ec6a1-da95-3c02-8690-7c23f1d18180"
  },
  {
    "title": "The Lord of the Rings: The Two Towers",
    "emsId": "35e97dbc-aef3-3121-b204-f814ca098b70"
  },
  {
    "title": "Mission: Impossible - Fallout",
    "emsId": "5004f9bf-acc7-3c99-8e7f-208a7a692f1f"
  },
  {
    "title": "Captain America: Civil War",
    "emsId": "e6eb9e3e-4a72-33a7-b44e-1f8cadf1dd8f"
  },
  {
    "title": "Star Wars: The Last Jedi",
    "emsId": "ad34316e-4d9c-3f65-a3cf-4a2174e294a1"
  },
  {
    "title": "The Northman",
    "emsId": "331878af-b880-421f-aaa3-a43f78697721"
  },
  {
    "title": "The Witcher",
    "emsId": "6f55bc2d-4f9a-390c-92ab-63acc5b8c84b"
  },
  {
    "title": "The Lord of the Rings: The Rings of Power",
    "emsId": "35e97dbc-aef3-3121-b204-f814ca098b70"
  },
  {
    "title": "Indiana Jones and the Kingdom of the Crystal Skull",
    "emsId": "ed91c42a-38e2-30ad-94ff-91be04905a35"
  },
  {
    "title": "The Witch",
    "emsId": "a881c2ba-4430-47c5-9829-c78da2fd1478"
  },
  {
    "title": "The Eyes of My Mother",
    "emsId": "916971e1-fbe2-3b39-bfef-80b730b69b27"
  },
  {
    "title": "Willow",
    "emsId": "01b53137-6aee-3747-9e5e-4c40776fa3c9"
  },
  {
    "title": "Uncut Gems",
    "emsId": "76c08fcb-877c-3416-9b17-76dee66745dd"
  },
  {
    "title": "Spy Kids",
    "emsId": "91571c74-cea1-4bd6-b156-e1f44fc4e18e"
  },
  {
    "title": "Ant-Man and the Wasp: Quantumania",
    "emsId": "431505cc-700e-4f8c-911a-2f3fcb2ac5a3"
  },
  {
    "title": "Star Wars: the Rise of Skywalker",
    "emsId": "d7083795-3ab7-3b17-9717-bbe6401ffd79"
  },
  {
    "title": "Morbius",
    "emsId": "efb6bf43-a63b-3117-9f94-b0c8d00af1b0"
  },
  {
    "title": "Joker",
    "emsId": "a50bc50f-396f-3d64-80f9-850414c4a40b"
  },
  {
    "title": "Man of Steel",
    "emsId": "3fbc9d82-14f0-3592-a00c-4f67b2a0da70"
  },
  {
    "title": "Eternals",
    "emsId": "2289d276-2f05-3965-a4d3-c2377c2fb0d6"
  },
  {
    "title": "Godzilla: King of the Monsters",
    "emsId": "1ea77d0a-a98c-31c4-9717-fe4b2f2b59cb"
  },
  {
    "title": "Uncharted",
    "emsId": "957b20be-2056-3318-9e77-1c7fef3aca9b"
  },
  {
    "title": "Fast X",
    "emsId": "00b20d93-6265-3079-a0da-de975d7ff0b1"
  },
  {
    "title": "Warcraft",
    "emsId": "09a55ab7-95a2-36ba-a2a7-aa0bd429ad24"
  },
  {
    "title": "Madami Web",
    "emsId": "7ddaaf2e-c123-4dce-a273-d06cfe249bc6"
  },
  {
    "title": "Best Laid Plans",
    "emsId": "c2a17d2e-1c07-3d54-b228-f0aa1c79874f"
  },
  {
    "title": "Gloria",
    "emsId": "63ad86f6-2048-3c50-95e0-fb6bc7cfea08"
  },
  {
    "title": "True Crime",
    "emsId":"29b74e4c-fb34-3d66-8d32-b22a4be42c02"
  },
  {
    "title":"One Tough Cop",
    "emsId": "018fb6a7-0495-3a2a-826d-61483e171d3c"
  },
  {
    "title": "Phoenix",
    "emsId": "0eb9ced5-3a30-3638-bf97-0067332d91aa"
  },
  {
    "title": "The Golden Child",
    "emsId":"7d492fbc-dfea-3338-8ebd-a9139eb44149"
  },
  {
    "title":"Imaginary",
    "emsId":"513ccb75-0212-3beb-a9da-98570972b55e"
  },
  {
    "title":"Dreamland",
    "emsId":"46b9c6c1-2cb7-3935-9a03-506f3a194362"
  },
  {
    "title":"Rebel Moon: Part One - A Child of Fire",
    "emsId":"0ac1266f-1215-4026-a216-e5522149c4bb"
  }
]
def save_data(data, filename="top_critics/lordofrings_top_critics.csv"):
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
    for movie in newdict:
        emsId = movie['emsId']
        initial_url = f"https://www.rottentomatoes.com/napi/movie/{emsId}/reviews/top_critics?after=MA&pageCount=20"
        initial_res = fetch_data(initial_url)
        hasNextPage, nextPage = process_page_info(initial_res)
        result = [initial_res]
        save_data([initial_res], f"top_critics/{movie['title'].replace(' ', '_')}_top_critics.csv")

        print(f"Fetching remaining data for movie {movie['title']}...")
        while hasNextPage:
            url = f"https://www.rottentomatoes.com/napi/movie/{emsId}/reviews/top_critics?after={nextPage}&pageCount=20"
            res = fetch_data(url)
            result.append(res)
            save_data([res], f"top_critics/{movie['title'].replace(' ', '_')}_top_critics.csv")
            hasNextPage, nextPage = process_page_info(res)
    print("Done.")

if __name__ == "__main__":
    main()
