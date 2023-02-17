# Goal: get the Titles and Links from google results...
# For a better understanding of my code, you should know how a website works, HTML, and python.

# Install these modules...

# pip install requests
# pip install beautifulsoup4

# The requests module will be used to send a request to google and get an HTML response.
# The beautifulsoup4 will filter the data from the HTML response.

# Import both modules.
import requests
from bs4 import BeautifulSoup


# Create a function.
def func_Scrape_google_result(Search_Keyword=None):
    # Set a variable for google URL.
    Google_Url = "https://www.google.com/search?q="


    # Set these settings for the requests module.
    # Check this documentation for more info https://requests.readthedocs.io/en/latest/

    # We need a user agent so that we disguise ourselves as a browser so that google will not block us.
    User_Agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'

    # Set the Language.
    Language = "en-US,en;q=0.5"

    # Set the Key names.
    Headers_Keyword_User_Agent = 'User-Agent'
    Headers_Keyword_Accept_Language = 'Accept-Language'
    Headers_Keyword_Content_Language = 'Content-Language'



    # Check arguments.

    if Search_Keyword == None or Search_Keyword.isspace() or Search_Keyword== "" :
        print("Missing arguments value Search_Keyword")
        return None


    # Set the full URL.
    Url = f"{Google_Url}{Search_Keyword}"  # output : https://www.google.com/search?q=Article for dogs 2023


    try:
        # Create an object.
        Session = requests.Session()
        # Set the settings to a dictionary format based on the documentation. https://requests.readthedocs.io/en/latest/

        Session.headers[Headers_Keyword_User_Agent] = User_Agent
        Session.headers[Headers_Keyword_Accept_Language] = Language
        Session.headers[Headers_Keyword_Content_Language] = Language

        #  We put text because it will just return a response<200> to view that we used text.
        Response = Session.get(Url).text
    except:
        Response = None
        print("Check the Requests module codes if you used them correctly or updated them.")


    if Response == None:
        return None

    else:
        # After getting the HTML content we parse and scrape it with a beautifulsoup module.
        # The word parsing means to divide something into its components and then describe its syntactic roles..
        # For more info https://www.geeksforgeeks.org/html-parsing-and-processing/
        try:
            Beautiful_Soup_Keyword_Parser = "html.parser"
            Data_Soup = BeautifulSoup(Response, Beautiful_Soup_Keyword_Parser)
        except:
            print("Check if Beautifulsoup codes are used correctly or updated.")
            Data_Soup = None

        if Data_Soup == None:
            return None
        else:
            try:
                # Now get the key elements from the HTML data to filter and extract the exact data.

                # Tip: creating a web scraping script is like a ticking bomb because anytime the website owner can change its HTML
                # elements so the current keys will not be correct then you have to change it.

                # Now open a browser and input the Url = https://www.google.com/search?q=Article for dogs 2023
                # Ctrl-shift-i to enter  the developer tools now find the elements that contain the info which are the Title and the Link.

                # Each Article is inside an <div> element with a class name = "yuRUbf" so all the articles are inside of this <div> element.
                Key_Element_Container = 'div'
                Key_Div_Attr = 'class'
                Key_Div_Class_Name = 'yuRUbf'

                # Get all the <div> that contains the Link & Title.
                # Find the element and the Extract data using beautiful soup check documentation : https://www.crummy.com/software/BeautifulSoup/bs4/doc/
                Articles_Link_Text_List = Data_Soup.find_all(Key_Element_Container, attrs={Key_Div_Attr: Key_Div_Class_Name})

                # output : Articles_Link_Text_List = [<div>content</div>,<div>content</div>..........]

                # Each <div> element contains the Link which is inside a element <a> & The Header title inside the element <h3>.

                Key_Element_Link = 'a'
                Key_Element_Header = 'h3'


                # Now extract the text and link.
                # Create a list container.
                Article_List = [] # output : Article_List = [[Article_Title,Article_Link],[Article_Title,Article_Link]..........]

                for Each_Article in Articles_Link_Text_List:
                    # Find the element 'h3' and extract the title which is text.
                    Article_Title = Each_Article.find(Key_Element_Header).text

                    # Find the element 'a'.
                    Article_Link_Element = Each_Article.find(Key_Element_Link, href=True)
                    # Extract the href in the element.
                    Article_Link = Article_Link_Element['href']

                    # Add it to the list.
                    Article_List.append([Article_Title,Article_Link])

                # Check if you extract something
                if len(Article_List) == 0:
                    print("Check Key Elements if updated")
                    return None

                return Article_List
            except:
                print("Check if Beautifulsoup codes are used correctly or updated.")
                return None




if __name__ == '__main__':
    Article_List = func_Scrape_google_result(Search_Keyword='Articles about Dogs 2023')

    # print the list if not empty or none
    if Article_List != None and len(Article_List) != 0:
        for Each_Article in Article_List:
            print(Each_Article)

        print(f"Number of items : {len(Article_List)}")




