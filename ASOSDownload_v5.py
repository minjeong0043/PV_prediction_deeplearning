import os.path
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import  ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import  Service
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
error_num = []
def file_down(driver):
    # driver.find_element(By.XPATH, '//*[@id="dsForm"]/div[3]/button').click()
    # WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))

    Excel = driver.find_element(By.XPATH, '//*[@id="wrap_content"]/div[4]/div[1]/div/a[2]')
    driver.execute_script("arguments[0].scrollIntoView();", Excel)
    time.sleep(1)
    Excel.click()
    time.sleep(1)
    option = driver.find_element(By.XPATH, '//*[@id="reqstPurposeCd7"]')
    driver.execute_script("arguments[0].scrollIntoView();", option)
    time.sleep(1)
    # option.click()
    action = ActionChains(driver)
    time.sleep(1)
    action.move_to_element(option).click().perform()
    action = ActionChains(driver)
    action.move_to_element(option).click().perform()
    action = ActionChains(driver)
    action.move_to_element(option).click().perform()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="wrap-datapop"]/div/div[2]/div/a[2]').click()
    # time.sleep(50)
    WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))

def file_down_iter(i, month, bias, end_day):
    download_dir = f'D:\mj Kim\진행중인 업무\종관기상관측(ASOS)\ASOS2022\month{month}'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    driver.get("https://data.kma.go.kr/data/grnd/selectAsosRltmList.do?pgmNo=36")
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="loginBtn"]').click()
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'loading-')))
    try:
        driver.find_element(By.ID, 'loginId').send_keys("0043kmj@gmail.com")
        driver.find_element(By.ID, 'passwordNo').send_keys("muxinnrmmg")
        driver.find_element(By.ID, 'loginbtn').click()
        selenium_cookies = driver.get_cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="dataFormCd"]/option[5]').click()
        time.sleep(1)
        start_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[1]/button/img').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="datepicker_year"]').click()
        time.sleep(1)
        set_year = driver.find_element(By.XPATH, '//*[@id="datepicker_year"]/option[26]').click() #24- 2020/ 25- 2021
        time.sleep(1)
        set_month = driver.find_element(By.XPATH, f'//*[@id="datepicker_month"]/option[{month}]').click()  # //*[@id="datepicker_month"]/option[12] 12월임
        # time.sleep(2)
        set_day = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{bias+1}]/a').click()
        time.sleep(1)
        end_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[2]/button/img').click()
        time.sleep(1)
        set_year = driver.find_element(By.XPATH, '//*[@id="datepicker_year"]/option[26]').click()
        time.sleep(1)
        set_month = driver.find_element(By.XPATH, f'//*[@id="datepicker_month"]/option[{month}]').click()
        time.sleep(2)
        set_day = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{bias+1}]/a').click()
        time.sleep(1)
        # option 선택
        driver.find_element(By.XPATH, '//*[@id="ztree_1_check"]').click()
        driver.find_element(By.XPATH, '//*[@id="ztree1_1_check"]').click()

        if i < 8:
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
            start_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[1]/button/img').click()
            set_day = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            end_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[2]/button/img').click()
            set_day = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
            # #option 선택
            # driver.find_element(By.XPATH, '//*[@id="ztree_1_check"]').click()
            # driver.find_element(By.XPATH, '//*[@id="ztree1_1_check"]').click()
            # 조회 및 다운
            file_down(driver)
            print(f"day : {i-bias} / {end_day-1}")
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
        elif i < 15:
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
            start_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[1]/button/img').click()
            set_day = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i-7}]/a').click()
            end_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[2]/button/img').click()
            set_day = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i-7}]/a').click()

            # 조회 및 다운
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
            file_down(driver)
            print(f"day : {i-bias} / {end_day-1}")
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
        elif i < 22:
            start_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[1]/button/img').click()
            set_day = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[{i - 14}]/a').click()
            end_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[2]/button/img').click()
            set_day = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[{i - 14}]/a').click()
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
            # 조회 및 다운
            file_down(driver)
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
            print(f"day : {i-bias} / {end_day-1}")
        elif i < 29:
            start_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[1]/button/img').click()
            set_day = driver.find_element(By.XPATH,
                                          f'//*[@id="ui-datepicker-div"]/table/tbody/tr[4]/td[{i - 21}]/a').click()
            end_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[2]/button/img').click()
            set_day = driver.find_element(By.XPATH,
                                          f'//*[@id="ui-datepicker-div"]/table/tbody/tr[4]/td[{i - 21}]/a').click()

            # 조회 및 다운
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
            file_down(driver)
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
            print(f"day : {i-bias} / {end_day-1}")
        else:
            start_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[1]/button/img').click()
            set_day = driver.find_element(By.XPATH,
                                          f'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[{i - 28}]/a').click()
            end_yyyymmdd = driver.find_element(By.XPATH, '//*[@id="dayData"]/dd/div[2]/button/img').click()
            set_day = driver.find_element(By.XPATH,
                                          f'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[{i - 28}]/a').click()

            # 조회 및 다운
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
            file_down(driver)
            WebDriverWait(driver, 50).until(EC.invisibility_of_element_located((By.ID, "loading-mask")))
            print(f"day : {i-bias} / {end_day-1}")
    except Exception as e:
        print(f"error: {e}")
        error_num.append(i)

    finally:
        time.sleep(5)
        driver.quit()

# download_dir = 'D:\mj Kim\진행중인 업무\종관기상관측(ASOS)\month1'
# if not os.path.exists(download_dir):
#     os.makedirs(download_dir)
# options = webdriver.ChromeOptions()
# prefs = {
#     "download.default_directory": download_dir,
#     "download.prompt_for_download": False,
#     "download.directory_upgrade": True,
#     "safebrowsing.enabled":True
# }
# options.add_experimental_option("prefs", prefs)
# driver = webdriver.Chrome(options= options)
# bias = 5
# end_day = 31
# month = 5
# # month
# for i in range(1+bias, end_day+bias+1):
#     file_down_iter(i,month, bias, end_day+1)

# Year로 돌아가도록 해보기
month_bias_2020 = [3, 6, 0, 3, 5, 1, 3, 6, 2, 4, 0, 2]
end_day_list_2020 = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

month_bias_2021 = [5,1, 1, 4, 6, 2, 4, 0, 3, 5, 1, 3]
end_day_list_2021 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

month_bias_2022 = [6, 2, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
end_day_list_2022 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

month_bias_2023 = [0, 3, 3, 6, 1, 4, 6, 2, 5, 0, 3, 5]
end_day_list_2023 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
for i in range(1, 13):
    month = i
    bias = month_bias_2022[i-1]
    end_day = end_day_list_2022[i-1]
    print(f"~~~~~~~2021 - {month}~~~~~~~")
    for k in range(1+bias, end_day+bias+1):
        file_down_iter(k, month, bias, end_day+1)


