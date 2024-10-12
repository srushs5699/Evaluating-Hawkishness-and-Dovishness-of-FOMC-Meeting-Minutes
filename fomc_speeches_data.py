
def create_url_list(start_year, end_year, prefix, suffix):
        # Generates a list of URLs for annual speech listings based on year range and URL components
    annual_htm_list = []
    for x in range(start_year, end_year+1):
        if x <=2010:
            this_suffix = 'speech.htm'
            mid_str=str(x)
            annual_htm_list.append(prefix + mid_str + this_suffix)
        else:
            mid_str = str(x)
            annual_htm_list.append(prefix + mid_str + suffix)
    return annual_htm_list

def find_speeches_by_year(host, this_url, print_test=False):
        # Fetches and parses speech details (dates, speakers, titles, links) from a given URL
    conn = HTTPSConnection(host = host)
    conn.request(method='GET', url = this_url)
    resp = conn.getresponse()
    body = resp.read()
    # check that we received the correct response code
    if resp.status != 200:
        print('Error from Web Site! Response code: ', resp.status)
    else:
        soup=BeautifulSoup(body, 'html.parser')
        event_list = soup.find('div', class_='row eventlist')
        # creating the list of dates, titles, speakers and html articles from web page
        date_lst =[]
        title_lst = []
        speaker_lst = []
        link_lst = []

        for row in event_list.find_all('div', class_='row'):
            tmp_date= [x.text for x in row.find_all('time')]
            date_lst.append(tmp_date)
        
            tmp_speaker = [x.text for x in row.find_all('p', class_='news__speaker')]
            speaker_lst.append(tmp_speaker)
        
            tmp_title = [x.text for x in row.find_all('em')]
            title_lst.append(tmp_title)

        # some of the links include video with the transcript. We are deleteing these here
        for link in event_list.find_all('a', href=True, class_ = lambda x: x != 'watchLive'):
            link_lst.append(link['href'])
        
        if print_test:
            print('length of dates: ', len(date_lst))
            print('length of speakers: ', len(speaker_lst))
            print('length of titles: ', len(title_lst))
            print('length of href: ', len(link_lst))

        return date_lst, speaker_lst, title_lst, link_lst

def create_speech_df(host, annual_htm_list):
    # Creates a DataFrame from the accumulated speech details across all URLs

    all_dates = []
    all_speakers = []
    all_titles = []
    all_links = []
    for item in annual_htm_list:
        date_lst, speaker_lst, title_lst, link_lst =find_speeches_by_year(host, 
                                                    item, print_test=False)
        all_dates = all_dates + date_lst
        all_speakers = all_speakers + speaker_lst
        all_titles = all_titles + title_lst
        all_links = all_links + link_lst
    
    dict1 = {'date': all_dates, 'speaker':all_speakers,
            'title': all_titles, 'link':all_links}
    df = pd.DataFrame.from_dict(dict1)
    
    #Cleaning up some of the dateframe elements to remove brackets
    df['date']=df['date'].str[0]
    df['date'] = pd.to_datetime(df['date'])
    df['speaker']=df['speaker'].str[0]
    df['title']=df['title'].str[0]
    
    # creating empty column for documents
    doc = np.zeros_like(df['date'])
    df['text'] = doc

    # removing items that are not speeches. These contain a link that starts with '/pubs/feds'
    delete_these = df[df['link'].str.match('/pubs/feds')].index
    df = df.drop(delete_these)
    return df

def retrieve_docs(host, df):
    # Scrapes full texts for each speech and updates the DataFrame with these texts

    for index, row in df.iterrows():
        this_item = df['link'][index]
        print('Scraping text for documents #: ', index)
        doc = get_one_doc(host, this_item)
        df['text'][index] = doc
    return df

def get_one_doc(host, this_url):
    # Retrieves and returns the full text content from a speech URL

    
    temp_url = 'https://' + host + this_url
    response = requests.get(temp_url)
    sp = BeautifulSoup(response.text)
    article = sp.find('div', class_='col-xs-12 col-sm-8 col-md-8')

    doc = []
    for p in article.find_all('p'):
        doc.append(p.text)

    return_doc = ''.join(doc)

    return return_doc

if __name__ == '__main__':
   
    # import functions
    import pandas as pd 
    import numpy as np
    from bs4 import BeautifulSoup
    from http.client import HTTPSConnection
    import pickle
    from urllib.request import urlopen
    import requests

    host = 'www.federalreserve.gov'
    prefix = '/newsevents/speech/'
    suffix = '-speeches.htm'
    start_year = 2012
    end_year = 2024

    # create list of web site containing annual speech links
    annual_htm_list =create_url_list(start_year, end_year, prefix, suffix)        
    print('Below is the annual_htm_list')
    print(annual_htm_list)
    
    # create dataframe containing speech information (not yet the text)
    df = create_speech_df(host, annual_htm_list)
    #print(df.info())
    
    
    # scrape the text from every speech in the dataframe
    df = retrieve_docs(host, df)
    print(df.info())

    # saving the df to a pickle file
    pickle_out = open('all_fed_speeches', 'wb')
    pickle.dump(df, pickle_out)
    pickle_out.close()