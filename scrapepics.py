from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import os


def testurl(url): #test the url, make it something like 'http://www.XXXXX.XX'
    if url.startswith('http'):
        url = url
    elif url.startswith('www.'):
        url = 'http://' + url
    elif url.startswith('//'):
        url = 'http:' + url
    else:
        url = 'http://www.' + url
    return url


def geturl():  # ask user to enter a url, test it and return it.
    url = str(input('Please enter the page url that you want to scrape pictures, '
                'such as "baidu.com".\n'))
    url = testurl(url)
    return url


def makefolder(foldername):  # make a folder to contain the downloaded pictures
    folder = os.path.join(os.getcwd(), foldername)
    if not os.path.exists(folder):
        os.mkdir(folder)
    return folder


pageurl = geturl()
folder = makefolder(pageurl[11:]) #folder name is the url

try:       #inform the user and exit the program if exception occur when opening the url
    pageobj = urlopen(pageurl)
except Exception as err:
    print("It seems that something is wrong:\n" + str(err) + "\n")
    exit()

picsobj = BeautifulSoup(pageobj, 'html.parser').find_all('img', src=True) # use bs to get a obj that contain img links

print('Start downloading pictures...')

x = 0
for picobj in picsobj:    #download pics one by one
    x += 1
    url = testurl(picobj['src'])
    try:
        urlretrieve(url, '%s/%d.jpg' % (folder, x))
        print('%d pictures downloaded.' % x)
    except Exception as err:   #skip it if exception occur when open one pic link
        x -= 1
        continue

if x == 0:   #inform user and exit program if no pics downloaded
    print("Sorry, we can't download any pictures from the page...")
    exit()

print('Downloading pictures completed.')
