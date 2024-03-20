# Standard library imports
import json
import logging
import time

# Third-party imports
from fastapi import APIRouter,Request, FastAPI
from fastapi import HTTPException

from pydantic import ValidationError
from typing import List
import requests
from bs4 import BeautifulSoup
import uvicorn

from pydantic import BaseModel
from ..models.blog_models import BlogTitles


# Local imports
from ..services import llm_api as llm, prompts as pr

logger = logging.getLogger("AppLogger")
router = APIRouter()

def extract_h_titles(url: str) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    htitles = [h.text for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    return htitles


""" @router.get("/seo/google_keyw_rank")
async def root(keyword: str, num_results: int = 10, n_pages: int = 1):
    results = []
    counter = 0
    for page in range(0, n_pages):
        url = f"https://www.google.com/search?q={keyword}&start={page * 10}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        search = soup.find_all("div", class_="tF2Cxc")

        for h in search:
            if counter == num_results:
                break
            counter += 1
            title = h.find("h3").text
            link = h.find("a")["href"]
            rank = counter
            htitles = extract_h_titles(link)

            results.append(
                {
                    "title": title,
                    "url": link,
                    "rank": rank,
                    "htitles": htitles,
                }
            )

    return {"results": results} """


@router.get("/seo/google_keyw_rank")
async def root(keyword: str, num_results: int = 10, n_pages: int = 1):
    try:
        results = []
        counter = 0
        for page in range(0, n_pages):
            url = f"https://www.google.com/search?q={keyword}&start={page * 10}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            search = soup.find_all("div", class_="tF2Cxc")

            for h in search:
                if counter == num_results:
                    break
                counter += 1
                title = h.find("h3").text
                link = h.find("a")["href"]
                rank = counter
                htitles = extract_h_titles(link)

                results.append(
                    {
                        "title": title,
                        "url": link,
                        "rank": rank,
                        "htitles": htitles,
                    }
                )

        if not results:
            return {"success": False, "message": "No results found"}
        else:
            return {"success": True, "message": "Generated Titles Successfully", "result": results}
    except Exception as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}