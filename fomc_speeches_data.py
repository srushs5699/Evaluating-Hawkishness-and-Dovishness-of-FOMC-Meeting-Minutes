''' 
    SCRAPING FEDERAL RESERVE SPEECHES

This file contains the functions to scrape the federal reserve web site for 
speech details and text from 2006 through today. The speeches are stored in 
a dataframe with the following columns
    date
    speaker
    title
    link (to site for speech text)
    text (speech stored as a string)

The Federal Reserve website contains a searchable site with their speeches at:
    https://www.federalreserve.gov/newsevents/speeches.htm

The speeches themselves are separated by year and stored on their own web pages with links 
to the path to the text file. For example: 
    "/newsevents/speech/2019-speeches.htm"
    "/newsevents/speech/2018-speeches.htm"
    "/newsevents/speech/2006speech.htm"

The results are saved to a pickle file with the named 'all_fed_speeches'
'''

def create_url_list(start_year, end_year, prefix, suffix):
    '''
    The Federal Reserve has a seperate web site for each year that contains links
    to the speeches made during that year. This function creates the list of 
    the paths to the web sites where the speeches are stored.
    
    INPUTS: 
        start_year  an int containing the first year of speeches to pull
                    (start_year >= 2006)
        end_year    an int containing the final year of speeches to pull
                    (we would expect this to be the current year)
        prefix      a string containing the first part of the path to the speechs
        suffix      a string containing the second part of the path to speeches
    
    OUTPUT: 
        annual_htm_list     which contains the path to the web sites containing 
                            speeches for each year

    NOTES: 
        1. The prefix does not include the host. The host is 'www.federalreserve.gov'
        2. The suffix has changed over time. Before 2011, the suffix was 'speech.htm'
            but this was changes to '-speeches.htm'
        3. This function only works from 2006 onward. Before that time period the Fed
            stored their speeches in a slightly different format

    EXAMPLE:
        Calling this function with 
            start_year = 2014
            end_year = 2019
            prefix = '/newsevents/speech/'
            suffix = '-speeches.htm'
        Returns the list of stings below
            ['/newsevents/speech/2016-speeches.htm',
            '/newsevents/speech/2017-speeches.htm',
            '/newsevents/speech/2018-speeches.htm',
            '/newsevents/speech/2019-speeches.htm']
    '''
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
    '''
    Takes the host and a url for a given year
    and returns infromation about the speeches and links to the web site
    containing the text of the speeches. This function is used to create
    the list of all web sites that contain the individual speeches that
    need to be scraped.

    INPUTS:
        host        the host (for the Federal Reserve 'www.federalreserve.gov)
        this_url         the path to the speeches for a given year
        print_test  an optional field that will print out summary statistics
    
    OUTPUT:
        date_lst    list of speech dates
        speaker_lst list of speaker names
        title_lst   list containing titles of speeches
        link_lst    list of htm links to the actual speeches
    
    NOTES:
        1. There are video links on some of the urls that we need to removed.
            These videos are represented by the 'watchLive' class.
        
    '''
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
    '''
    Builds a dataframe containing information and links to all of the
    Federal Reserve speeches. This dataframe is later called to scrape the
    actual speeches

    INPUTS:
        host                the host (for the Federal Reserve 'www.federalreserve.gov)
        annual_htm_list     which contains the path to the web sites containing 
                             speeches for each year
   
    OUTPUT:
        df    a dateframe containing the following columns
            ['date]         date of speech
            ['speaker']     speaker
            ['title']       title of speech
            ['link']        link to website with speech text to be scraped
            ['text']        empty column to be populated later with text
    
    NOTES:
        1. There are two items from 2006 to present that are on the Federal Reserve
            website that are not speeches but reports. These items are removed in this
            function by idenfitying dataframe rows where the link contains '/pubs/feds'

    '''
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
    '''
    This function takes a dataframe with the columns 'link' and 'text' and the host to 
    the paths contained in the link column. The original dataframe is returned with
    the text of the scrapped speeches in the 'text' column as a string

    INPUTS:
        host    the host to the Federal Reserve
        df      a dataframe containing the column 'link' which contains all of the
                speech paths to be scrapped
                the dataframe should also contain a blank column 'text' that gets
                populated in this funciton

    OUTPUTS:
        df      the original dataframe is returned with the column 'text' populated
                with the text from the speeches
    '''
    for index, row in df.iterrows():
        this_item = df['link'][index]
        print('Scraping text for documents #: ', index)
        doc = get_one_doc(host, this_item)
        df['text'][index] = doc
    return df

def get_one_doc(host, this_url):
    '''
    This function takes a host and url containing the location of one Federal
    Reserve speech and returns a string containing the text from the speech.
    
    INPUTS:
        host    the host to the Federal Reserve
        url     the path to a particular speech

    OUTPUTS:
        string  containing the text of the speech

    '''
    
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