#!/usr/bin/env python
# coding: utf-8

# In[1]:


from time import sleep
from bs4 import BeautifulSoup
import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe


# In[2]:


#変数urlにSUUMOホームページをのURLを格納する
url='https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&pc=30&smk=&po1=25&po2=99&tc=0400203&tc=0400905&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sc=13102&sc=13106&sc=13108&ta=13&cb=0.0&ct=15.0&co=1&md=03&md=04&md=06&md=07&ts=1&et=7&mb=30&mt=9999999&cn=20&tc=0400301&tc=0400101&fw2=&page={}'


# In[3]:


#リストを作成
property_list = []

#1p～20pまで情報を取得 ※データがない場合の考慮検討
for i in range(1,10):
    
    print(len(property_list))

    target_url = url.format(i)

    print(target_url)

    r = requests.get(target_url)

    sleep(1)

    soup = BeautifulSoup(r.text)

    #全てのcasseteitem情報を取得
    contents = soup.find_all('div', class_='cassetteitem')

    #各物件情報をforループで取得する
    for content in contents:

        #物件情報を取得しておく
        detail = content.find('div', class_='cassetteitem-detail')

        #物件名と住所を取得
        title = detail.find('div', class_='cassetteitem_content-title').text
        station_near = detail.find('div', class_='cassetteitem_detail-text').text
        address = detail.find('li', class_='cassetteitem_detail-col1').text

        #各部屋情報(階数、家賃、敷金＆礼金、広さ)を取得
        table = content.find('table', class_='cassetteitem_other')
        tr_tags = table.find_all('tr', class_='js-cassette_link')
        floor, price, first_fee, capacity = tr_tags[0].find_all('td')[2:6]

        fee, management_fee = price.find_all('li')
        deposit, gratuity = first_fee.find_all('li')
        madori, menseki = capacity.find_all('li')

        property = {
            '物件名': title,
            '最寄り駅': station_near,
            '住所': address,
            '間取り': madori.text,
            '家賃': fee.text,
            '階': floor.text
        }


        #取得した辞書をproperty_listに格納する
        property_list.append(property)


# In[4]:


df = pd.DataFrame(property_list)


# In[5]:


print(df.columns)


# In[6]:


#（削除）階列から、「階」を削除
df['階'] = df['階'].apply(lambda x: x.replace('階', ''))
#（削除）家賃から、「万円」を削除
df['家賃'] = df['家賃'].apply(lambda x: x.replace('万円', ''))
#（削除）住所から、「東京都」を削除
df['住所'] = df['住所'].apply(lambda x: x.replace('東京都', ''))
# 不要なスペースをすべて削除
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

#最寄り駅カラムデータのクレンジング

#（抽出→新規列追加）最寄駅から、駅までの距離だけを抽出し、「駅までの距離（徒歩/分）」として新規列に追加
df[['最寄り駅', '駅までの距離（徒歩/分）']] = df['最寄り駅'].str.split(' ', expand=True)

#（削除）駅までの距離（徒歩/分）カラムデータ、歩と分の文字列を消す
df['駅までの距離（徒歩/分）'] = df['駅までの距離（徒歩/分）'].apply(lambda x: x.replace('歩', ''))
df['駅までの距離（徒歩/分）'] = df['駅までの距離（徒歩/分）'].apply(lambda x: x.replace('分', ''))

#（分割）最寄り駅名カラムを、路線名と駅名で分割
df[['路線名', '駅名']] = df['最寄り駅'].str.split('/', expand=True)

# 最寄り駅カラムと路線名、駅名カラムを入れ替え、最寄り駅カラムを削除
df = df.drop('最寄り駅', axis=1)
column_order = ['物件名', '路線名', '駅名', '駅までの距離（徒歩/分）', '間取り', '階', '家賃', '住所']
df = df[column_order]


# In[7]:


#重複削除（物件名=最寄り駅名となっているものを消去する）

