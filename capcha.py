import time, requests, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'
filefolder = '/tmp/'
filename = '1.mp3'
delayTime = 2
audioToTextDelay = 10

def audioToText(mp3Path,driver):
    print("1")
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    print("2")
    driver.get(googleIBMLink)
    delayTime = 10
    # Upload file
    time.sleep(1)
    print("3")
    # Upload file
    time.sleep(1)
    root = driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(mp3Path)
    # Audio to text is processing
    time.sleep(delayTime)
    #btn.send_keys(path)
    print("4")
    # Audio to text is processing
    time.sleep(audioToTextDelay)
    print("5")
    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div').find_elements_by_tag_name('span')
    print("5.1")
    result = " ".join( [ each.text for each in text ] )
    print("6")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("7")
    return result

def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)

def start_cap(driver):
    print('start cap')
    url = driver.current_url
    driver.switch_to_frame('main-iframe')
    googleClass = driver.find_elements_by_class_name('g-recaptcha')[0]
    time.sleep(2)
    outeriframe = googleClass.find_element_by_tag_name('iframe')
    time.sleep(1)
    url = driver.current_url
    outeriframe.click()
    time.sleep(2)
    if driver.current_url == url:
        allIframesLen = driver.find_elements_by_tag_name('iframe')
        time.sleep(1)
        audioBtnFound = False
        audioBtnIndex = -1
        for index in range(len(allIframesLen)):
            driver.switch_to.default_content()
            driver.switch_to_frame('main-iframe')
            iframe = driver.find_elements_by_tag_name('iframe')[index]
            driver.switch_to.frame(iframe)
            driver.implicitly_wait(delayTime)
            try:
                audioBtn = driver.find_element_by_id('recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
                audioBtn.click()
                audioBtnFound = True
                audioBtnIndex = index
            except Exception as e:
                pass

            if audioBtnFound:
                try:
                    while True:
                        href = driver.find_element_by_id('audio-source').get_attribute('src')
                        response = requests.get(href, stream=True)
                        saveFile(response,os.path.join(filefolder,filename))
                        response = audioToText(os.path.join(filefolder,filename),driver)
                        driver.switch_to.default_content()
                        driver.switch_to_frame('main-iframe')
                        iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
                        driver.switch_to.frame(iframe)
                        inputbtn = driver.find_element_by_id('audio-response')
                        inputbtn.send_keys(response)
                        time.sleep(1)
                        inputbtn.send_keys(Keys.ENTER)
                        time.sleep(3)
                        main_page = driver.window_handles[0]  
                        driver.switch_to.window(main_page)
                        new_url = driver.current_url
                        if url != new_url:
                            print("Success")
                            return driver
                            break
                except Exception as e:
                    print(e)
                    print('Caught. Need to change proxy now')
                    return False
