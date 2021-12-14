from selenium import webdriver
from selenium.webdriver.common.keys import Keys #keystrokes
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

#takes in block number as paramater and returns its ether price
def getEtherPrice(block_num):

#designate browser, create an instance of chromedriver
    driver = webdriver.Chrome() 
    
#Open etherscan.io in Chrome
    url = "https://etherscan.io/"
    driver.get(url)

#Find search bar, paste block # and keystroke enter
    search = driver.find_element(By.ID, "txtSearchInput")   
    search.send_keys(block_num)
    search.send_keys(Keys.ENTER)

#get etherprice 
    xpath = '//*[@id="ContentPlaceHolder1_closingEtherPrice"]/div/div[2]'
    ethprice = driver.find_element(By.XPATH, xpath)

    return ethprice.text 

    driver.close()

def main():
    ether_price = getEtherPrice(4047627)
    print(ether_price) 
    #for this example, should print $226.33 / ETH