from flask import Flask, request, redirect
from selenium import webdriver
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import urllib.request
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

app = Flask(__name__)

#start the WebDriver
canvas_driver = webdriver.Chrome()

@app.route('/login', methods=['POST','GET'])
def login():

    dict = {}

    if request.method == 'POST':
        #start at the Canvas Home Page
        canvas_driver.get("https://canvas.rutgers.edu/")

        #navigate to the 'NetID Login Button'
        canvas_driver.find_element_by_xpath("/html/body/header/div[1]/div/div[2]/div/div[1]/a").click()

        #request the username and password attributes from the Twilio SMSing service
        username = request.values.get('username')
        password = request.values.get('password')

        #allow the page to load and send in the username and password keys
        w = WebDriverWait(canvas_driver, 3).until(EC.visibility_of_element_located((By.XPATH,'/html/body/main/div/div[2]/div[1]/div[2]/form/section/div[1]/input')))
        canvas_driver.find_element_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/form/section/div[1]/input').send_keys(username)
        canvas_driver.find_element_by_xpath('/html/body/main/div/div[2]/div[1]/div[2]/form/section/section[1]/div/input').send_keys(password)

        #submit the form with the populated fields
        wait = WebDriverWait(canvas_driver, 3).until(EC.visibility_of_element_located((By.ID,'fm1')))
        canvas_driver.find_element_by_xpath('//*[@id="fm1"]/section/input[4]').click()
    else:
        #if the POST request succeeded, the driver should be able to navigate to the courses page
        canvas_driver.get('https://rutgers.instructure.com/courses')

        #get the number of courses to iterate through
        list = canvas_driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr')
        length = len(list)

        #get all the listed courses (this includes all courses - not just Spring 2021 semester!)
        canvas_driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[1]/div/table[1]/tbody/tr[1]').click()
        page = canvas_driver.page_source

        #Initiliaze BeautifulSoup parser
        soup = BeautifulSoup(page, "html.parser")
        courses = soup.find_all(class_='course-list-table-row')
        all_courses = []
        for c in range(0,length):
            all_courses.append(courses[c])

        #get the active classes by checking for the links to the respective course pages
        course_links = []
        course_names = []
        for d in all_courses:
            links = d.findAll('a')
            for a in links:
                course_links.append('https://rutgers.instructure.com' + a['href'] + '/assignments')
                course_names.append(a['title'])


        #Initiliaze the lists to keep class and assignment data in
        class_name = []
        due_date = []
        assignment_title = []

        #for all the classes in the list, get the respective assignments and add them to the final dict that is returned
        for i in range(0,len(course_links)):
            canvas_driver.get(course_links[i])
            try:
                w = WebDriverWait(canvas_driver, 1).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[3]/ul/li[1]/div/div[2]/ul/li/div/div/div[2]/a')))
                canvas_driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[3]/ul/li[1]/div/div[2]/ul/li/div/div/div[2]/a').click()
                date = canvas_driver.find_element_by_class_name('display_date')
                title = canvas_driver.find_element_by_class_name('title')
                time = canvas_driver.find_element_by_class_name('display_time')
                date_time = date.text + ' @ ' + time.text
                dict[course_names[i]] = 'Assignment ' + title.text + ' is due on ' + date_time
                class_name.append(course_names[i])
                due_date.append(date.text)
                assignment_title.append(title.text)
            except NoSuchElementException:
                continue
            except TimeoutException:
                continue


        print(class_name)
        print(due_date)
        print(assignment_title)
        print(dict)

    #return final dict
    return dict


@app.route('/logout', methods=['GET'])
def logout():

    #if the user is done using the service, the driver is closed and the cookies are deleted 
    canvas_driver.close()

    return 'success'


@app.route('/error', methods=['GET'])
def error():

    canvas_driver.close()
    return "success"



if __name__ == "__main__":
    app.run(debug=True)
