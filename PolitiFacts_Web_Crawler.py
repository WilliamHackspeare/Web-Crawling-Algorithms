from bs4 import BeautifulSoup                               #Beautiful Soup is a Python package capable of parsing HTML and XML documents, including those with malformed markup ("tag soup") 
import requests                                             #The requests library allows sending HTTP requests via Python simply
import pandas as pd                                         #Pandas library allows us to process and analyse extensive data with ease, using special data structures and functions

pagesToGet= 10                                              #This denotes the number of pages to be scanned, can be increased and decreased as per requirement

upperframe=[]                                               #Initialises a list to save the entire data of the website

for page in range(1,pagesToGet+1):                                              #Basic loop to cycle through the pages
    print('processing page :', page)                                            
    url = 'https://www.politifact.com/factchecks/list/?page='+str(page)         #Saves the URL of current page
    print(url)                                                                  
    page=requests.get(url)                                                      #Sends a request for the HTTP content of the current URL and saves it
    sp1=BeautifulSoup(page.text,'html.parser')                                  #Initialises a BeautifulSoup object to parse the HTML content saved from the URL
    frame=[]                                                                    #Intialises a blank list to stare the data of the current page
    links=sp1.find_all('li',attrs={'class':'o-listicle__item'})                 #Finds and stores all instances of the specified tag-attributes combination containing the article links
    print(len(links))                                                           #Prints the number of articles found on the page
    for j in links:             
        Statement = j.find("div",attrs={'class':'m-statement__quote'}).text.strip()                     #Saves the title
        Link = "https://www.politifact.com"
        Link += j.find("div",attrs={'class':'m-statement__quote'}).find('a')['href'].strip()            #Saves the link
        Date = j.find('div',attrs={'class':'m-statement__body'}).find('footer').text[-14:-1].strip()    #Saves the date
        Source = j.find('div', attrs={'class':'m-statement__meta'}).find('a').text.strip()              #Saves the source
        Label = j.find('div', attrs ={'class':'m-statement__content'}).find('img',attrs={'class':'c-image__original'}).get('alt').strip()   #Saves the label
        frame.append((Statement,Link,Date,Source,Label))                                                #Add a tuple with the title, text and the link of the current article to the list
    upperframe.extend(frame)                                                                            #Appends the list of the current page to the list of the whole website
data=pd.DataFrame(upperframe, columns=['Statement','Link','Date','Source','Label'])                     #Initialises a Pandas dataframe with the final collected list
data.to_csv('NEWS.csv')                                                          #Convert the dataframe to a CSV file
print(data.head())                                                              #Print the first 5 rows of the dataframe
