from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from math import sqrt
from typing import List

load_dotenv()

app = FastAPI()

OFFICIAL_EMAIL = "arshnoor3792.beai23@chitkara.edu.in"
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


@app.get("/health")
def health():
    return {
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    }


class BFHLRequest(BaseModel):
    fibonacci: int | None = None
    prime: List[int] | None = None
    lcm: List[int] | None = None
    hcf: List[int] | None = None
    AI: str | None = None


@app.post("/bfhl")
def bfhl(req: BFHLRequest):
    try:
        data = req.dict(exclude_none=True)

        if len(data) != 1:
            raise HTTPException(status_code=400, detail="Invalid input")

        key, value = next(iter(data.items()))

        if key == "fibonacci":
            result = fibonacci(value)

        elif key == "prime":
            result = [x for x in value if is_prime(x)]

        elif key == "lcm":
            result = lcm_array(value)

        elif key == "hcf":
            result = hcf_array(value)

        elif key == "AI":
            result = ask_ai(value)

        else:
            raise HTTPException(status_code=400, detail="Invalid key")

        return {
            "is_success": True,
            "official_email": OFFICIAL_EMAIL,
            "data": result
        }

    except Exception:
        return {
            "is_success": False,
            "error": "Server error"
        }


# -- LOGIC FUNCTIONS 
def fibonacci(n: int):
    if n <= 0:
        return []
    seq = [0, 1]
    for i in range(2, n):
        seq.append(seq[i-1] + seq[i-2])
    return seq[:n]


def is_prime(num: int):
    if num < 2:
        return False
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def lcm(a, b):
    return a * b // gcd(a, b)


def lcm_array(arr):
    res = arr[0]
    for x in arr[1:]:
        res = lcm(res, x)
    return res


def hcf_array(arr):
    res = arr[0]
    for x in arr[1:]:
        res = gcd(res, x)
    return res



def ask_ai(question: str):
    if not GEMINI_KEY:
        return "Unknown"

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [
                {"parts": [{"text": question}]}
            ]
        }

        r = requests.post(url, json=payload, timeout=10)
        data = r.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip().split()[0]  

    except Exception:
        return "Unknown"
