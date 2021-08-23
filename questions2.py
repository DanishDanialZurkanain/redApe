from urllib.parse import urlparse, unquote, parse_qs
import os 

def checkURIs(uriOne, uriTwo):
    one = urlparse(uriOne)
    two = urlparse(uriTwo)

    if one.port == None:
        one = one._replace(netloc = one.hostname + ':80')
    
    if two.port == None:
        two = two._replace(netloc = two.hostname + ':80')

    queryOne = parse_qs(one.query)
    queryTwo = parse_qs(two.query)

    pathOne = one.path
    pathTwo = two.path

    one = one.geturl() 
    two = two.geturl() 

    newOne = unquote(one)
    newTwo = unquote(two)
    
    newOne = os.path.normpath(newOne)
    newTwo = os.path.normpath(newTwo)


    if newOne == newTwo:
        print("True")
    elif queryOne == queryTwo:
        if pathOne == pathTwo:
            print("True")
    else:
        print("False")

if __name__ == "__main__":
  checkURIs('http://abc.com:80/~smith/home.html', 'http://ABC.com/%7Esmith/home.html')
  checkURIs('http://abc.com/drill/down/foo.html', 'http://abc.com/drill/further/../down/./foo.html')
  checkURIs('http://abc.com/foo.html?a=1&b=2', 'http://abc.com/foo.html?b=2&a=1')
  checkURIs('http://abc.com/foo.html?a=1&b=2&a=3', 'http://abc.com/foo.html?a=3&a=1&b=2')