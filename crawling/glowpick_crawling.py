class glowpick():
    
    def __init__(self):
        self.datas = self.GetId()
        item_df = self.GetDetailInfo()
        item_df['RANK'] = item_df['RANK'].replace(0,'-')
        item_df['PRICE'] = item_df['PRICE'].fillna(0).astype(int)
        self.item_df = item_df
        
    def GetId(self):
    
        urls_ls = []
        item_ls = []

        headers = ({
            'authorization' : 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnbG93cGljay53ZWIiLCJpYXQiOjE1ODk0NjA2NzIsInN1YiI6Imdsb3dwaWNrLWF1dGgiLCJpc3MiOiJnbG93ZGF5eiIsImV4cCI6MTU4OTU0NzA3MiwiYXVkIjoiSTRXWmlNbTg1YmppUDlaTzI4VUJnbmRNdldZVGZjOVVDeE04Nmk0VXlVSzNkQjc0Z3ZWKzhZbnhNNjd1bGo0NkhQMDZnY3JOV3JyTzgwM3NaNjZ2aGc9PSJ9.DDiqtcEIdUzDFj-Q9DEBC63zCqnLv7KFfmKxcdkCv_E',
            'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'referer' : 'https://www.glowpick.com/beauty/ranking?id=1&level=3',
            })

        for id in range(1,5):
            for cursor in range(1,6):
                offset = (cursor - 1) * 20
                url = f'https://api-j.glowpick.com/api/ranking/category/3/{id}?cursor={cursor}&id={id}&idBrandCategory=&order=rank&limit=20&level=3&offset={offset}'
                urls_ls.append(url)

        for url in urls_ls:
            req = requests.get(url, headers = headers)
            data = json.loads(req.text)
            item_ls.append(data)

        return item_ls
      
    def GetDetailInfo(self):
    
        items = []
        for i in range(len(self.datas)):
            try:
                for data in self.datas[i]['products']:
                    items.append({
                        'ID' : data['idProduct'],
                        'RANK' : data['productRank'],
                        'BRAND' : data['brand']['brandTitle'],
                        'NAME' : data['productTitle'],
                        'VOLUME' : data['volume'],
                        'PRICE' : data['price'],
                        'RATE' : data['ratingAvg'],
                    })
            except:
                pass

        return pd.DataFrame(items)
