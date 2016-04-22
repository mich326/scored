import os, re
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


class geography_extractor:
	def __init__(self, geograpy_path = './GeoLite2-City-Locations.csv'):
		self.punc_list = ['!','.','/',',','?']
		self._country_continent_map = {}
		self._district_country_map =  {}
		self._city_district_map = {}
		self._location_set = set()
		self._city_set = set()
		self._parse_geograpy(geograpy_path)


	def extract_geography(self, text):
		found_location = set()
		text = text.replace('\n','')
		for punc in self.punc_list:
			text = text.replace(punc, ' ')
		
		test_text = ' ' + text + ' '

		for location in self._location_set:
			test_location = ' ' + location + ' '
			if test_location in test_text:
				'''
				print location
				try: district = self._city_district_map[location]
				except KeyError: district = ''
				try: country = self._district_country_map[location]
				except KeyError: country = ''
				try: continent = self._country_continent_map[location]
				except KeyError: continent = ''
				if location in self._city_set: city = location
				else: city = ''
				full_location = ','.join([continent, country, district, city])
				'''
				found_location.add(location)
				test_text.replace(test_location, ' ')
		print "\n"
		return found_location

	def _parse_geograpy(self, geograpy_path):
		for line in open(geograpy_path):
			#line = line.lower()
			#line = line.replace(',', ' ')
			#line = re.sub(r'[^\w]', '', line)
			#print line.split(',')
			continent = line.split(',')[2]
			acronym = line.split(',')[3]
			country = line.split(',')[4]
			district = line.split(',')[6]
			city = line.split(',')[7]
			city = city.replace('\n','').split("/")[-1].replace('"','')
			#print city

			if continent != '' and country != '': self._country_continent_map[country] = continent
			if country != '' and district != '': self._district_country_map[district] = country
			if district != '' and city != '': self._city_district_map[city] = district

			if continent != '': self._location_set.add(continent)
			if country != '': self._location_set.add(country)
			if district != '': self._location_set.add(district)
			if acronym != '': self._location_set.add(acronym)

			if city != '': 
				self._location_set.add(city)
				self._city_set.add(city)

		self._location_set.add('USA')
		self._location_set.add('UK')
			

if __name__ == '__main__':
	g = geography_extractor()
	g.extract_geography('I am from Los Angeles,California.wpe owaifj opa wfoiajf skajf dsah Chino Hills, Fremont')