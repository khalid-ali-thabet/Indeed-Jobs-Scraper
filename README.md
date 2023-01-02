# Indeed-Jobs-Scraper

# Language & libraries:
* Python programming language
* selenium : for automation 
* BeautifulSoup : to deal with the HTML of the web page
* Time : to wait some time until the HTML code fully loaded  
* smtplib, ssl : to send the file by email 
# Description:
This project's purposes is to scrape the jobs provided on Indeed.com website and make a CSV file, saving it in the local machine and finally send that file by email to whomever you want.

# input & output:
## input: through the code lines you will find a TODO comment telling you what to type, these TODOes are:
* job title to search about on indeed 
* the location/country you want
* the email address to send the data to 
* the passward of that email address
# csv file content:
### 'N/A': is the default value for every field if this particular information didn't provided
* title : the full title of the posted job
* compaany: company name 
* full or part: type of the job if it's full time or part time
* salary: the salary provided by the company's job post 
* location: the location of the company 
* link: the link to the job post 
* date: how many days passed since this job posted 

