from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import csv
import time
import re

driver = webdriver.Chrome()
driver.get("https://www.carousell.ph/")
#?slt=null

# Click review button to go to the review section
#category_button = driver.find_element_by_xpath('//span[@class="padLeft6 cursorPointer"]')
#category_button.click()

tab = driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div[1]/div/div[2]')
tab.click()

time.sleep(2)
category_button = driver.find_element_by_xpath('//*[@id="root"]/div/div[4]/div[1]/div[1]/div/div[2]/div[19]/a/img')
category_button.click()

csv_file = open('videogames.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

index = 1
# We want to start the first two pages.
# If everything works, we will change it to while True
while index <=15:
	try:
		print("Scraping chunk number " + str(index))
		index = index + 1
		# Find all the reviews. The find_elements function will return a list of selenium select elements.
		# Check the documentation here: http://selenium-python.readthedocs.io/locating-elements.html
		

		listings = driver.find_elements_by_xpath('//div[@class="styles__cardContent___TpQXu"]')
		#listings = driver.find_elements_by_xpath('//div[@class="styles__listingsWrapper___2RJeL"]')

		# Iterate through the list and find the details of each review.
		for listing in listings:
			# Initialize an empty dictionary for each review
			
			listings_dict = {}
			
			# To get the attribute instead of the text of each element, use 'element.get_attribute(href) for example'
			try:
				product = listing.find_element_by_xpath('.//p[@class="styles__text___1gJzw styles__colorUrbanGrey60___2rwkI styles__overflowNormal___mT74G styles__singleline___nCFol styles__textAlignLeft___lqg5e styles__weightSemibold___uxIDP desktop__sizeS___30RAN"]').text

			except:
				continue

			price = listing.find_element_by_xpath('.//p[@class="styles__text___1gJzw styles__colorUrbanGrey60___2rwkI styles__overflowNormal___mT74G styles__singleline___nCFol styles__textAlignLeft___lqg5e styles__weightRegular___19l6i desktop__sizeM___3k5LI"]').text
			user = listing.find_element_by_xpath('.//p[@class="styles__text___1gJzw styles__colorUrbanGrey90___2NNa9 styles__overflowNormal___mT74G styles__singleline___nCFol styles__textAlignLeft___lqg5e styles__weightSemibold___uxIDP desktop__sizeS___30RAN"]').text
			status = listing.find_element_by_xpath('.//p[4][@class="styles__text___1gJzw styles__colorUrbanGrey60___2rwkI styles__overflowNormal___mT74G styles__singleline___nCFol styles__textAlignLeft___lqg5e styles__weightRegular___19l6i desktop__sizeS___30RAN"]').text
		
			driver.execute_script("arguments[0].scrollIntoView();",listing)
			
			#print('Product = {}'.format(product))
			#print('Price = {}'.format(price))
			#print('User = {}'.format(user))
			#print('='*50)
			
			# Use relative xpath to locate text, username, date_published, rating.
			# Your code here

			# Uncomment the following lines once you verified the xpath of different fields
			#text = review.find_element_by_xpath('.//span[@class = "pad6 onlyRightPad"]').text
			#rating = review.find_element_by_xpath('//*[@id="reviews"]/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/span/span[3]/span[1]').text
			
			#driver.execute_script("arguments[0].scrollIntoView();",review)
			listings_dict['product'] = product
			listings_dict['price'] = price 
			listings_dict['user'] = user
			listings_dict['status'] = status

			writer.writerow(listings_dict.values())
			
			#print('Text={}'.format(text))
			#print('Rating={}'.format(rating))

		# We need to scroll to the bottom of the page because the button is not in the current view yet.
		#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		#time.sleep(1)
		# Locate the next button element on the page and then call `button.click()` to click it.
		try:
			button = driver.find_element_by_xpath('//button[@class="styles__button___3dxOP desktop__button___2Hl0n styles__medium___3KEDn styles__outline___3AGrh desktop__outline___2UF39 styles__loadMore___yYAF4"]')
			#time.sleep(1)
			actions = ActionChains(driver)
			actions.move_to_element(button).click().perform()

			time.sleep(1)

		except:
			writer.writerow(listings_dict.values())

	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break