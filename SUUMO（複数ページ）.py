#!/usr/bin/env python
# coding: utf-8

# In[107]:


#ライブラリーのインポート
from time import sleep

from bs4 import BeautifulSoup
import requests


# In[108]:


#変数urlにSUUMOホームページのURLを格納する
url = 'https://suumo.jp/chintai/tokyo/sc_chuo/?page={}'

#変数d_listに空のリストを作成する
d_list = []


# In[109]:


#1~3をループする
for i in range(1,4):
    print('d_listの大きさ：',len(d_list))
    
    #変数target_urlに、アクセス先のURLを格納する
    target_url = url.format(i)
    
    #print()してtarget_urlを確認する
    print(target_url)
    
    #2.'Requests'を使って1で設定したURLにアクセスする
    r = requests.get(target_url)
    
    sleep(1)
    
    #3.取得したHTMLを'BeautifulSoup'で解析する
    soup = BeautifulSoup(r.text)      
    
    #4.すべての物件情報（20件）を取得する
    contents = soup.find_all('div',class_='cassetteitem')

    #5.各物件情報をforループで取得する
    for content in contents:

     #それぞれを解析する
     #物件情報と部屋情報を取得しておく
     detail = content.find('div',class_='cassetteitem_content')
     table = content.find('table',class_='cassetteitem_other')

     #物件情報から必要な情報を取得する
     title = detail.find('div',class_='cassetteitem_content-title').text
     address = detail.find('li',class_='cassetteitem_detail-col1').text
     access = detail.find('li',class_='cassetteitem_detail-col2').text
     age = detail.find('li',class_='cassetteitem_detail-col3').text

     #部屋情報のブロックから各部屋情報を取得する
     tr_tags = table.find_all('tr',class_='js-cassette_link')
     tr_tag = tr_tags[0]
    
    #各部屋情報をforループで取得する
    for tr_tag in tr_tags:

     #部屋情報から欲しい情報を取得する
     floor,price,first_fee,capacity = tr_tag.find_all('td')[2:6]
    
     #さらに細かい情報を取得する
     fee, manegement_fee = price.find_all('li')
     deposit, gratuity = first_fee.find_all('li')
     madori, menseki = capacity.find_all('li')
    
     #取得したすべての情報を辞書に格納する
     d = {
      'title':title,
      'address':address,
      'access':access,
      'age':age,
      'floor':floor.text,
      'fee':fee.text,
      'manegement_fee':manegement_fee.text,
      'deposit':deposit.text,
      'gratuity':gratuity.text,
      'madori':madori.text,
      'menseki':menseki.text,
      }
    
     #取得した情報をd_listに格納する
     d_list.append(d)


# In[110]:


get_ipython().run_cell_magic('time', '', '#1=10を出力するコードを時間計測とともに出力する\nfor i in range(1,11):\n    print(i)\n')


# In[111]:


#d_listに格納されている最後のインデックスを確認する
d_list[-1]


# In[112]:


#4.すべての物件情報（20件）を取得する
contents = soup.find_all('div',class_='cassetteitem')

#5.各物件情報をforループで取得する
for content in contents:

#物件情報と部屋情報を取得しておく
detail = content.find('div',class_='cassetteitem-detail')
table = content.find('table',class_='cassetteitem_other')

#物件情報から必要な情報を取得する
title = detail.find('div',class_='cassetteitem_content-title').text
address = detail.find('li',class_='cassetteitem_detail-col1').text
access = detail.find('li',class_='cassetteitem_detail-col2').text
age = detail.find('li',class_='cassetteitem_detail-col3').text

#部屋情報のブロックから各部屋情報を取得する
tr_tags = table.find_all('tr',class_='js-cassette_link')
tr_tag = tr_tags[0]

#各部屋情報をforループで取得する
for tr_tag in tr_tags:

#部屋情報から欲しい情報を取得する
floor,price,first_fee,capacity = tr_tag.find_all('td')[2:6]

#さらに細かい情報を取得する
fee, manegement_fee = price.find_all('li')
deposit, gratuity = first_fee.find_all('li')
madori, menseki = capacity.find_all('li')

#取得したすべての情報を辞書に格納する
d = {
  'title':title,
  'address':address,
  'access':access,
  'age':age,
  'floor':floor.text,
  'fee':fee.text,
  'manegement_fee':manegement_fee.text,
  'deposit':deposit.text,
  'gratuity':gratuity.text,
  'madori':madori.text,
  'menseki':menseki.text,
 }

#取得した情報をd_listに格納する
d_list.append(d)


# In[113]:


#cassetteクラスを持ったdivタグをすべて取得しいて、変数contentsに格納
contents = soup.find_all('div',class_='cassetteitem')


# In[114]:


