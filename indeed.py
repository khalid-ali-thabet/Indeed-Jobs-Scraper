from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd 
import time

driver = webdriver.Chrome('C:/chromedriver.exe')
driver.maximize_window()
driver.get('https://indeed.com')
time.sleep(1)

NAN = 'N/A'# for the values that didn't provided 

# function to find by xpath
def find_element_by_xpath(xpath):
    return driver.find_element(By.XPATH, xpath)


job_search = find_element_by_xpath('//*[@id="text-input-what"]')
#TODO: TYPE THE JOB TITLE
job_search.send_keys('job title')

location_search = find_element_by_xpath('//*[@id="text-input-where"]')
#TODO: TYPE THE COUNTRY 
location_search.send_keys('egypt')
location_search.send_keys(Keys.ENTER)

#find_button = find_element_by_xpath('//*[@id="jobsearch"]/button').click()

soup = BeautifulSoup(driver.page_source, 'lxml')

df = pd.DataFrame({'title':[''], 'compaany':[''], 'full or part':[''], 'salary':[''], 'location':[''], 'link':[''],'date':['']})

key_words = ['data entry', 'data', 'entry']

while True:
    soup = BeautifulSoup(driver.page_source, 'lxml')
    posts = soup.find_all('div', class_= 'slider_container css-g7s71f eu4oa1w0')
    for post in posts:
        try:
            title = post.find('h2', class_= 'jobTitle css-1h4a4n5 eu4oa1w0').text
        except:
            # if the job is new then its html class is different 
            title = post.find('h2', class_='jobTitle jobTitle-newJob css-bdjp2m eu4oa1w0').text
        
        try:
            company_name = post.find('span', class_='companyName').text
        except:
            company_name = NAN
        try:
            company_location = post.find('div', class_= 'companyLocation').text
        except:
            company_location =NAN
        # the problem with salary is that not every job post has a salary
        try:
            salary = post.find('div', class_= 'metadata salary-snippet-container').find('div').text
        except:
            salary = NAN
        
        try:
            job_type = post.find('div', class_='metadata').text
        except:
            job_type = NAN
        
        link = 'https://indeed.com'+post.find('a',class_='jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
        date = post.find('span', class_='date').text
        
        df = df.append({'title':title, 'compaany':company_name, 'full or part':job_type, 'salary':salary, 'location':company_location, 'link':link,'date':date}, ignore_index=True)
        
        # next page 
    try:
        # we need the current url to get the first half of it e.g  eg.indeed.com
        url = driver.current_url[:driver.current_url.find('.com')+4]
        nex = soup.find_all('a', {'data-testid':'pagination-page-next'})
        driver.get(url+nex[0].get('href'))
        time.sleep(3)
    except:
        break 

#######################################################################################
# filtering and sorting the data on the date column 

def numbers(string):
    '''
    inpit -> string i.e. 'posted 30+ days ago'
    output -> integer i.e. 30 
    '''
    new_str = ''
    for i in string:
        if i in '0123456789':
            new_str = new_str + i
    try:
        new_str = int(new_str)
    except:
        new_str = 0
    return new_str

# select the interested in columns and sort them on date column 
df['date (days ago)'] = df['date'].apply(numbers)
df = df[['title', 'compaany', 'full or part','salary','location','date (days ago)', 'link' ]]
df.sort_values(by= 'date (days ago)', inplace = True)

#TODO: TYPE THE LOCATION YOU WANT TO SAVE THE FILE IN   
df.to_csv('F:/new_jobs.csv')

######################################################################################

#Code below sends an email to whomever through python
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

#Input the email account that will send the email and who will receiving it
#TODO: TYPE EMAIL ADDRESS
sender = 'Your email address'
# i will send that email to myself so sender = reciver, but if you want you can type the reciver email 
receiver = sender

#Creates the Message, Subject line, From and To
msg = MIMEMultipart()
msg['Subject'] = 'New Jobs on Indeed'
msg['From'] = sender
msg['To'] = ','.join(receiver)

#Adds a csv file as an attachment to the email (indeed_jobs.csv is our attahced csv in this case)
part = MIMEBase('application', 'octet-stream')
part.set_payload(open('F:/new_jobs.csv', 'rb').read())
encoders.encode_base64(part)

#TODO: TYPE THE LOCATION OF THE FILE YOU WANT TO SEND  
part.add_header('Content-Disposition', 'attachment; filename ="F:/new_jobs.csv"')
msg.attach(part)

#Will login to your email and actually send the message above to the receiver
s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
#TODO: TYPE EMAIL AND PASSWORD OF THE SENDER  
s.login(user = 'your email address', password = 'your password')
s.sendmail(sender, receiver, msg.as_string())
s.quit()


# gmail problem solving link -> https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp















