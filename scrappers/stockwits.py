import requests
from bs4 import BeautifulSoup
import csv
import os

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

# Open the usernames file (common.txt) and read the usernames
with open(usernames_file, 'r') as f:
    usernames = f.read().splitlines()

# Total usernames for progress calculation
total_usernames = len(usernames)

# Create and open a CSV file for writing the output
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(['Username', 'Scraped Link', 'Bio'])

    # Loop through each username in the list
    for index, username in enumerate(usernames):
        profile_url = f"https://stocktwits.com/{username}"
        response = requests.get(profile_url, headers=headers)

        # Only process if the response is successful (profile exists)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            # Find the element with the class "UserPageHeader_descriptionContainer__ZTG_A"
            links = soup.find('div', class_="UserPageHeader_descriptionContainer__ZTG_A")
            scraped_link = ""

            # Check if the element was found and extract its content
            if links:
                scraped_link = links.text.strip()  # Get the link

            # Find the bio with the class "UserPageHeader_bio__U6eL8"
            bio = soup.find('p', class_="UserPageHeader_bio__U6eL8 break-words")
            bio_text = bio.text.strip() if bio else "Bio not found"

            # Write the username, scraped link, and bio to the CSV
            csvwriter.writerow([username, scraped_link, bio_text])
            csvfile.flush()  # Flush the output to ensure it's written to the file immediately

        else:
            # Handle profiles that do not exist (optional: log or print)
            print(f"Profile for username '{username}' does not exist.")

        # Show progress update to the user
        progress = (index + 1) / total_usernames * 100
        print(f"\rProcessed {index + 1}/{total_usernames} usernames ({progress:.2f}% done)", end='')

print("\nScraping completed. Results saved in stocktwits_profiles.csv")
