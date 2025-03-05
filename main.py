import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the Amazon Bestsellers page
driver.get("https://www.amazon.com.br/gp/bestsellers/")


time.sleep(3)

# Find all lists on the page
lists = driver.find_elements(By.XPATH, '//ol[@class="a-carousel" and @role="list"]')

# Find list names based on the specified class
list_names_elements = driver.find_elements(By.XPATH, '//div[@class="a-column a-span8"]')
list_names = [name_element.text for name_element in list_names_elements]

# Open a CSV file to write the data
with open('amazon_bestsellers.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write header row
    csvwriter.writerow(['List Name', 'Item Number', 'Item Name'])

    # Loop through each list and its corresponding name
    for list_index, (item_list, list_name) in enumerate(zip(lists, list_names)):
        # Find items within the list and limit to 2 items
        items = item_list.find_elements(By.XPATH,
                                        './/div[@class="p13n-sc-truncate-desktop-type2  p13n-sc-truncated"]')

        # Extract and write the text from the first two items to the CSV
        for item_index, item in enumerate(items[:2]):  # Limit to the first 2 items
            csvwriter.writerow([list_name, item_index + 1, item.text])

driver.quit()
