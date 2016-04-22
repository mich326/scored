import json, nltk, os, random
from geography_extractor import geography_extractor
from pprint import pprint

#random.seed(25)



def argmax(iterable):
	max_ = 0
	idx = -1
	for i, j in enumerate(iterable):
		if max_ < j:
			max_ = j
			idx = i
	return idx

class parse_from_abstract:
	def __init__(self, data, df):
		self.data = data
		self.g_extractor = geography_extractor()
		self.data_file = df
		self.flag_phrases = ["data from", "analysis on", "used data", "was used", "data set"]
		self.flag_words = ["dataset", "corpus", "corpora", "datum", "data", "database", "from"]
		self.bad_words = ["satellite", "society", "laboratory", "lab", "university", "institute", "instruments", "universidad", "published", "publish"]
		self.parse_abstracts(self.data, self.data_file)
	
	def generate_sentence_score(self, sentence):
		sentence = sentence.lower()
		sentence = ' ' + sentence + ' '
		score = 0
		for phrase in self.flag_phrases:
			if phrase in sentence:
				#print 'FLAG: ' + phrase
				score += 3
				sentence = sentence.replace(phrase,'')
		for word in self.flag_words:
			word = ' ' + word + ' '
			if word in sentence:
				#print 'FLAG: ' + word
				score += 2
				sentence = sentence.replace(word, '')
		for word in self.bad_words:
			word = ' ' + word + ' '
			if word in sentence:
				#print 'FLAG: ' + word
				score = score - 1
				sentence = sentence.replace(word, '')
		
		return score
		#print scores.values()
		#idx =  argmax(scores.values())
		
		#if idx != -1: print scores.keys()[idx] 
	

	def parse_abstracts(self, data, data_file):

		# Neatly prints out the abstract for comparison with resulting extracted datasets,
		# which are also printed
		pprint(self.data['abstract'])
		pprint(self.data['abstract'], self.data_file)
		
		json_abstract = self.data['abstract']
		json_abstract = json_abstract.replace('\n',' ')
		#text = nltk.word_tokenize(json_abstract)
		#pos_tags = nltk.pos_tag(text)
		sentences = nltk.tokenize.sent_tokenize(json_abstract)


		# Searches for datasets using basic rule:
		# ( Proper noun followed by 1 or more of: Noun, Conjunction, Preoposition,
		# another Proper Noun, Plural Noun, or Determiner ) OR multiple Proper Nouns
		grammar = r"""
			NP: {(<NNP><NN|CC|NNP|IN|NNS|DT>+)|<NNP>+}
			
		"""
		cp = nltk.RegexpParser(grammar)


		results = set()
		scores_results = set()

		for sentence in sentences:
			text = nltk.tokenize.word_tokenize(sentence)
			pos_tags = nltk.pos_tag(text)
			#print pos_tags
			for item in cp.parse(pos_tags):
				names = []
				
				if hasattr(item, 'label') and item.label:
					
					# If the item has been selected by our regex grammar rule:
					if item.label() == 'NP':
						names.append(' '.join([child[0] for child in item]))
						
						# Next five lines are a sloppy way of avoiding names like
						# J. Doe as well as removing basic single-word selections,
						# unless they are acronyms. Questionable filter, will be
						# improved soon.sss
						
						#print 'score: ' + str(self.generate_sentence_score(sentence))
						score = self.generate_sentence_score(sentence)
						if len(names[0].split(" ")) > 1 and names[0][1] != '.':
							results.add(names[0])
							if score > 0: scores_results.add(names[0])
						
						elif sum(1 for l in names[0] if l.isupper()) > 1 and names[0][1] != '.':
							results.add(names[0]) 
							if score > 0: scores_results.add(names[0])

		# Creates a set of locations that are present in the json file abstract
		locations = self.g_extractor.extract_geography(json_abstract)
		print "Locations: ",locations
		print '\n'
		print "Results with Locations included: ", results
		print '\n'
		print "Results with score-filtered sentences", scores_results
		pprint(results, self.data_file)
		pprint(locations, self.data_file)
		discard_list = []
		for item1 in locations:	
			for item2 in results:
				if item1 in item2:
					discard_list.append(item2)
		for x in discard_list:
			results.discard(x)
		print "Results without locations: ", results
		# results_less_locations = results.difference(locations)
		# print results_less_locations
		# pprint(locations, self.data_file)
		# pprint(results_less_locations, self.data_file)
		pprint(results, self.data_file)
		print '\n'


if __name__ == '__main__':

	data_file = open('datasets.txt', 'w+')

	for i in range(1): # Change this value to determine how many abstracts you want tested
		data = []

		# The folder jsonFiles, as mentioned in the README, should be in the same directory
		# as this file, and contain the raw files without additional folders. This can 
		# change once we test the extraction on all of our abstracts.

		json_file = random.choice(os.listdir('./jsonFiles'))

		# Prints name of the file that was selected for opening and parsing
		print "Name of json file: " + json_file
		data_file.write("Name of json file: " + json_file)
		data_file.write('\n')
		with open('./jsonFiles/' + json_file) as f:
			data = json.load(f)
		pfa = parse_from_abstract(data, data_file)

