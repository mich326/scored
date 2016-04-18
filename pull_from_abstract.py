import json, nltk, os, random
from geography_extractor import geography_extractor
from pprint import pprint


class parse_from_abstract:
	def __init__(self, data, df):
		self.data = data
		self.g_extractor = geography_extractor()
		self.data_file = df
		self.parse_abstracts(self.data, self.data_file)
		
	def parse_abstracts(self, data, data_file):

		# Neatly prints out the abstract for comparison with resulting extracted datasets,
		# which are also printed
		pprint(self.data['abstract'])

		#data_file.write(data['abstract'])
		pprint(self.data['abstract'], self.data_file)
		
		json_abstract = self.data['abstract']
		text = nltk.word_tokenize(json_abstract)
		sentence = nltk.pos_tag(text)

		# Searches for datasets using basic rule:
		# ( Proper noun followed by 1 or more of: Noun, Conjunction, Preoposition,
		# another Proper Noun, Plural Noun, or Determiner ) OR multiple Proper Nouns
		grammar = r"""
			NP: {(<NNP><NN|CC|NNP|IN|NNS|DT>+)|<NNP>+}
			
		"""
		cp = nltk.RegexpParser(grammar)


		results = set()

		for item in cp.parse(sentence):
			names = []
			
			if hasattr(item, 'label') and item.label:
				
				# If the item has been selected by our regex grammar rule:
				if item.label() == 'NP':
					names.append(' '.join([child[0] for child in item]))
					
					# Next five lines are a sloppy way of avoiding names like
					# J. Doe as well as removing basic single-word selections,
					# unless they are acronyms. Questionable filter, will be
					# improved soon.
					if len(names[0].split(" ")) > 1 and names[0][1] != '.':
						results.add(names[0])
					
					elif sum(1 for l in names[0] if l.isupper()) > 1 and names[0][1] != '.':
						results.add(names[0]) 

		# Creates a set of locations that are present in the json file abstract
		locations = self.g_extractor.extract_geography(json_abstract)
		print "Locations: ",locations
		print '\n'
		print "Results with Locations included: ", results
		print '\n'
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

	for i in range(2): # Change this value to determine how many abstracts you want tested
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

