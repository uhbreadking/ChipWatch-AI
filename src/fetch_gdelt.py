import time
import requests
import pandas as pd

URL = "https://api.gdeltproject.org/api/v2/doc/doc"
HEADERS = {"User-Agent": "ChipWatch-AI/0.1 (student portfolio project)"}
GDELT_DATE_FORMAT = "%Y%m%dT%H%M%SZ"
#Writing these names in ALL CAPS is a Python convention meaning “this is a setting that won’t change while the program runs.”

def _get_json(params, retries=2):
    """Ask GDELT for data and return it as a Python dictionary."""
    for attempt in range(retries + 1):
        resp = requests.get(URL, params=params, headers=HEADERS, timeout=45)
        if resp.status_code == 429 and attempt < retries:
            time.sleep(15)
            continue
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            if attempt < retries:
                time.sleep(6)
                continue
            raise RuntimeError(f"GDELT returned non-JSON response: {resp.text[:200]}")

def historical_attention(query, days=30):
    """Daily count of matching articles. This is NEWS ATTENTION, not risk."""
    params = {
        "query": query,
        "mode": "timelinevolraw",
        "format": "json",
        "timespan": f"{days}d",
    }
    payload = _get_json(params)

    series = payload.get("timeline", [])
    if not series or not series[0].get("data"):
        return pd.DataFrame(columns=["date", "value"])

    df = pd.DataFrame(series[0]["data"])
    df["date"] = pd.to_datetime(df["date"], format=GDELT_DATE_FORMAT, errors="coerce", utc=True)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna(subset=["date", "value"]).reset_index(drop=True)