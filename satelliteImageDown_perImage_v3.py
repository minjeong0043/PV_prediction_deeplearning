import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import smtplib
from email.mime.text import MIMEText
import threading
# driver = webdriver.Chrome()

def saveData(driver):
    save_button = driver.find_element(By.XPATH, '//*[@id="content"]/section/div[2]/div/div[2]/button[5]/i').click()
    time.sleep(0.1)
    original_img_button = driver.find_element(By.XPATH, '//*[@id="download-confirm"]/ul/li[1]/button/em').click()
    time.sleep(0.1)
    savePage_close_button = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/button').click()

# Send an image when error is occured
def timeout_handler():
    send_error_email('코드가 멈췄습니다. 확인이 필요합니다.')

def send_finishing_email(message):
    smtp_host = 'smtp.naver.com'  # SMTP 서버 주소
    smtp_port = 587
    sender_email = 'kmjmj04031@naver.com'
    sender_password = '6837GEXHUG2K'
    receiver_email = '0043kmj@korea.ac.kr'

    # content of email
    msg = MIMEText(f'{message}')
    msg['Subject'] = 'Python 코드 완료 알림'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # SMTP 서버 연결 및 전송
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("에러 이메일 전송 완료")
    except Exception as e:
        print('이메일 전송 실패 :', e)

def send_error_email(error_message):
    smtp_host = 'smtp.naver.com' # SMTP 서버 주소
    smtp_port = 587
    sender_email = 'kmjmj04031@naver.com'
    sender_password = '6837GEXHUG2K'
    receiver_email = '0043kmj@korea.ac.kr'

    # content of email
    msg = MIMEText(f'파이썬 코드에서 에러가 발생했습니다:\n\n{error_message}')
    msg['Subject'] = 'Python 코드 에러 알림'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # SMTP 서버 연결 및 전송
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("에러 이메일 전송 완료")
    except Exception as e:
        print('이메일 전송 실패 :', e)

