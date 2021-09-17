from bs4 import BeautifulSoup                               #Beautiful Soup is a Python package capable of parsing HTML and XML documents, including those with malformed markup ("tag soup") 
import requests                                             #The requests library allows sending HTTP requests via Python simply
import pandas as pd                                         #Pandas library allows us to process and analyse extensive data with ease, using special data structures and functions

pagesToGet= 10                                              #This denotes the number of pages to be scanned, can be increased and decreased as per requirement

upperframe=[]                                               #Initialises a list to save the entire data of the website

for page in range(1,pagesToGet+1):                                              #Basic loop to cycle through the pages
    print('processing page :', page)                                            
    url = 'https://www.theguardian.com/world?page='+str(page)                   #Saves the URL of current page
    print(url)                                                                  
    page=requests.get(url)                                                      #Sends a request for the HTTP content of the current URL and saves it
    sp1=BeautifulSoup(page.text,'html.parser')                                  #Initialises a BeautifulSoup object to parse the HTML content saved from the URL
    frame=[]                                                                    #Intialises a blank list to stare the data of the current page
    links=sp1.find_all('div',attrs={'class':'fc-item__container'})             #Finds and stores all instances of the specified tag-attributes combination containing the article links
    print(len(links))                                                           #Prints the number of articles found on the page
    for j in links:             
        title = j.find("a").text.strip()                                        #Saves the title
        Link = j.find('a')['href'].strip()                                      #Saves the link
        ptemp = requests.get(Link)                                              #Requests the article page
        sp2 = BeautifulSoup(ptemp.text,'html.parser')                           #Initialises a second BeautifulSoup object to parse the article page
        text = ''                                                               #Initialises a blank string to store the article text
        kinks = sp2.find_all('p',attrs={'class':'dcr-s23rjr'})                  #Finds all tags containing the text
        for k in kinks:
            text += k.text.strip()                                              #Add the text from the current section to the blank string
        frame.append((title,text,Link))                                         #Add a tuple with the title, text and the link of the current article to the list
    upperframe.extend(frame)                                                    #Appends the list of the current page to the list of the whole website
data=pd.DataFrame(upperframe, columns=['text','title','Link'])                  #Initialises a Pandas dataframe with the final collected list
nan_value = float("NaN")
data.replace("", nan_value, inplace=True)                                       #Replace "" with NaN in the text for pages with no news paragraphs
data.dropna(subset = ["text"], inplace=True)                                    #Drop pages with no text
data.to_csv('OPI.csv')                                                          #Convert the dataframe to a CSV file
print(data.head())                                                              #Print the first 5 rows of the dataframe                                                     #Print the first 5 rows of the dataframe
