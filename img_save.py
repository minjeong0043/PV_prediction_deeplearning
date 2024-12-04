import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def setTime_saveData():
    # set time
    time_button = driver.find_element(By.XPATH, '//*[@id="searchTime"]').click()
    time.sleep(1)
    for j in range(1, 716):
        specific_time_button = driver.find_element(By.XPATH, f'//*[@id="searchTime"]/option[{716 - j}]').click()
        # save data
        time.sleep(1.3)
        save_button = driver.find_element(By.XPATH, '//*[@id="content"]/section/div[2]/div/div[2]/button[5]/i').click()
        original_img_button = driver.find_element(By.XPATH, '//*[@id="download-confirm"]/ul/li[1]/button/em').click()
        savePage_close_button = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/button').click()

def month_9():
    while True:
        current_month_year = driver.find_element(By.CLASS_NAME, 'ui-datepicker-title').text
        if "2024년 9월" in current_month_year:
            break
        prev_month_button = driver.find_element(By.CLASS_NAME, 'ui-datepicker-prev').click()
        time.sleep(1)
        print("press prev month")
    print("Reached September 2024")
    for i in range(6,31):
        if i<8:
            if i == 1:
                DD_button = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                time.sleep(1)
                setTime_saveData()
            else:
                YYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
                DD_button = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                time.sleep(1)
                setTime_saveData()

        elif i <15:
            YYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            time.sleep(1)
            setTime_saveData()

        elif i < 22:
            YYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            time.sleep(1)
            setTime_saveData()

        elif i < 29:
            YYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            time.sleep(1)
            setTime_saveData()

        else:
            dYYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            time.sleep(1)
            setTime_saveData()

def month_10():
    while True:
        current_month_year = driver.find_element(By.CLASS_NAME, 'ui-datepicker-title').text
        if "2024년 10월" in current_month_year:
            break
        driver.find_element(By.CLASS_NAME, 'ui-datepicker-prev').click()
        time.sleep(1)
        print("press prev month")
    print("Reached September 2024")

    for i in range(2+1,2+31):
        if i<8:
            if i == 1:
                driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                time.sleep(1)
                setTime_saveData()


            else:
                YYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
                DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                time.sleep(1)
                setTime_saveData()

        elif i <15:
            YYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            time.sleep(1)
            setTime_saveData()

        elif i < 22:
            YYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            time.sleep(1)
            setTime_saveData()

        elif i < 29:
            YYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            time.sleep(1)
            setTime_saveData()

        else:
            YYYYMMDD_button = driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            time.sleep(1)
            setTime_saveData()

def month_11():
    while True:
        current_month_year = driver.find_element(By.CLASS_NAME, 'ui-datepicker-title').text
        if "2024년 11월" in current_month_year:
            break
        driver.find_element(By.CLASS_NAME, 'ui-datepicker-prev').click()
        time.sleep(1)
        print("press prev month")
    print("Reached September 2024")

    for i in range(6+1,6+31):
        if i<8:
            if i == 1:
                driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                time.sleep(1)
                setTime_saveData()


            else:
                driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
                driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                time.sleep(1)

                setTime_saveData()

        elif i <15:
            driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i-7}]/a').click()
            time.sleep(1)
            setTime_saveData()

        elif i < 22:
            driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[{i-14}]/a').click()
            time.sleep(1)
            setTime_saveData()

        elif i < 29:
            driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[4]/td[{i-21}]/a').click()
            time.sleep(1)
            setTime_saveData()

        else:
            driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()
            driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[{i-28}]/a').click()
            time.sleep(1)
            setTime_saveData()

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)
url = 'https://nmsc.kma.go.kr/homepage/html/satellite/viewer/selectNewSatViewer.do?dataType=operSat'
driver.get(url)
driver.refresh()

time.sleep(5)

try:
    input("Press enter when you set information!! (자료 종류, 영역 .etc)")
    # set YYYY-MM-DD
    driver.find_element(By.XPATH, '//*[@id="inputsearch"]').click()

    month_9()
    month_10()
    month_11()

    print('Finish downloading')
    print("Button clicked successfully!")
except Exception as e:
    print(f"An error occurred: {e}")

# Close the browser
input("Enter")
driver.quit()