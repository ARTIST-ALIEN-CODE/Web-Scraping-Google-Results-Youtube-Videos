# Using selenium to scrape Youtube videos
# Some websites won't load by using the requests module and we need also to scroll down to get all the content to load.
# It helps us to automate the browser that is installed in our machine using their specific software like chromedriver.exe.
# for more info check there documentation https://selenium-python.readthedocs.io/


# In my code, I use chrome browser and I used a headless browsing method.
# headless means you will not see the GUI of chrome but it's working on the background.
# This method is much faster.

# Tip: Always update the keywords elements that I used to extract data from HTML and the driver.
# For a better understanding of my code, you should know how a website works, HTML, and python.


# Install selenium
# pip install selenium

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def func_Scrape_youtube(By_Youtube_Channel=None, By_Search_Keyword=None, Number_Scroll_Down=10):

    # Selenium Settings

    User_Agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    Chrome_Argument_keyword1 = 'user-agent='
    Chrome_Argument_keyword2 = "--window-size=1920,1080"
    Chrome_Argument_keyword3 = "--ignore-certificate-errors"
    Chrome_Argument_keyword4 = "--allow-running-insecure-content"
    Chrome_Argument_keyword5 = "--disable-extensions"
    Chrome_Argument_keyword6 = "--proxy-server='direct://'"
    Chrome_Argument_keyword7 = "--proxy-bypass-list=*"
    Chrome_Argument_keyword8 = "--start-maximized"
    Chrome_Argument_keyword9 = "--disabled-gpu"
    Chrome_Argument_keyword10 = "--disabled-dev-shm-usage"
    Chrome_Argument_keyword11 = "--no-sandbox"

    Options = webdriver.ChromeOptions()
    Options.add_argument('--headless')
    Options.add_argument(f'{Chrome_Argument_keyword1}{User_Agent}')
    Options.add_argument(Chrome_Argument_keyword2)
    Options.add_argument(Chrome_Argument_keyword3)
    Options.add_argument(Chrome_Argument_keyword4)
    Options.add_argument(Chrome_Argument_keyword5)
    Options.add_argument(Chrome_Argument_keyword6)
    Options.add_argument(Chrome_Argument_keyword7)
    Options.add_argument(Chrome_Argument_keyword8)
    Options.add_argument(Chrome_Argument_keyword9)
    Options.add_argument(Chrome_Argument_keyword10)
    Options.add_argument(Chrome_Argument_keyword11)

    # Include the path of the driver.
    # Take note chrome driver must match the version of the chrome browser your using on your machine.
    # You can download a driver here https://chromedriver.chromium.org/
    # The driver helps us control the browser via code executions.

    Exe_Driver = Service('./chromedriver')

    Driver = webdriver.Chrome(service=Exe_Driver, options=Options)


    # for a specific channel.

    if By_Youtube_Channel != None and not By_Youtube_Channel == "" and not By_Youtube_Channel.isspace():

        # Go to the Url based on the channel.
        Driver.get(f'https://www.youtube.com/{By_Youtube_Channel}/videos')

        # Pause to load the content.
        time.sleep(5)

        # Check the screenshot if successfully enter the URL.
        Driver.save_screenshot("Enter_Url_Screenshot.png")

        # Scroll down function.
        func_Scroll_down(Driver=Driver, Scroll_Limit=Number_Scroll_Down)

        # Check screenshot if successful scroll Down to the last content
        Driver.save_screenshot("Scroll_Down_Screenshot.png")

        # Create a list
        Youtube_Content_List = []

        try:
            # Now get the key elements from the HTML data.

            # Tip: creating a web scraping script is like a ticking bomb because anytime the website owner can change its HTML
            # elements so the current keys will not be correct then you have to change it.

            # Now open a browser and input the Url
            # Ctrl-shift-i to enter  the developer tools now find the elements that contain the info.

            # Each Youtube Video is inside an <div> element with a class id = "details" so all the Youtube Videos are inside of this <div> element.

            # Element div that contains Youtube info.
            Key_Element_Container = 'div#details'


            # Element that contains Link & Title.
            Key_Element_Video_Title_Link = 'a#video-title-link'

            # Element that contain Views.
            Key_Element_Views = './/*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][1]'

            # Element that contain Date & Time.
            Key_Element_Date_Time = './/*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][2]'

            # Use for loop to load Each Youtube details inside the div element
            # and wait for 30 milliseconds.
            for Each_Element in WebDriverWait(Driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, Key_Element_Container))):

                # Get details in every div element
                Get_Video_Title = Each_Element.find_element(By.CSS_SELECTOR,Key_Element_Video_Title_Link).get_attribute('title')
                Get_Video_Url = Each_Element.find_element(By.CSS_SELECTOR,Key_Element_Video_Title_Link).get_attribute('href')
                Get_Video_Views = Each_Element.find_element(By.XPATH,Key_Element_Views).text
                Get_Video_Date_Time = Each_Element.find_element(By.XPATH,Key_Element_Date_Time).text

                # Append data on the list
                Youtube_Content_List.append({
                    'Youtube_Video_Title': Get_Video_Title,
                    'Youtube_Video_Url': Get_Video_Url,
                    'Youtube_Video_Date_Time': Get_Video_Date_Time,
                    'Youtube_Video_views': Get_Video_Views
                })


        except:
            print("Some content has not found please wait......")


        if len(Youtube_Content_List) == 0:
            print(Youtube_Content_List)
            print("Check Element Keywords is correct")
            Driver.save_screenshot("Last_View_Screenshot.png")
            Driver.quit()
            return None

        Driver.save_screenshot("Last_View_Screenshot.png")
        Driver.quit()
        return Youtube_Content_List


    # Based on search keyword.

    elif By_Search_Keyword != None and not By_Search_Keyword == "" and not By_Search_Keyword.isspace():

        Driver.get(f'https://www.youtube.com/results?search_query={By_Search_Keyword}')


        # Pause to load the content.
        time.sleep(5)

        # Check the screenshot if successfully enter the URL.
        Driver.save_screenshot("Enter_Url_Screenshot.png")

        # Scroll down function
        # We limit the scroll down here but you can change this to none if you want.
        func_Scroll_down(Driver=Driver, Scroll_Limit=Number_Scroll_Down)


        # Check screenshot if successful scroll Down to the last content.
        Driver.save_screenshot("Scroll_Down_Screenshot.png")

        Youtube_Content_List = []

        try:
            # Now get the key elements from the HTML data.

            # Tip: creating a web scraping script is like a ticking bomb because anytime the website owner can change its HTML
            # elements so the current keys will not be correct then you have to change it.

            # Now open a browser and input the Url
            # Ctrl-shift-i to enter  the developer tools now find the elements that contain the info.

            # Each Youtube Video is inside an <div> element with a class id = "dismissible" so all the Youtube Videos are inside of this <div> element.

            # Element div that contains Youtube info.

            Key_Element_Container = 'div#dismissible'

            # Element that contains Link & Title
            Key_Element_Video_Title_Link = 'a#video-title'

            # Element that contain Views
            Key_Element_Views = './/*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][1]'

            # Element that contain Date & Time
            Key_Element_Date_Time = './/*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][2]'

            # Use for loop to load Each Youtube details inside the div element
            # and wait for 30 milliseconds.
            for Each_Element in WebDriverWait(Driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, Key_Element_Container))):

                # Get details in every div element
                Get_Video_Title = Each_Element.find_element(By.CSS_SELECTOR,Key_Element_Video_Title_Link).get_attribute('title')
                Get_Video_Url = Each_Element.find_element(By.CSS_SELECTOR,Key_Element_Video_Title_Link).get_attribute('href')

                Get_Video_Views = Each_Element.find_element(By.XPATH,Key_Element_Views).text
                Get_Video_Date_Time = Each_Element.find_element(By.XPATH,Key_Element_Date_Time).text

                #append it on the list
                Youtube_Content_List.append({
                    'Youtube_Video_Title': Get_Video_Title,
                    'Youtube_Video_Url': Get_Video_Url,
                    'Youtube_Video_Date_Time': Get_Video_Date_Time,
                    'Youtube_Video_views': Get_Video_Views
                })


        except:
            print("Some content has not found please wait......")


        if len(Youtube_Content_List) == 0:
            print(Youtube_Content_List)
            print("Check Element Keywords is correct")
            Driver.save_screenshot("Last_View_Screenshot.png")
            Driver.quit()
            return None

        Driver.save_screenshot("Last_View_Screenshot.png")
        Driver.quit()
        return Youtube_Content_List

    else:
        print("Missing arguments value")
        return None




# Scroll Down the until all videos load or add Specific number of Scroll down
# I suggest put a limit for search videos because it will longer than the specific channel videos

def func_Scroll_down(Driver = None, Scroll_Limit = 0):

    # Get over all height content based on the current URL

    Overall_Height_Content = Driver.execute_script("return document.documentElement.scrollHeight")

    if Scroll_Limit == 0:

        Keep_Scrolling = True

        while Keep_Scrolling:

            # To move the content upward get the current screen height position then minus the overall heigh
            Driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

            # Pause to load the content
            time.sleep(4)

            # Get Over all height Again
            New_Overall_Height_Content = Driver.execute_script("return document.documentElement.scrollHeight")

            # Check the new overall height and last height if same
            if New_Overall_Height_Content == Overall_Height_Content:
                Keep_Scrolling = False

            # Change Overall_Height_Content to New_Overall_Height_Content
            Overall_Height_Content = New_Overall_Height_Content

    else:

        Number_Scroll_Down = 0

        while Number_Scroll_Down <= Scroll_Limit:

            # To move the content upward get the current screen height position then minus the overall height
            Driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

            # Pause to load the content
            time.sleep(4)

            Number_Scroll_Down += 1


if __name__ == "__main__":
    Youtube_List = func_Scrape_youtube(By_Youtube_Channel=None, By_Search_Keyword=None, Number_Scroll_Down=5)

    # print the list if not empty or none
    if Youtube_List != None and len(Youtube_List) != 0:
        for Each_Youtube_Detail in Youtube_List:
            print(Each_Youtube_Detail)
        print(f"Number of items : {len(Youtube_List)}")
