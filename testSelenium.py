from selenium import webdriver
#from bs4 import BeautifulSoup


driver = webdriver.PhantomJS(executable_path='/users/shashankagrawal/documents/phantomjs-2.1.1-macosx/bin/PhantomJS')

driver.set_window_size(1024, 768)
driver.get('http://journals.ametsoc.org')
content = driver.page_source

def info_from_ams():

	allIssues = driver.find_elements_by_link_text('Available Issues')

	for issue in allIssues:
		print issue.text.encode('utf-8')
		get_issue_info(issue.text.encode('utf-8'))

def get_issue_info(issue):

	driver.find_element_by_link_text(issue).click()
	issueList = []

	for i in range(1, 13):
		xpath = '//*[@id="962015"]/ul/li[%d]/div[1]/a' % (i)
		#print xpath
		issueList.append(xpath)


	for x in range(0,12):
		allIssues = driver.find_elements_by_xpath(issueList[x])
		print issueList[x]

	for issue in allIssues:
		print issue.text.encode('utf-8')
		print "print"




#journals = driver.find_elements_by_link_text('Abstract')

#journals[0].click()

#[0].implicitly_wait(3)

#title = driver.find_element_by_xpath("//*[@id='articleContent']/h1")

#print title.text.encode('utf-8')

#driver.quit()


#curl 'http://journals.ametsoc.org/doi/abs/10.1175/BAMS-D-14-00170.1'
info_from_ams() 

#//*[@id="tocContent"]/table[1]/tbody/tr/td[3]/a[1]
#//*[@id="tocContent"]/table[2]/tbody/tr/td[3]/a[1]