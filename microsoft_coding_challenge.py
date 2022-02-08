from collections import Counter
import requests
from bs4 import BeautifulSoup, NavigableString
from prettytable import PrettyTable

class TopFrequentWords:
	def __init__(self, url, frequency, exclusion_words=[], special_chars="!@#$%^&*()_-+={[}]\;:\"<>?/., 1234567890"):
		self.wordList = []
		self.url = url
		self.frequency = frequency
		self.exclusion_words = exclusion_words
		self.special_chars = special_chars
		
	def parseBetweenTwoTags(self, cur, end):
#		print("parsing between tags")
		while cur and cur != end:
			if isinstance(cur, NavigableString):
				text = cur.strip()
				if len(text):
					words = text.lower().split()
					for each_word in words:
						self.wordList.append(each_word)
			cur = cur.next_element

	def clean_data(self, wordlist):
		clean_list = []
		for word in wordlist:
			for i in range(len(self.special_chars)):
				word = word.replace(self.special_chars[i], '')
			if len(word) > 0:
				clean_list.append(word)
		return clean_list
		
	def getFrequentWords(self, clean_list):
		word_count = {}
		for word in clean_list:
			if word in word_count:
				word_count[word] += 1
			else:
				word_count[word] = 1
		for word in self.exclusion_words:
			del word_count[word]
			
		c = Counter(word_count)
		top10List = c.most_common(self.frequency)
		return top10List
		
	def findTopFrequentWords(self):
		source_code = requests.get(self.url).text
		soup = BeautifulSoup(source_code, 'html.parser')
		self.parseBetweenTwoTags(soup.find('h2', text='History').next_sibling,
							soup.find('h2', text='Corporate affairs'))
		clean_list = self.clean_data(self.wordList)
		return self.getFrequentWords(clean_list)
		
	def print_result(self, data):
		print("Result of crawling the webpage: ", self.url)
		table = PrettyTable(['Word', 'No of Occurrences'])
		for i, tuple in enumerate(data):
			table.add_row([tuple[0], tuple[1]])
		print(table)
		return
		
if __name__ == "__main__":
	solution = TopFrequentWords("https://en.wikipedia.org/wiki/Microsoft", 10)
	data = solution.findTopFrequentWords()
	solution.print_result(data)


#Result of crawling the webpage:  https://en.wikipedia.org/wiki/Microsoft
#+-----------+-------------------+
#|    Word   | No of Occurrences |
#+-----------+-------------------+
#|    the    |        264        |
#| microsoft |        150        |
#|     in    |        133        |
#|     to    |        111        |
#|     of    |        110        |
#|    and    |        106        |
#|     a     |        101        |
#|     on    |         82        |
#|  windows  |         66        |
#|    for    |         61        |
#+-----------+-------------------+