#変数contentsの中身を確認する
len(contents)


# #変数contentにcontentsの最初の要素を格納する
# content = contents[0]

# 取得したい項目の確認
# 物件名
# -住所
# -間取り
# -家賃
# -階数

# In[115]:


#物件情報を変数detailに格納する
detail=content.find('div',class_='cassetteitem-detail')

#各部屋の情報を変数tableに格納する
table = content.find('table',class_='cassetteitem_other')


# In[116]:


#変数titleに物件名を格納する
title = detail.find('div',class_='cassetteitem_content-title').text

#変数addressに住所を格納する
address = detail.find('li',class_='cassetteitem_detail-col1').text

#変数accessにアクセス情報を格納する
access = detail.find('li',class_='cassetteitem_detail-col2').text

#変数ageに築年数を格納する
age = detail.find('li',class_='cassetteitem_detail-col3').text


# In[117]:


#各変数の取得結果を確認
title, address, access, age


# In[118]:


#変数tableからすべてのtrタグを取得して、変数tr_tagsに格納
tr_tags = table.find_all('tr',class_='js-cassette_link')

#tr_tagsの中から最初の１つだけtr_tagに格納
tr_tag = tr_tags[0]


# 取得したい項目の確認
# 物件名
# -階数
# -賃料/管理費
# -敷金・礼金
# -間取り・面積

# In[119]:


# 変数floor,price,first_fee,capacityに４つの情報を格納する
floor,price,first_fee,capacity = tr_tag.find_all('td')[2:6]


# In[120]:


# 変数floor,price,first_fee,capacityの中身を確認する
floor,price,first_fee,capacity


# In[121]:


#変数feeとmanegement_feeに、賃料を管理費を格納する
fee, manegement_fee = price.find_all('li')

#変数depositとgratuityに、敷金と礼金を格納する
deposit, gratuity = first_fee.find_all('li')

#変数madoriとmensekiに、間取りと面積を格納する
madori, menseki = capacity.find_all('li')


# In[122]:


#変数feeとmanegement_feeを確認する
print(fee)
print(manegement_fee)
print()

#変数depositとgratuityを確認する
print(deposit)
print(gratuity)
print()

#変数madoriとmensekiを確認する
print(madori)
print(menseki)
print()


# In[123]:


#変数dに、これまで取得した１１項目を格納する  floor,price,first_fee,capacity
d = {
    'title':title,
    'address':address,
    'access':access,
    'age':age,
    'floor':floor.text,
    'fee':fee.text,
    'manegement_fee':manegement_fee.text,
    'deposit':deposit.text,
    'gratuity':gratuity.text,
    'madori':madori.text,
    'menseki':menseki.text,
}


# In[124]:


#変数dの中身を確認する
d


# In[127]:


#変数d_listに空のリストを作成する
d_list= []

#すべての物件情報（20件）を取得する
contents = soup.find_all('div',class_='cassetteitem')

#各物件情報をforループで取得する
for content in contents:

   #物件情報と部屋情報を取得しておく
   detail =content.find('div',class_='cassetteitem-detail')
   table = content.find('table',class_='cassetteitem_other')

   #物件情報から必要な情報を取得する
   title = detail.find('div',class_='cassetteitem_content-title').text
   address = detail.find('li',class_='cassetteitem_detail-col1').text
   access = detail.find('li',class_='cassetteitem_detail-col2').text
   age = detail.find('li',class_='cassetteitem_detail-col3').text

   #部屋情報のブロックから各部屋情報を取得する
   tr_tags = table.find_all('tr',class_='js-cassette_link')
   tr_tag = tr_tags[0]
    
   #各部屋情報をforループで取得する
   for tr_tag in tr_tags:

    #部屋情報から欲しい情報を取得する
    floor,price,first_fee,capacity = tr_tag.find_all('td')[2:6]
    
    #さらに細かい情報を取得する
    fee, manegement_fee = price.find_all('li')
    deposit, gratuity = first_fee.find_all('li')
    madori, menseki = capacity.find_all('li')
    
    #取得したすべての情報を辞書に格納する
    d = {
      'title':title,
      'address':address,
      'access':access,
      'age':age,
      'floor':floor.text,
      'fee':fee.text,
      'manegement_fee':manegement_fee.text,
      'deposit':deposit.text,
      'gratuity':gratuity.text,
      'madori':madori.text,
      'menseki':menseki.text,
     }
    
    #取得した情報をd_listに格納する
    d_list.append(d)


# In[128]:


#pprintをインポートする
from pprint import pprint


# In[129]:


#d_listに入っているインデックスの0番目と1番目を確認する
pprint(d_list[0])
print()
pprint(d_list)


# In[ ]:





# In[ ]:




