import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from test1206_function import saveData
driver = webdriver.Chrome()

time.sleep(5)
url = 'https://nmsc.kma.go.kr/homepage/html/satellite/viewer/selectNewSatViewer.do?dataType=operSat'
driver.get(url)
driver.refresh()
time.sleep(5)

# Define button
YYYYMMDD_xpath = '//*[@id="inputsearch"]'
prev_month_button_xpath = 'ui-datepicker-prev'
future_month_button_xpath = '//*[@id="ui-datepicker-div"]/div/a[2]/span'
time_button_xpath =  '//*[@id="searchTime"]'

try:
    input("Press enter when you set information!! (자료 종류, 영역 .etc)")
    driver.find_element(By.XPATH, YYYYMMDD_xpath).click()

    # month_9()
    # 9월달 나올 때까지 이전달 버튼 누르기
    while True:
        current_month_year = driver.find_element(By.CLASS_NAME, 'ui-datepicker-title').text
        if "2024년 9월" in current_month_year:
            break
        driver.find_element(By.CLASS_NAME, prev_month_button_xpath).click()
        time.sleep(1)
        print('press prev month')
    print("Reached September 2024")

    # Day 버튼
    # for i in range(30,31):
    for i in range(4, 5):
        if i < 8:
            if i == 4:
                DD_button = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                time.sleep(1)
                # 데이터 다운
                driver.find_element(By.XPATH, time_button_xpath).click()
                time.sleep(1)
                for j in range(5, 720, 5):
                    specific_time_button = driver.find_element(By.XPATH, f'//*[@id="searchTime"]/option[{720 - j}]').click()
                    time.sleep(3)
                    saveData(driver)
                time.sleep(1)
            else:
                driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
                DD_button = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                for j in range(5, 720, 5):
                    specific_time_button = driver.find_element(By.XPATH, f'//*[@id="searchTime"]/option[{720 - j}]').click()
                    time.sleep(1.3)
                    saveData(driver)
                time.sleep(1.3)
        elif i < 15:
            if i == 14:
                DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i - 7}]/a').click()
                time.sleep(2)
                for j in range(665, 720, 5):
                    specific_time_button = driver.find_element(By.XPATH,f'//*[@id="searchTime"]/option[{720 - j}]').click()
                    time.sleep(1.5)
                    saveData(driver)
                time.sleep(1)
            else:
                driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
                DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i - 7}]/a').click()
                time.sleep(1.5)
                for j in range(5, 720, 5):
                    specific_time_button = driver.find_element(By.XPATH,f'//*[@id="searchTime"]/option[{720 - j}]').click()
                    time.sleep(1.5)
                    saveData(driver)
                time.sleep(1)
        elif i < 22:
            driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
            DD_button = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[{i - 14}]/a').click()
            time.sleep(1.5)
            for j in range(5, 720, 5):
                specific_time_button = driver.find_element(By.XPATH, f'//*[@id="searchTime"]/option[{720 - j}]').click()
                time.sleep(1.5)
                saveData(driver)
                time.sleep(1)
        elif i < 29:
            if i == 26:
                DD_button = driver.find_element(By.XPATH,
                                                f'//*[@id="ui-datepicker-div"]/table/tbody/tr[4]/td[{i - 21}]/a').click()
                time.sleep(3)
                for j in range(5, 720, 5):
                    specific_time_button = driver.find_element(By.XPATH,
                                                               f'//*[@id="searchTime"]/option[{720 - j}]').click()
                    time.sleep(3)
                    saveData(driver)
                time.sleep(2)
            else:
                driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
                DD_button = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[4]/td[{i - 21}]/a').click()
                time.sleep(2)
                for j in range(5, 720, 5):
                    specific_time_button = driver.find_element(By.XPATH, f'//*[@id="searchTime"]/option[{720 - j}]').click()
                    time.sleep(2)
                    saveData(driver)
                    time.sleep(1)
        else:
            driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
            DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[{i - 28}]/a').click()
            time.sleep(1.5)
            for j in range(5, 720, 5):
                specific_time_button = driver.find_element(By.XPATH, f'//*[@id="searchTime"]/option[{720 - j}]').click()
                # time.sleep(2)
                # saveData(driver)
                # time.sleep(1)
    time.sleep(1)


    # month_10()
    # # 10월달 나올 때까지 이전달 버튼 누르기
    # while True:
    #     current_month_year = driver.find_element(By.CLASS_NAME, 'ui-datepicker-title').text
    #     if "2024년 10월" in current_month_year:
    #         break
    #     driver.find_element(By.CLASS_NAME, prev_month_button_xpath).click()
    #     time.sleep(1)
    #     print('press prev month')
    # print("Reached September 2024")
    #
    # # Day 버튼
    # for i in range(2+24, 2+32):
    #     if i < 8:
    #         if i == 2+1:
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
    #             time.sleep(1)
    #             # 데이터 다운
    #             driver.find_element(By.XPATH, time_button_xpath).click()
    #             time.sleep(1)
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(2)
    #                 saveData(driver)
    #             time.sleep(1)
    #         else:
    #             driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(1.3)
    #                 saveData(driver)
    #             time.sleep(1.3)
    #     elif i < 15:
    #         if i == 10:
    #             driver.find_element(By.XPATH, '// *[ @ id = "inputsearch"]').click()
    #             # // *[ @ id = "ui-datepicker-div"] / table / tbody / tr[2] / td[4] / a
    #             DD_button = driver.find_element(By.XPATH,f'// *[ @ id = "ui-datepicker-div"] / table / tbody / tr[2] / td[{i-7}] / a').click()
    #             # DD_button = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[2]/a').click()
    #             time.sleep(2)
    #             for j in range(373, 718, 5):
    #                 print("-----")
    #                 time.sleep(1)
    #                 driver.find_element(By.XPATH, '//*[@id="searchTime"]').click()
    #                 # driver.find_element(By.XPATH, '//*[@id="searchTime"]/option[712]')
    #                 specific_time_button = driver.find_element(By.XPATH,f'//*[@id="searchTime"]/option[{718 - j}]').click()
    #                 time.sleep(1.3)
    #                 saveData(driver)
    #             time.sleep(1)
    #         else:
    #             driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i - 7}]/a').click()
    #             time.sleep(2)
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(2)
    #                 saveData(driver)
    #             time.sleep(1)
    #     elif i < 22:
    #         if i== 19+2:
    #             driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[{i - 14}]/a').click()
    #             time.sleep(2)
    #             for j in range(5, 715, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{715 - j}]').click()
    #                 time.sleep(3)
    #                 saveData(driver)
    #                 time.sleep(2)
    #         else:
    #             driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[{i - 14}]/a').click()
    #             time.sleep(1.5)
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH, f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(3)
    #                 saveData(driver)
    #                 time.sleep(2)
    #     elif i < 29:
    #         if i == 26:
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[4]/td[{i - 21}]/a').click()
    #             time.sleep(3)
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(3)
    #                 saveData(driver)
    #             time.sleep(2)
    #         else:
    #             driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[4]/td[{i - 21}]/a').click()
    #             time.sleep(2)
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(3)
    #                 saveData(driver)
    #                 time.sleep(2)
    #     else:
    #         driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #         DD_button = driver.find_element(By.XPATH,
    #                                         f'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[{i - 28}]/a').click()
    #         time.sleep(2)
    #         for j in range(5, 720, 5):
    #             specific_time_button = driver.find_element(By.XPATH, f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #             time.sleep(3)
    #             saveData(driver)
    #             time.sleep(1)
    # time.sleep(1)

    # month_11()
    # 11월달 나올 때까지 이전달 버튼 누르기
    # while True:
    #     current_month_year = driver.find_element(By.CLASS_NAME, 'ui-datepicker-title').text
    #     if "2024년 11월" in current_month_year:
    #         break
    #     driver.find_element(By.CLASS_NAME, prev_month_button_xpath).click()
    #     time.sleep(1.3)
    #     print('press prev month')
    # print("Reached September 2024")
    #
    # # Day 버튼
    # for i in range(5 + 16, 5 + 31):
    #     if i < 8:
    #         if i == 5 + 1:
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
    #             time.sleep(1)
    #             # 데이터 다운
    #             driver.find_element(By.XPATH, time_button_xpath).click()
    #             time.sleep(1)
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(3)
    #                 saveData(driver)
    #             time.sleep(1)
    #         else:
    #             driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(1.3)
    #                 saveData(driver)
    #             time.sleep(1.3)
    #     elif i < 15:
    #         if i == 5 + 8:
    #             driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i - 7}]/a').click()
    #             time.sleep(2)
    #             for j in range(5, 715, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{715 - j}]').click()
    #                 time.sleep(2)
    #                 saveData(driver)
    #             time.sleep(1)
    #         else:
    #             driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i - 7}]/a').click()
    #             time.sleep(2)
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(2)
    #                 saveData(driver)
    #             time.sleep(1)
    #     elif i < 22:
    #         if i == 5 + 16:
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[{i - 14}]/a').click()
    #             time.sleep(1.5)
    #             for j in range(5, 715, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{715 - j}]').click()
    #                 time.sleep(3)
    #                 saveData(driver)
    #                 time.sleep(2)
    #         else:
    #             driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #             DD_button = driver.find_element(By.XPATH,
    #                                             f'//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[{i - 14}]/a').click()
    #             time.sleep(1.5)
    #             for j in range(5, 720, 5):
    #                 specific_time_button = driver.find_element(By.XPATH,
    #                                                            f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #                 time.sleep(3)
    #                 saveData(driver)
    #                 time.sleep(2)
    #     elif i < 29:
    #         driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #         DD_button = driver.find_element(By.XPATH,
    #                                         f'//*[@id="ui-datepicker-div"]/table/tbody/tr[4]/td[{i - 21}]/a').click()
    #         time.sleep(2)
    #         for j in range(5, 720, 5):
    #             specific_time_button = driver.find_element(By.XPATH,
    #                                                        f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #             time.sleep(3)
    #             saveData(driver)
    #             time.sleep(2)
    #     else:
    #         driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
    #         DD_button = driver.find_element(By.XPATH,
    #                                         f'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[{i - 28}]/a').click()
    #         time.sleep(2)
    #         for j in range(5, 720, 5):
    #             specific_time_button = driver.find_element(By.XPATH, f'//*[@id="searchTime"]/option[{720 - j}]').click()
    #             time.sleep(3)
    #             saveData(driver)
    #             time.sleep(1)
    # time.sleep(1)
    print("Finish downloading")


except Exception as e:
    print(f"An error occurred: {e}")


input("Enter")
driver.quit()