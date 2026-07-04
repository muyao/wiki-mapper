import json
import requests
import time
from helpers import add_to_output
from helpers import is_bad_url
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Need to set a user-agent, wikipedia blocks default python one
HEADERS = {
	"User-Agent": "wiki-mapper-muyao/0.0.1 (https://github.com/muyao/wiki-mapper)"
}

# Max depth for recursive scrape
MAX_DEPTH = 1

# End after 1 hour (60 * 60 seconds)
END_AFTER = 60 * 60

# When the programme started
START_TIME = time.time()

# URL to start scraping
START_URL = "https://en.wikipedia.org/wiki/Philosophy"

# This will be go into output.json
output = {}

# Scrape single Wikipedia page. Return list of links
def scrape(url):
	print(f"Scraping {url}")

	# Fetch the webpage
	response = requests.get(url, headers=HEADERS)

	# Stop if not ok
	if response.status_code != 200:
		raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

	# Parse HTML
	soup = BeautifulSoup(response.content, "html.parser")

	# Find all <a> tags and get href
	links = []
	for link in soup.find_all("a"):
		href = link.get("href")

		# If href doesnt exist skip
		if not href:
			continue

		# Turn relative URLs like /wiki/Wikipedia into good URLs like https://en.wikipedia.org/wiki/Wikipedia
		# Only use the part before a #
		joined_url = urljoin(url, href).split("#")[0]

		# Filter out bad URLs
		if joined_url == url:
			continue
		if joined_url in links:
			continue
		if is_bad_url(joined_url):
			continue

		# Add to links list
		links.append(joined_url)

	# Return links
	return links

# Scrape recursively
def recursive_scrape(url, depth=0):

	# Get all links in page
	urls = scrape(url)

	# Stop and add to output if depth exceeds MAX_DEPTH
	if depth >= MAX_DEPTH:
		add_to_output(url, output, urls)
		return

	# For each link of this page
	for url in urls:

		# Stop if taking too long
		if time.time() > START_TIME + END_AFTER:
			break

		# Recursively scrape each page
		recursive_scrape(url, depth + 1)

		# 1 second delay to avoid getting 429ed
		time.sleep(1)

if __name__ == "__main__":

	# Run
	recursive_scrape(START_URL)

	# Write output into file
	with open("output.json", "w") as f:
		json.dump(output, f, indent="\t", ensure_ascii=False)