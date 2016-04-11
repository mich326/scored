import json, nltk, os, random
from pprint import pprint


def parse_abstracts(data):

	# Neatly prints out the abstract for comparison with resulting extracted datasets,
	# which are also printed
	pprint(data['abstract'])
	print "\n"
	
	json_abstract = data['abstract']

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
	print results
	print '\n'


for i in range(4): # Change this value to determine how many abstracts you want tested
	data = []

	# The folder jsonFiles, as mentioned in the README, should be in the same directory
	# as this file, and contain the raw files without additional folders. This can 
	# change once we test the extraction on all of our abstracts.

	json_file = random.choice(os.listdir('./jsonFiles'))

	# Prints name of the file that was selected for opening and parsing
	print "Name of json file: " + json_file
	with open('./jsonFiles/' + json_file) as f:
		data = json.load(f)
	parse_abstracts(data)