threadingTime = 40
try:
    # Set download path
    download_path = r"D:\SatelliteImageDownload(10.5color)\2021_7"
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': download_path,
             'download.prompt_for_download': False,
             'directory_upgrade': True,
             'safebrowsing.enabled': True}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)

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

    # Set time sleep time
    timeSleep_after_dayButton = 1.5
    timeSleep_after_timeButton = 0.3
    timeSleep_after_selectTime = 1.4
    timeSleep_after_saveData = 0.1
    timeSleep_after_allSaveDataPerDay = 0.2
    threadingTime = 10
    try:
        # input("Press enter when you set information!! (자료 종류, 영역 .etc)")
        # 자료 종류 10.5um로 설정
        time.sleep(1)
        select_elem = driver.find_element(By.XPATH, '//select[@name="type"]')
        select = Select(select_elem)
        select.select_by_value("ENHC-COLOR-IR105")

        driver.find_element(By.XPATH, YYYYMMDD_xpath).click()

        # month_9()
        # 9월달 나올 때까지 이전달 버튼 누르기
        while True:
            current_month_year = driver.find_element(By.CLASS_NAME, 'ui-datepicker-title').text
            if "2021년 7월" in current_month_year:
                break
            driver.find_element(By.CLASS_NAME, prev_month_button_xpath).click()
            time.sleep(0.16)
            print('press prev month')
        print("Reached September 2021.7")

        # Day 버튼
        # for i in range(30,31):
        Blacknum = 4
        startnum = 10

        print(f'Start Day : {startnum}')
        # searchTime select 박스 내 모든 option 요소를 찾기
        options = driver.find_elements(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody')
        option_count = len(options)  # 마지막 index는 option_count
        print(f"Day 총 개수 (마지막 인덱스): {option_count}")
        for i in range(Blacknum+startnum, Blacknum+1+31):
            if i < 8:
                if i == 1:
                    DD_button = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                    time.sleep(timeSleep_after_dayButton)
                    # 데이터 다운
                    driver.find_element(By.XPATH, time_button_xpath).click()
                    time.sleep(timeSleep_after_timeButton)
                    # searchTime select 박스 내 모든 option 요소를 찾기
                    options = driver.find_elements(By.XPATH, '//*[@id="searchTime"]/option')
                    option_count = len(options)  # 마지막 index는 option_count
                    print(f"option의 총 개수 (마지막 인덱스): {option_count}")

                    for j in range(0, option_count):
                        timer = threading.Timer(threadingTime, timeout_handler)
                        timer.start()
                        specific_time_button = driver.find_element(By.XPATH,
                                                                   f'//*[@id="searchTime"]/option[{option_count - j}]').click()
                        time.sleep(timeSleep_after_selectTime)
                        saveData(driver)
                        time.sleep(timeSleep_after_saveData)
                        timer.cancel()
                    time.sleep(timeSleep_after_allSaveDataPerDay)
                else:
                    driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
                    DD_button = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[{i}]/a').click()
                    time.sleep(timeSleep_after_dayButton)
                    # searchTime select 박스 내 모든 option 요소를 찾기
                    options = driver.find_elements(By.XPATH, '//*[@id="searchTime"]/option')
                    option_count = len(options)  # 마지막 index는 option_count
                    print(f"option의 총 개수 (마지막 인덱스): {option_count}")

                    for j in range(0, option_count):
                        timer = threading.Timer(threadingTime, timeout_handler)
                        timer.start()
                        specific_time_button = driver.find_element(By.XPATH,
                                                                   f'//*[@id="searchTime"]/option[{option_count - j}]').click()
                        time.sleep(timeSleep_after_selectTime)
                        saveData(driver)
                        time.sleep(timeSleep_after_saveData)
                        timer.cancel()
                    time.sleep(timeSleep_after_allSaveDataPerDay)
            elif i < 15:
                if i == 14:
                    DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i - 7}]/a').click()
                    time.sleep(timeSleep_after_dayButton)
                    # searchTime select 박스 내 모든 option 요소를 찾기
                    options = driver.find_elements(By.XPATH, '//*[@id="searchTime"]/option')
                    option_count = len(options)  # 마지막 index는 option_count
                    print(f"option의 총 개수 (마지막 인덱스): {option_count}")

                    for j in range(0,option_count):
                        timer = threading.Timer(threadingTime, timeout_handler)
                        timer.start()
                        specific_time_button = driver.find_element(By.XPATH,f'//*[@id="searchTime"]/option[{option_count - j}]').click()
                        time.sleep(timeSleep_after_selectTime)
                        saveData(driver)
                        time.sleep(timeSleep_after_saveData)
                        timer.cancel()
                    time.sleep(timeSleep_after_allSaveDataPerDay)
                else:
                    driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
                    DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[{i - 7}]/a').click()
                    time.sleep(timeSleep_after_dayButton)
                    # searchTime select 박스 내 모든 option 요소를 찾기
                    options = driver.find_elements(By.XPATH, '//*[@id="searchTime"]/option')
                    option_count = len(options)  # 마지막 index는 option_count
                    print(f"option의 총 개수 (마지막 인덱스): {option_count}")

                    for j in range(0, option_count):
                        timer = threading.Timer(threadingTime, timeout_handler)
                        timer.start()
                        specific_time_button = driver.find_element(By.XPATH,
                                                                   f'//*[@id="searchTime"]/option[{option_count - j}]').click()
                        time.sleep(1.4)
                        saveData(driver)
                        time.sleep(timeSleep_after_saveData)
                        timer.cancel()
                    time.sleep(timeSleep_after_allSaveDataPerDay)
            elif i < 22:
                driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
                DD_button = driver.find_element(By.XPATH, f'//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[{i - 14}]/a').click()
                time.sleep(timeSleep_after_dayButton)
                # searchTime select 박스 내 모든 option 요소를 찾기
                options = driver.find_elements(By.XPATH, '//*[@id="searchTime"]/option')
                option_count = len(options)  # 마지막 index는 option_count
                print(f"option의 총 개수 (마지막 인덱스): {option_count}")

                for j in range(0, option_count):
                    timer = threading.Timer(threadingTime, timeout_handler)
                    timer.start()
                    specific_time_button = driver.find_element(By.XPATH,
                                                               f'//*[@id="searchTime"]/option[{option_count - j}]').click()
                    time.sleep(timeSleep_after_selectTime)
                    saveData(driver)
                    time.sleep(timeSleep_after_saveData)
                    timer.cancel()
                time.sleep(timeSleep_after_allSaveDataPerDay)
            elif i < 29:
                driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
                DD_button = driver.find_element(By.XPATH,
                                                f'//*[@id="ui-datepicker-div"]/table/tbody/tr[4]/td[{i - 21}]/a').click()
                time.sleep(timeSleep_after_dayButton)
                # searchTime select 박스 내 모든 option 요소를 찾기
                options = driver.find_elements(By.XPATH, '//*[@id="searchTime"]/option')
                option_count = len(options)  # 마지막 index는 option_count
                print(f"option의 총 개수 (마지막 인덱스): {option_count}")

                for j in range(0, option_count):
                    timer = threading.Timer(threadingTime, timeout_handler)
                    timer.start()
                    specific_time_button = driver.find_element(By.XPATH,
                                                               f'//*[@id="searchTime"]/option[{option_count - j}]').click()
                    time.sleep(timeSleep_after_selectTime)
                    saveData(driver)
                    time.sleep(timeSleep_after_saveData)
                    timer.cancel()
                time.sleep(timeSleep_after_allSaveDataPerDay)
            elif i < 36:
                driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
                DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[{i - 28}]/a').click()
                time.sleep(timeSleep_after_dayButton)
                # searchTime select 박스 내 모든 option 요소를 찾기
                options = driver.find_elements(By.XPATH, '//*[@id="searchTime"]/option')
                option_count = len(options)  # 마지막 index는 option_count
                print(f"option의 총 개수 (마지막 인덱스): {option_count}")

                for j in range(0, option_count):
                    timer = threading.Timer(threadingTime, timeout_handler)
                    timer.start()
                    specific_time_button = driver.find_element(By.XPATH,
                                                               f'//*[@id="searchTime"]/option[{option_count - j}]').click()
                    time.sleep(timeSleep_after_selectTime)
                    saveData(driver)
                    time.sleep(timeSleep_after_saveData)
                    timer.cancel()
                time.sleep(timeSleep_after_allSaveDataPerDay)
            else:
                driver.find_element(By.XPATH, YYYYMMDD_xpath).click()
                DD_button = driver.find_element(By.XPATH,f'//*[@id="ui-datepicker-div"]/table/tbody/tr[6]/td[{i - 35}]/a').click()
                time.sleep(timeSleep_after_dayButton)
                # searchTime select 박스 내 모든 option 요소를 찾기
                options = driver.find_elements(By.XPATH, '//*[@id="searchTime"]/option')
                option_count = len(options)  # 마지막 index는 option_count
                print(f"option의 총 개수 (마지막 인덱스): {option_count}")

                for j in range(0, option_count):
                    timer = threading.Timer(threadingTime, timeout_handler)
                    timer.start()
                    specific_time_button = driver.find_element(By.XPATH,
                                                               f'//*[@id="searchTime"]/option[{option_count - j}]').click()
                    time.sleep(timeSleep_after_selectTime)
                    saveData(driver)
                    time.sleep(timeSleep_after_saveData)
                    timer.cancel()
                time.sleep(timeSleep_after_allSaveDataPerDay)
        time.sleep(1)
        print("Finish downloading")
        send_finishing_email('Downloading Finished')
    except Exception as e:
        print(f"An error occurred: {e}")
        send_error_email(str(e))
        timer.cancel()

    input("Enter")
    driver.quit()
except Exception as err:
    send_error_email(str(err))

input('Enter')
timer.cancel()