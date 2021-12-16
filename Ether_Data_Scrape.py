from selenium import webdriver
from selenium.webdriver.common.keys import Keys #keystrokes
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

#takes in HolderAddress as paramater and returns ether price, ether value
def getEtherData(block_num):

#designate browser, create an instance of chromedriver
    driver = webdriver.Chrome() 
    
#Open etherscan.io in Chrome
    url = "https://etherscan.io/"
    driver.get(url)
    
#Find search bar, paste transaction ID and keystroke enter
    search = driver.find_element(By.ID, "txtSearchInput")   
    search.send_keys('0x49107a0662d96081896620cef66e6cce880368e92127763814ca6007061698b5')
    search.send_keys(Keys.ENTER)

#click first transaction
    xpath = '/html/body/div[1]/main/div[4]/div[3]/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/a'
    driver.find_element(By.XPATH, xpath).click()

#get ether value
    xpath = '/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[7]/div[2]/span/span'
    ethvalue = driver.find_element(By.XPATH, xpath)

#get ether price 
    xpath = '//*[@id="ContentPlaceHolder1_closingEtherPrice"]/div/div[2]'
    ethprice = driver.find_element(By.XPATH, xpath).text
    ethprice = ethprice[1:ethprice.find(" /")]
    ethprice = ethprice.replace(',', '')
    
# get eth amount
    xpath = '/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[8]/div[2]/span/span'
    ethamount = driver.find_element(By.XPATH, xpath).text
    
    return [ethprice, ethamount]

    driver.close()

def main():
    ether_price = getEtherData(4047627)
    print(ether_price)
    #for this example, should print $226.33

if __name__ == "__main__":
    main()