#（抽出）物件名と最寄り駅が共通しているデータを抽出
def find_common_part(title, station_near):
    common_parts = []
    for word in title.split():
        if word in station_near:
            common_parts.append(word)
    return " ".join(common_parts)

# （df格納）共通部分をdfとして格納
df['共通部分'] = df.apply(lambda x: find_common_part(x['物件名'], x['路線名'] + ' ' + x['駅名']), axis=1)


# （df格納）物件名から最寄り駅名と共通部分を削除したものをdfに格納
df['物件名（共通部分削除後）'] = df.apply(lambda x: x['物件名'].replace(x['共通部分'], ''), axis=1)

# (入れ替え) 共通部分削除後の物件名を、元の物件名に置き換える
df['物件名'] = df['物件名（共通部分削除後）']

# （削除）共通部分削除のカラムを削除する
df = df.drop(columns=['共通部分', '物件名（共通部分削除後）'])

#重複削除（重複している物件情報を削除）
# 重複した行を特定する条件を指定
duplicate_condition = df.duplicated(subset=['住所', '家賃', '階'], keep=False)

# 重複した行を抽出
duplicates = df[duplicate_condition]
# 重複した行を削除
df = df.drop_duplicates(subset=['住所', '家賃', '階'], keep='first')

# dfをcsvに出力
df.to_csv('suumo_cleansing.csv', index=None, encoding='utf-8-sig')


# In[9]:


import sqlite3

# データベースに接続
conn = sqlite3.connect('/users/mihokoonishi/suumo_properties_list.db')
cursor = conn.cursor()

# テーブルの内容をクエリする
cursor.execute("SELECT * FROM suumo_properties_list")
rows = cursor.fetchall()

for row in rows:
    print(row)

# 接続を閉じる
conn.close()


# In[10]:


#スプレッドシート格納
#必要なログイン情報を取得
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('tech0-step3-411723-02357e5d467b.json', scope)
gc = gspread.authorize(credentials)

#対象となるスプレッドシートを選択
spreadsheet = gc.open('suumo_properties_list')

# DataFrameのデータをリストに変換（カラム名を含む）
df_data_with_columns = [df.columns.tolist()] + df.values.tolist()

# データをスプレッドシートに挿入
worksheet = spreadsheet.get_worksheet(0)  # ワークシートのインデックスを指定
worksheet.insert_rows(df_data_with_columns, 2)  # データを挿入

# 空白行を削除
worksheet.delete_rows(1)  # 1行目を削除

#SQLliteにdfを格納
import sqlite3

# 新しいテーブルを作成（suumo_properties_list.db）
conn = sqlite3.connect('suumo_properties_list.db')
# sqlへdf内容を挿入
df.to_sql('suumo_properties_list', conn, if_exists='replace', index=False)


# In[9]:


# ワークフロー名
name: housework_bot
on:
  schedule:
    # 定期実行する時間
    - cron: '0 12 * * *'
  
jobs:
  build:
    # Ubuntuの最新版環境内で処理を実行することを指定
    runs-on: ubuntu-latest

    # 実行する処理＆コマンド指定
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.11.7
        uses: actions/setup-python@v1
        with:
          python-version: 3.11.7
      - name: Install dependencies
        run: 
          # pip更新
          python -m pip install --upgrade pip
          # 必要なパッケージインストール・・・②
          pip install requests
          pip install beautifulsoup4
          pip install pandas
          pip install tqdm
          pip install numpy
          

      - name: Run script
        run: |
          # 定期実行するファイルを指定。・・・③
          python suumo_cleansing.py

      - name: Commit and push if there are changes
        run: |
          git config --global user.name 'mipo0610'
          git config --global user.email 'mihoko.o.0610@gmail.com'
          git add -A
          git commit -m 'Update database' || exit 0  # コミットがなければ終了
          git remote set-url origin https://${{ secrets.GH_TOKEN }}@github.com/mipo0610/techone.git
          git push


# In[ ]:




