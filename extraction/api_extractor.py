import requests

# Template for extracting from a real business API (CRM / product API).
# It follows the pattern from the project specification: authentication
# header, pagination, and basic error handling.
# In this project the pipeline runs on local sample files, so this file
# is provided ready to connect when a real API and key are available.
# Put the key in an environment variable, never in the code.


def fetch_pages(base_url, api_key=None, page_size=50, max_pages=10):
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    all_records = []
    for page in range(1, max_pages + 1):
        try:
            response = requests.get(base_url, headers=headers,
                                    params={"page": page, "limit": page_size}, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"API request failed on page {page}: {e}")
            break

        records = response.json()
        if isinstance(records, dict):
            records = records.get("data", [])
        if not records:
            break
        all_records.extend(records)
        if len(records) < page_size:
            break
    return all_records
