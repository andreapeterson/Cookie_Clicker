from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Keep Chrome browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Set-Up
driver = webdriver.Chrome(options=chrome_options)  # Tells selenium how to work with latest version of browsers
driver.get("https://orteil.dashnet.org/cookieclicker/")

time.sleep(5)  # Gives dynamic website time to load

# Getting through pop-ups of accepting cookies and choosing language
accept_cookies = driver.find_element(By.XPATH, value="/html/body/div[1]/div/a[1]")
accept_cookies.click()

select_english = driver.find_element(By.XPATH, value="//*[@id='langSelect-EN']")
select_english.click()

time.sleep(5)  # Gives dynamic website time to load(again)

# Code for collecting cookies and purchasing upgrades and timing
time_to_check = time.time() + 10  # Personally, I found 10 seconds inbetween purchases to be the sweet spot where you can save up more cookies to buy bigger products but still small enough where you are buying frequently to get better clicks per second
five_mins = time.time() + 60 * 5
cookie = driver.find_element(By.ID, value="bigCookie")

keep_clicking = True
while keep_clicking:
    cookie.click()

    while time.time() > time_to_check:
        # See if there are available upgrades to purchase first
        for n in range(8, -1, -1):
            try:
                upgrade = driver.find_element(By.ID, f"upgrade{n}")
                upgrade.click()
            except:
                pass
        # See if there are available products to purchase second
        for n in range(19, -1, -1):
            try:
                product = driver.find_element(By.ID, f"product{n}")
                check_class = product.get_attribute("class")
                # Below will buy as many of the highest tier product first, then go to the next cheaper option and do the same until can't purchase any thing more
                while check_class == "product unlocked enabled":
                    product.click()
                    check_class = product.get_attribute("class")
            except:
                pass
        time_to_check = time_to_check + 10

    if time.time() > five_mins:
        time.sleep(0.1)  # Fixes stale element error
        cookie_per_s = driver.find_element(by='id', value="cookiesPerSecond")
        print(f"Cookies baked per second: {cookie_per_s.text} cookies.")
        break
