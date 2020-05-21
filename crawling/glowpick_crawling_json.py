import requests
import pandas as pd



def glowpick_json():
    ID_data = pd.read_csv('glowpick_items_data_lv2.csv', encoding='utf-8')
    # ID_data = pd.read_csv('glowpick_items_data.csv', encoding='utf-8') 데이터가 2개
    ID_list = list(ID_data['ID'])
    category = []
    name = []
    keywords = []
    error = []
    for idx, x in enumerate(ID_list):
        url = 'https://api-j.glowpick.com/api/product/{}'.format(x)
        headers = {
        'authority': 'api-j.glowpick.com',
    'method': 'GET',
    'path': '/api/product/{}'.format(x),
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization':'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnbG93cGljay53ZWIiLCJpYXQiOjE1OTAwMzg1NjgsInN1YiI6Imdsb3dwaWNrLWF1dGgiLCJpc3MiOiJnbG93ZGF5eiIsImV4cCI6MTU5MDEyNDk2OCwiYXVkIjoiSTRXWmlNbTg1YmppUDlaTzI4VUJndDg1WmljRUM4S09iRG9vUEMyb3FKQkF4dVQ1SzJNLzhqUTFtalpoT29QL05wMW9BZVpWZG80bC8xeTBmS0t4N1E9PSJ9.BphqoxydaQfPtCO5n72HcakWEfEM_S8aNPZicV9zRJs',
            # 오류나는 경우 authorization 값 부터 수정
    'cache-control': 'no-cache',
    'origin': 'https://www.glowpick.com',
    'pragma': 'no-cache',
    'referer': 'https://www.glowpick.com/product/{}'.format(x),
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
}
    response = requests.get(url, headers=headers)
    print('{} 중 {}'.format(len(ID_list), idx))
    if response.text == '{"message":null}':
        error.append(x)
        continue
    else:
        cat = response.json()['data']['categoryInfo'][0]['secondCategoryText']
        name_ = response.json()['data']['productTitle']
        keyword = response.json()['data']['keywords']
        category.append(cat)
        name.append(name_)
        keywords.append(keyword)

    data = {
    'category':category,
    'name':name,
    'keywords':keywords
    }
    
    return pd.DataFrame(data)