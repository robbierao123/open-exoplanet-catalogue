import urllib.request

def download_csv(url, destination):

    try:
        urllib.request.urlopen('http://google.ca', timeout=1)
    except urllib.request.URLError as err:
        print('url is down!')
        return
    urllib.request.urlretrieve(url, destination)

'''
download_csv('http://exoplanet.eu/catalog/csv/', 'F:/Senior/CSCC01/Project/OEC Data/EU_Catalogue_Data.csv')
'''
