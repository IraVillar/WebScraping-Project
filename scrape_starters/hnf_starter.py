from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import csv
import time
import re

driver = webdriver.Chrome()
driver.get("https://www.carousell.ph/")


csv_file = open('hnf.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

time.sleep(3)
next_button = driver.find_element_by_xpath('//div[@class="styles__arrowContainer___1W_TE styles__arrowLeftRightContainer___1ZbYd styles__arrowRightContainer___3uvCS"]')
next_button.click()
time.sleep(1)
property_button = driver.find_element_by_xpath('//div[10]/a[@class="styles__collectionLink___37_IC styles__link___9msaS"]')
property_button.click()

time.sleep(3)

index = 1

while index <=15:
	try:
		print("Scraping chunk number " + str(index))
		index = index + 1
		
		listings = driver.find_elements_by_xpath('//div[@class="styles__cardContent___TpQXu"]')
		
		for listing in listings:
			# Initialize an empty dictionary for each review
			listings_dict = {}
			
			try:
				product = listing.find_element_by_xpath('.//p[@class="styles__text___1gJzw styles__colorUrbanGrey60___2rwkI styles__overflowNormal___mT74G styles__singleline___nCFol styles__textAlignLeft___lqg5e styles__weightSemibold___uxIDP desktop__sizeS___30RAN"]').text
			except:
				continue

			price = listing.find_element_by_xpath('.//p[@class="styles__text___1gJzw styles__colorUrbanGrey60___2rwkI styles__overflowNormal___mT74G styles__singleline___nCFol styles__textAlignLeft___lqg5e styles__weightRegular___19l6i desktop__sizeM___3k5LI"]').text
			user = listing.find_element_by_xpath('.//p[@class="styles__text___1gJzw styles__colorUrbanGrey90___2NNa9 styles__overflowNormal___mT74G styles__singleline___nCFol styles__textAlignLeft___lqg5e styles__weightSemibold___uxIDP desktop__sizeS___30RAN"]').text
			status = listing.find_element_by_xpath('.//p[4][@class="styles__text___1gJzw styles__colorUrbanGrey60___2rwkI styles__overflowNormal___mT74G styles__singleline___nCFol styles__textAlignLeft___lqg5e styles__weightRegular___19l6i desktop__sizeS___30RAN"]').text
			#status = listing.find_element_by_xpath('//*[@id="root"]/div/div[3]/div[1]/div[2]/main/div[1]/div/div/div[1]/a[2]/p[4]').text
			driver.execute_script("arguments[0].scrollIntoView();",listing)
			
			
			listings_dict['product'] = product
			listings_dict['price'] = price 
			listings_dict['user'] = user
			listings_dict['status'] = status
		

			writer.writerow(listings_dict.values())
			
			
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
