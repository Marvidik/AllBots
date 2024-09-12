import requests
from bs4 import BeautifulSoup

# Simulate a real browser by adding headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://google.com",  # A referer header can help sometimes
}

# URL of the StockTwits followers page
followers_url = "https://stocktwits.com/GambitMentality/followers"
response = requests.get(followers_url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')

    # Find the div with the infinite scroll component class
    infinite_scroll_div = soup.find('div', class_="infinite-scroll-component")
    print(infinite_scroll_div)
    if infinite_scroll_div:
        # Now try to find the child divs inside the infinite scroll div
        followers = infinite_scroll_div.find_all('div', class_="flex flex-row justify-between items-center mx-5 my-6")
        print(followers)
        # Extract and print usernames
        for follower in followers:
            # Target the div with class UserPageFollows_avatarContainer__RGim7 flex
            avatar_container = follower.find('div', class_="UserPageFollows_avatarContainer__RGim7 flex")
            if avatar_container:
                # Find the next div with class ml-4 and extract the username
                ml4_div = avatar_container.find_next_sibling('div', class_="ml-4")
                if ml4_div:
                    username_link = ml4_div.find('a')
                    if username_link and 'href' in username_link.attrs:
                        # Extract the username from the href attribute
                        username = username_link['href'].split('/')[-1]
                        print(f"Username: {username}")
                    else:
                        print("failed3")
                else:
                    print("failed2")
            else:
                print("failed1")
    else:
        print("Could not find the infinite scroll component div.")
else:
    print(f"Failed to fetch page, status code: {response.status_code}")
#fortoto

