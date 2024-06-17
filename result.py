from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import Select
import urllib
from pytesseract import image_to_string
import pytesseract
import time
import os, csv

# Specify the path to chromedriver.exe
chromedriver_path = 'D:\\BrowserDrivers\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'
# setup tesseract path 
tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# setup driver
chrome_service = Service(executable_path=chromedriver_path)
chrome_options = Options()

chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize Chrome WebDriver with explicit executable_path
# driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options, service=chrome_service)

driver = webdriver.Chrome(options=chrome_options, service=chrome_service)

website = 'https://www.jecjabalpur.ac.in/exam/programselect.aspx?id=%$'

class Scraping_Result : 
    def student_details(self, id, filename):
        driver.get(website)
        # select B.Tech
        driver.find_element(By.XPATH, '//*[@id="radlstProgram_1"]').click()

        try : 
            driver.find_element(By.XPATH, '//*[@id="txtrollno"]').send_keys(id)
        except :
            return False
        
        try : 
            drop_down = driver.find_element(By.XPATH, '//*[@id="drpSemester"]')
            dd = Select(drop_down)
            dd.select_by_index(5)
        #    time.sleep(3)
        except :
            return False

        time.sleep(1)
        # captcha reading 
        image_link = driver.find_element(By.XPATH, '//*[@id="pnlCaptcha"]/table/tbody/tr[1]/td/div/img').get_dom_attribute('src')
        
        captcha_link = 'https://www.jecjabalpur.ac.in/'+image_link
#        print(captcha_link)
        # get the captcha to text
        # Retrieve the image data from the URL
        img_file = id+'.png'
        response = urllib.request.urlopen(captcha_link)
        data = response.read()

        # Write the image data to a file
        with open(img_file, 'wb') as f:
            f.write(data)

        text = image_to_string(img_file)

#        print(text)
        captcha_val = self.structure_captcha(text)
#        print(captcha_val)
        os.remove(img_file)

        # send captcha 
        try :
            driver.find_element(By.XPATH, '//*[@id="TextBox1"]').send_keys(captcha_val)
        #    time.sleep(3)
        except :
            return False 

        time.sleep(1.5)
        # view result
        try : 
            driver.find_element(By.XPATH, '//*[@id="btnviewresult"]').click()
        except :
            return False

        time.sleep(1) 

        # Alert Handling 
        if self.is_alert_present(driver):
        #    print("Alert is present")
            # You can handle the alert here, e.g., accept it
            alert = driver.switch_to.alert
            alert_text = alert.text
            print("Alert Text : ", alert_text)
            alert.accept()
            
            if "you have entered a wrong text" in alert_text:
                return False
            else :
                return True

        
        time.sleep(1)
        # fetch details
        name = ''
        sgpa = ''
        verdict = ''
        branch = ''
        try : 
            name = driver.find_element(By.XPATH, '//*[@id="lblNameGrading"]').text
            sgpa = driver.find_element(By.XPATH, '//*[@id="lblSGPA"]').text
            verdict = driver.find_element(By.XPATH, '//*[@id="lblResultNewGrading"]').text
            branch = driver.find_element(By.XPATH, '//*[@id="lblBranchGrading"]').text
        except :
            return False

        print(f"{id} ,{name}, {branch}, {sgpa}, {verdict}")
        if name != '':
            filename 
            with open(filename, 'a', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([branch, id, name, sgpa, verdict])
                return True 
            
        return False


    # to handle captcha
    def structure_captcha(self, s):
        s = s[:-1].upper().replace(" ", '')
        s = s.replace("\n","")
        return s[:5]
    
    def is_alert_present(self, driver):
        try:
            alert = driver.switch_to.alert
        #   print("Alert Text : ", alert.text)
            return True
        except NoAlertPresentException:
            return False



result = Scraping_Result()
branch = ['CS', 'IT', 'AI', 'EC', 'CE', 'IP', 'ME', 'MT', 'EE']
upper_range = [110, 110, 70, 110, 70, 70, 70, 70, 110]

length = len(branch)
print(length)

for j in range(0, length):

    filename = branch[j]+'_6sem.csv'
    for i in range(1, upper_range[j]):
        id = '0201'+branch[j]+'211'
        if (i < 10):
           id = id+'00'+str(i)
        elif (i>9 and i<100) :
           id = id+'0'+str(i)
        else:
           id = id+str(i)

        for i in range(5):
            bool = result.student_details(id, filename)
            if bool == True:
               break 


driver.quit()