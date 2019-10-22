from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from db import Review

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\where\you\download\the\chromedriver.exe')
driver = webdriver.Chrome()

driver.get("https://www.verizonwireless.com/smartphones/samsung-galaxy-s8")
# Click review button to go to the review section
review_button = driver.find_element_by_xpath('//span[@class="padLeft6 cursorPointer"]')
review_button.click()

# Windows users need to open the file using 'wb'
# Page index used to keep track of where we are.
index = 1
while index True:
	try:
		print("Scraping Page number " + str(index))
		index = index + 1
		# Find all the reviews on the page
		wait_review = WebDriverWait(driver, 10)
		reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,
									'//div[@class="row border_grayThree onlyTopBorder noSideMargin"]')))
		for review in reviews:
			# Initialize an empty dictionary for each review
			review_dict = {}
			# Use relative xpath to locate the title, text, username, date.
			# Once you locate the element, you can use 'element.text' to return its string.
			# To get the attribute instead of the text of each element, use 'element.get_attribute()'
			try:
				title = review.find_element_by_xpath('.//div[@class="NHaasDS75Bd fontSize_12 wrapText"]').text
			except:
				continue

			# OPTIONAL PART 1a
			# Attempts to click the "read more" button to expand the text. This needs to be clicked
			# a second time otherwise the button click in the next review will collapse the previous
			# review text (and won't expand the current text).

			# We also need to scroll to the review element first because the button is not in the current view yet.
			driver.execute_script("arguments[0].scrollIntoView();", review)
			
			read_more_exists = False
			try:
				read_more = review.find_element_by_xpath('.//a[@class="border_gray onlyBottomBorder color_000 fontSize_1"]')
				read_more.click()
				read_more_exists = True
				# Slows down the text expansion so the text can be scraped
				time.sleep(.5)
			except:
				pass

			text = review.find_element_by_xpath('.//span[@class="pad6 onlyRightPad"]').text
			username = review.find_element_by_xpath('.//span[@class="padLeft6 NHaasDS55Rg fontSize_12 pad3 noBottomPad padTop2"]').text
			date_published = review.find_element_by_xpath('.//span[@class="NHaasDS55Rg fontSize_12  pad3 noBottomPad padTop2"]').text
			rating = review.find_element_by_xpath('.//span[@class="positionAbsolute top0 left0 overflowHidden color_000"]').get_attribute('style')
			rating = int(re.findall('\d+', rating)[0])/20	
	
			# OPTIONAL PART 1b
			# Click the read more button if it exists in order to collapse the text for the current review
			if read_more_exists:
				read_more.click()

			# create a Review object that correponds to one row of our table.
			cur_review = Review(username=username,
							title=title,
							text=text,
							date_published=date_published,
							rating=rating)
			cur_review.save()

		# We need to scroll to the bottom of the page because the button is not in the current view yet.
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Locate the next button on the page.
		wait_button = WebDriverWait(driver, 10)
		next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									'//li[@class="nextClick displayInlineBlock padLeft5 "]')))
		next_button.click()
	except Exception as e:
		print(e)
		csv_file.close()
		driver.close()
		break