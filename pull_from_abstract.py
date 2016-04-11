import json, nltk, os, random
from pprint import pprint


# with open('/Users/josh/Desktop/jsonFiles/www-the-cryosphere-net-6-1221-2012-.json') as f:
# 	data = json.load(f)
# patterns = [
# 	(r'.*sson$', 'VBG')

# ]

def parse_abstracts(data):
	pprint(data['abstract'])
	print "\n"
	json_abstract = data['abstract']

	text = nltk.word_tokenize(json_abstract)
	sentence = nltk.pos_tag(text)
	# print sentence

	grammar = r"""
		NP: {(<NNP><NN|CC|NNP|IN|NNS|DT>+)|<NNP>+}
		
	"""

	cp = nltk.RegexpParser(grammar)
	results = set()
	for item in cp.parse(sentence):
		names = []
		if hasattr(item, 'label') and item.label:
			if item.label() == 'NP':
				names.append(' '.join([child[0] for child in item]))
				# print names, len(names), names[0]

				if len(names[0].split(" ")) > 1 and names[0][1] != '.':
					results.add(names[0])
				elif sum(1 for l in names[0] if l.isupper()) > 1 and names[0][1] != '.':
					results.add(names[0]) 
	print results
	print '\n'


for i in range(4):
	data = []
	json_file = random.choice(os.listdir('./jsonFiles'))
	print json_file
	with open('./jsonFiles/' + json_file) as f:
		data = json.load(f)
	parse_abstracts(data)