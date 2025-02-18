import os
import time
import random
import requests
import subprocess

# Google API key and search engine ID
API_KEY = "API KEY"
SEARCH_ENGINE_ID = "SEARCH ENGINE ID NEXT TO API KEY IN GOOGLE CLOUD CONSOLE"

# Updated list of file types
FILETYPES = [
    "pdf", "docx", "txt", "xls", "xlsx", "ppt", "csv", "rtf",
    "doc", "bak", "tmp"
]

def google_search(query, filetype, start=1):
    """Performs a Google Custom Search query."""
    while True:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": f"{query} filetype:{filetype}",
            "start": start
        }
        response = requests.get(url, params=params)

        print(f"Request URL: {response.url}")

        if response.status_code == 429:
            print("429 Error: Too many requests. Applying delay before retry...")
            time.sleep(random.uniform(1, 6))
            continue

        response.raise_for_status()
        results = response.json()

        if "items" not in results:
            print("No results found. Retrying after a short delay...")
            time.sleep(random.uniform(1, 2))

        return results

def download_file(url, folder):
    """Downloads a file from a given URL and saves it."""
    os.makedirs(folder, exist_ok=True)
    local_filename = os.path.join(folder, url.split("/")[-1])
    
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {local_filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def process_files(folder):
    """Processes downloaded files using exiftool for metadata extraction."""
    metadata_filename = os.path.join(folder, "metadata.txt")
    
    with open(metadata_filename, "w", encoding="utf-8") as meta_file:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if not os.path.isfile(file_path) or filename in {"metadata.txt", "metadata-urls.txt"}:
                continue

            meta_file.write(f"Metadata for {filename}:\n")
            try:
                result = subprocess.run(
                    ["exiftool", "-Author", "-Creator", "-CreatorTool", "-Producer", "-Title", file_path],
                    capture_output=True, text=True, check=True
                )
                meta_file.write(result.stdout)
            except subprocess.CalledProcessError as e:
                meta_file.write(f"Error processing {filename}: {e}\n")
            meta_file.write("\n" + "=" * 40 + "\n")
    
    print(f"Metadata saved to {metadata_filename}")

def main():
    domain = input("Enter the domain to search (e.g., example.com): ").strip()
    folder_name = domain.replace(".", "_")
    
    print(f"Starting search for documents on {domain}...")

    urls_found = []

    for filetype in FILETYPES:
        for start in range(1, 91, 10):  # Google API allows up to 100 results
            try:
                print(f"Searching for {filetype} files, results {start}-{start+9}...")
                results = google_search(f"site:{domain}", filetype, start)
                if "items" in results:
                    for item in results["items"]:
                        link = item.get("link")
                        if link:
                            print(f"Found: {link}")
                            urls_found.append(link)
                            download_file(link, folder_name)
            except Exception as e:
                print(f"Error during search: {e}")

        print(f"Completed search for {filetype} files. Pausing for 2 minutes to avoid rate limits...")
        time.sleep(120)

    # Write all found URLs to metadata-urls.txt
    urls_filename = os.path.join(folder_name, "metadata-urls.txt")
    try:
        with open(urls_filename, "w", encoding="utf-8") as url_file:
            for url in urls_found:
                url_file.write(url + "\n")
        print(f"All URLs saved to {urls_filename}")
    except Exception as e:
        print(f"Failed to write URLs to file: {e}")

    print("Processing downloaded files with exiftool...")
    process_files(folder_name)

if __name__ == "__main__":
    main()
