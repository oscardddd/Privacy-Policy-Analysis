import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import concurrent.futures
import subprocess
import sys



def find_privacy_policy_link(url):
    try:
        # Referenced from https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        # Potential improvements: https://thehftguy.com/2020/07/28/making-beautifulsoup-parsing-10-times-faster/
        s = requests.Session()
        response = s.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        likely_candidates = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            link_text = link.text.lower()
            if 'privacy' in link_text or 'privacy' in href.lower():
                full_url = urljoin(url, href)
                likely_candidates.append(full_url)
        
        footers = soup.find_all(['footer', 'div'], class_=['footer', 'page-footer'])
        for footer in footers:
            for link in footer.find_all('a', href=True):
                if 'privacy' in link.text.lower():
                    full_url = urljoin(url, link['href'])
                    if full_url not in likely_candidates:
                        likely_candidates.append(full_url)
        
        return likely_candidates[0] if likely_candidates else None
    
    except Exception as e:
        print(f"Error retrieving URL {url}: {e}")
        return None

def get_privacy_policy_content(privacy_policy_url):
    """Get the content of the privacy policy from its URL."""
    try:
        response : requests.models.Response = requests.get(privacy_policy_url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error retrieving privacy policy URL {privacy_policy_url}: {e}")
        return None
    
def process_line(line, region):
    global num_successes
    homepage_url = "http://" + line.strip()

    privacy_policy_link = find_privacy_policy_link(homepage_url)
    if privacy_policy_link:
        if not privacy_policy_link.startswith('http'):
            from urllib.parse import urljoin
            privacy_policy_link = urljoin(homepage_url, privacy_policy_link)

        privacy_policy_content = get_privacy_policy_content(privacy_policy_link)
        if privacy_policy_content:
            print("Privacy Policy Content Retrieved Successfully")
            num_successes += 1
            with open(f"results/{region}.{line.strip()}.html", "w+", encoding='utf-8') as file:
              file.write(privacy_policy_content)
        else:
            print("Failed to Retrieve Privacy Policy Content")
    else:
        print("Privacy Policy Link Not Found")

if __name__ == '__main__':
  regions = ['al', 'au', 'at', 'be', 'br', 'bg', 'ca', 'co', \
             'hr', 'cz', 'dk', 'ee', 'fi', 'fr', 'de', 'gr', \
             'hk', 'hu', 'ie', 'il', 'it', 'jp', 'lv', 'mx', \
             'nl', 'nz', 'no', 'pl', 'pt', 'ro', 'rs', 'sg', \
             'sk', 'za', 'es', 'se', 'ch', 'gb', 'ua', 'us']
  
  for region in regions:
    # result = subprocess.run(['mullvad', 'relay', 'set', 'location', region], capture_output=True, text=True)
    # result = subprocess.run(['mullvad', 'connect'], capture_output=True, text=True)

    num_successes = 0

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    num_domains = len(lines)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_line = {executor.submit(process_line, line, region): line for line in lines}
        
        for future in concurrent.futures.as_completed(future_to_line):
            line = future_to_line[future]
            try:
                future.result()
            except Exception as exc:
                print(f'{line} generated an exception: {exc}')

    print(f"Successes: {num_successes} / {num_domains} for {region}")