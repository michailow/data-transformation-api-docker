import requests


def main():
    urlGet = 'http://127.0.0.1:80'
    r = requests.get(urlGet)
    assert r.text == 'App started', 'Failture with API'
    urlPost = 'http://127.0.0.1:80/postOutlet/tripadvisor_user.json'
    r = requests.post(urlPost)
    assert r.text == 'File tripadvisor_user.json posted',\
        'Failture with DB'
    print('Everything passed')
    input()


if __name__ == '__main__':
    main()