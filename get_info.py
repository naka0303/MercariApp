from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs

SLEEP_TIME = 10

try:
    # chromedriverのパス格納
    driver_path = fs.Service(executable_path='/Users/nakagawa/Projects/MercariApp/chromedriver')

    # Chromeインスタンス作成
    driver = webdriver.Chrome(service=driver_path)

    # メルカリ公式サイトを開く
    driver.get("https://jp.mercari.com/")

    # 遷移判定
    driver.implicitly_wait(SLEEP_TIME)
    search_btn = driver.find_element(By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div/div/header/mer-navigation-top')

    print('sasasa')

    driver.close()

except Exception:
    driver.close()