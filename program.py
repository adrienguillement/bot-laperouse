import urllib.request
from urllib.error import HTTPError


def download_file(download_url):
    try:
        response = urllib.request.urlopen(download_url)

        file = open("programme-fr.pdf", 'wb')
        file.write(response.read())
        file.close()
        print("Completed")
    except HTTPError as err:
        if err.code == 404:
            print('error 404')
        else:
            print('unknow error')


download_file("http://www.puydufou.com/ftp/programme-fr.pdf")
