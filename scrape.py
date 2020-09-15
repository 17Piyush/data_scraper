import requests
from bs4 import BeautifulSoup
import pprint


res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')  # This will look on page 2
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.storylink')
subtext = soup.select('.subtext')
links2 = soup2.select('.storylink')
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2

# sort the list on the basis of votes, from max to min
def sort_stories_by_votes(hnlist):
	return sorted(hnlist, key= lambda k:k['votes'], reverse=True)


# make a dictionary of news with more than 100 votes
def create_custom_hn(links, subtext):               # hn = hacker news
	hn = []
	for idx, item in enumerate(links):              # links[idx] == item, we can use any of them
		title = item.getText()                      # collect the title of the news
		href = links[idx].get('href', None)         # collect the link of the news
		vote = subtext[idx].select('.score')        # collect the vote on the news
		if len(vote):
			points = int(vote[0].getText().replace(' points', ''))
			# only votes more than 100 is allowed
			if points > 99:
				hn.append({'title': title, 'link': href, 'votes': points})
	return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(mega_links, mega_subtext))