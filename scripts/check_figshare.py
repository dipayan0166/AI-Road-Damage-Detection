import urllib.request
import json

url = "https://api.figshare.com/v2/articles/21431547"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(f"Title: {data.get('title')}")
        files = data.get('files', [])
        print(f"Total files: {len(files)}")
        for f in files:
            name = f.get('name')
            size_mb = f.get('size', 0) / (1024 * 1024)
            dl_url = f.get('download_url')
            print(f"- {name} ({size_mb:.1f} MB) -> {dl_url}")
except Exception as e:
    print(f"Error: {e}")

