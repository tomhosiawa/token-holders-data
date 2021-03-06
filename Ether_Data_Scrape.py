from selenium import webdriver
from selenium.webdriver.common.keys import Keys #keystrokes
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

#takes in hash as paramater and returns ether price, ether value

def getEtherData(hash):

#designate browser, create an instance of chromedriver
    driver = webdriver.Chrome() 
    
#Open etherscan.io in Chrome
    url = "https://etherscan.io/"
    driver.get(url)
    
#Find search bar, paste hash and keystroke enter
    search = driver.find_element(By.ID, "txtSearchInput")   
    search.send_keys(hash)
    search.send_keys(Keys.ENTER)

#get ether amount
    xpath = '/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[9]/div[2]/span/span'
    ethamount = driver.find_element(By.XPATH, xpath).text
    ethamount = ethamount[1:ethamount.find(" ")] 
    
#get ether price 
    xpath = '//*[@id="ContentPlaceHolder1_closingEtherPrice"]/div/div[2]'
    ethprice = driver.find_element(By.XPATH, xpath).text
    ethprice = ethprice[1:ethprice.find(" /")]
    ethprice = ethprice.replace(',', '')

    driver.close()
    return [ethprice, ethamount]


def main():
    ether_price = getEtherData('0x48ff3dfdec7106041566ea34fb0c0bf6481ccbc9b450b1b139f99920dbc94904')
    print(ether_price)

if __name__ == "__main__":
    main()
