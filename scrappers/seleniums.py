import time
from playwright.sync_api import sync_playwright

def scrape_followers():
    with sync_playwright() as p:
        # Launch browser (headless mode can be set to False to see the browser)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Set a user-agent to mimic a real browser
        page.set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

        # Navigate to the followers page
        url = 'https://stocktwits.com/GambitMentality/followers'
        page.goto(url)

        # Scroll down and load more followers (simulate lazy loading)
        last_height = page.evaluate("document.body.scrollHeight")

        while True:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for content to load
            new_height = page.evaluate("document.body.scrollHeight")

            if new_height == last_height:  # Break if no more new content is loaded
                break

            last_height = new_height

        # Extract all followers' usernames
        followers = page.query_selector_all("a.username")

        # Extract the text content of each follower's username and save them
        usernames = [f.text_content() for f in followers]

        # Close browser
        browser.close()

        # Write the usernames to a file
        with open('followers.txt', 'w') as f:
            for username in usernames:
                f.write(f"{username}\n")

        print(f"Scraped {len(usernames)} usernames.")
        
# Run the scraper
scrape_followers()
