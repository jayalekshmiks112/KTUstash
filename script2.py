import requests
from bs4 import BeautifulSoup

# Make a GET request to the website
url = "https://www.keralanotes.com/p/ktu-study-materials.html?m=1"
response = requests.get(url)

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the links on the page
links = soup.find_all("a")

# Print the href attribute of each link
for link in links:
    print(link.get("href"))
