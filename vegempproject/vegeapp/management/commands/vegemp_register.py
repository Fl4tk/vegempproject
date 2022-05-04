from django.core.management.base import BaseCommand
from vegeapp.models import vegemodel

class Command(BaseCommand):
    def handle(self, *args,**options):
        from bs4 import BeautifulSoup
        import requests
        import re
        import pandas as pd

        #---------------農林水産省HPから価格動向調査のExcel取得--------------------
        url = 'https://www.maff.go.jp/j/zyukyu/anpo/kouri/k_yasai/h22index.html'
        res = requests.get(url)
        soup = BeautifulSoup(res.text,'lxml')
        elems = soup.find('ul',class_='non mb30').find('a',attrs={'href':re.compile(r'.xlsx')})

        child = elems['href']
        child = child[1:]
        parent = url.replace('/h22index.html','')
        target = parent + child
        print(target)
        response = requests.get(target)
        #-------------------------------------------------------------------------

        #---------------------Excelを出力し、dfに変換・データ整形-------------------
        with open('sample.xlsx','wb') as f:
            f.write(response.content)

        df = pd.read_excel('sample.xlsx')
        df.columns = df.iloc[0]
        row_num = len(df)
        df = df[1:row_num-6]
        df = df.drop(['ほうれんそう','なす'],axis=1)
        #-------------------------------------------------------------------------

        #-----------------model登録(野菜名、最終更新日、価格/1kg)-------------------
        data = {}
        get_latest_data = df.columns[1:]

        #-----------------最新データの取得--------------------
        for _ in get_latest_data:
            exist_data = '-'
            max_row = len(df)
            while exist_data == '-':
                exist_data = df[_].iloc[max_row-1]
                max_row -= 1
            data[_] = {df.iloc[max_row].values[0].replace('の週',' 最終更新'):exist_data}
            #--------------最新データの取得ここまで--------------

            #--------------model登録用整形-------------------
            values = list(data.values())
            latestdate = list(values[len(values)-1])
            price = list(values[len(values)-1].values())

            result1 = latestdate[len(latestdate)-1]
            result2 = price[len(price)-1]
            try:
                db = vegemodel.objects.get(vegename=_) #既にmodel登録されていたら更新する
                db.latestdate = result1
                db.price = result2
                db.save()
            except:
                vegemodel(vegename=_,latestdate=result1,price=result2).save() #新規model登録
        self.stdout.write(self.style.SUCCESS('Successfully vegemp_register')) #終了メッセージ表示