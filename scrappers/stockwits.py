import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# File paths
usernames_file = 'names.txt'
output_file = 'stocktwits_profiles.csv'

# Simulate a real browser by adding headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://google.com",  # A referer header can help sometimes
}

# Function to scrape a single user's profile
def scrape_profile(username):
    profile_url = f"https://stocktwits.com/{username}"
    response = requests.get(profile_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        # Find the element with the class "UserPageHeader_descriptionContainer__ZTG_A"
        links = soup.find('div', class_="UserPageHeader_descriptionContainer__ZTG_A")
        scraped_link = links.text.strip()

        # Find the bio with the class "UserPageHeader_bio__U6eL8"
        bio = soup.find('p', class_="UserPageHeader_bio__U6eL8 break-words")
        bio_text = bio.text.strip()

      

        # Only return data if there is either a link or a bio
        if scraped_link or bio_text != "Bio not found":
            return username, scraped_link, bio_text
        else:
            return None  # Profile has neither link nor bio
    else:
        return None  # Profile does not exist

# Open the usernames file and read the usernames
with open(usernames_file, 'r') as f:
    usernames = f.read().splitlines()

# Create and open a CSV file for writing the output
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(['Username', 'Scraped Link', 'Bio'])

    # Use ThreadPoolExecutor to scrape profiles concurrently
    with ThreadPoolExecutor(max_workers=15) as executor:
        # Submit tasks to the executor
        future_to_username = {executor.submit(scrape_profile, username): username for username in usernames}

        # Process the results as they complete
        for future in as_completed(future_to_username):
            result = future.result()
            if result:  # Only write to CSV if result is not None
                username, scraped_link, bio_text = result
                if scraped_link or bio_text != "Bio not found":  # Double-check if either link or bio exists
                    csvwriter.writerow([username, scraped_link, bio_text])
                    csvfile.flush()  # Flush the output to ensure it's written to the file immediately

            # Show progress update to the user
            progress = (list(future_to_username.keys()).index(future) + 1) / len(usernames) * 100
            print(f"\rProcessed {list(future_to_username.keys()).index(future) + 1}/{len(usernames)} usernames ({progress:.2f}% done)", end='')

print("\nScraping completed. Results saved in stocktwits_profiles.csv")
