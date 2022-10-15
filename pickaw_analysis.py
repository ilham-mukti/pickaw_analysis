import requests
import pandas as pd
import os 
import ast
from datetime import datetime
from pytz import timezone
import json

class PickawContest:
  def __init__(self):
    self.pages = 3
    self.output_file = "list_pickaw_contest.csv"
    self.seed_list = "seed_list.json"
    self.cookies = {
        'i18n-lang': 'en',
        '_ga': 'GA1.2.367684644.1665811144',
        '_gid': 'GA1.2.1270628231.1665811144',
        '_fbp': 'fb.1.1665811144465.357421690',
        'crisp-client%2Fsession%2Fad02dfcf-7460-460d-bc6d-658345899d51': 'session_3d39dea8-bd1d-40ec-8e21-43da153e1c1a',
        'crisp-client%2Fsocket%2Fad02dfcf-7460-460d-bc6d-658345899d51': '1',
        'registration': '13671c4f940343259887329f34792118sq7uT7DbNgNBvqerfyquWJa86%2BjY6yi7yYzFpgWKy4BAwGccR%2FxNMisNRREkKfyVCDp8Xl3qSf3LGZeG4AWBPKL%2BfOxboYnl8sSgHBqLOM01rzdMYkeD1Y8dldXCzG%2F3FRxaFan%2FWB2E8%2FJJc%2FGpw%2BPle%2F0fzrWih0%2FTne5dPJ1zrSgW0CNpxHcrbogGz7DbgUKRqln3flM%2BgF%2FxlnYV%2BLdO1DqjLmyZyKb7oWgHBAV0dM2dZX6MW1gdUgFHT3gcx8Nv8L1%2BLwZ85M1SDE9KZ5rY05lidL6YJLBnCBZ8aL19SPX1mpOVMIbtz%2BWjyp0Xz%2FdMzA3sRrrEjnV7cP4j57Wkm%2F1A9AxwHY4zZXQMkNzLoZPtKlPslyYSHJJVNr8kUjfHDV4jXunuslwcLQmij4KJXPGikpojshoFWzSt3GReTVmYodQEhrC0fIw2d3%2B3O8LKIvJQD%2FXEvh0TvDtMJZP4VzW0PByANQLkoc75H9Q5YpTO3XCxKKFkWs5qdq7lrAiyjHnzgNWv6ycWN5Qo4rmK5gyWpUFD165eOXPYz3%2BTkLRXqBrNcISscW4gomVHKFpigWGtE89jHgxgYjfw%2FpNU00bdfUhGgsfIkAnTbL2C6ZShiGUD4Hs1DEGTHBV2nQEMHi9iYwJGrdDvrMKJwCqZEbYVpDF%2B4LQebMqzhuDMqN8WZjpmYZ3k5F8QZ1orBHAk%2F5tdJsXjETJ%2FpzybeRd1ysz4jpWZlDb6MH%2FhFbFXIGIEJElpLe26Wj2tAR47pWoae4soJ13I9%2BAFhGKUY79yf5zYygG4DfoBZpiLRVVw8ykygyKvyaF0%2BLau5CHsvcD46v66hDFKN1dx88Dqag%3D%3D',
        'session': '5b52e8745adcc290c412d72f4686a5c6kw6rDVz4HGu%2Bmjv7Q%2FLjmVzFhNbeNxxjJOdCnjWUQrMRwIU3TQ4%2FmUIq4qrwI7FPS%2FkN8H0CQe6xO1UUaxUN8NdMM4n0VQDaBX9L1Sk%2F3HrN4eyqjhWr2vUXUyG%2BpsNE',
        'XSRF-TOKEN': 'a22ef85f36bd518c68271ee0cd72d30d3BMnTujlcvm9BEZPz7jGzUl66xEa83JdNlep%2FjAv%2Bz%2BYs%2FRb%2B6biw0qtX9VaivQhvHLeYKnkXFlW1Y7eB8ucH0q05dlyvt4xDPKtAMTgOkRH5vOj3XToy1drdWggp7jg',
        '_gat': '1',
    }

    self.headers = {
        'authority': 'pickaw.app',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9',
        'referer': 'https://pickaw.app/me/contests',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-pickaw-version': '1.22.0',
        'x-requested-with': 'XMLHttpRequest',
        'x-websocket-id': 'YSXQD2IO-7pKgRjTAFI0',
        'x-xsrf-token': 'a22ef85f36bd518c68271ee0cd72d30d3BMnTujlcvm9BEZPz7jGzUl66xEa83JdNlep/jAv+z+Ys/Rb+6biw0qtX9VaivQhvHLeYKnkXFlW1Y7eB8ucH0q05dlyvt4xDPKtAMTgOkRH5vOj3XToy1drdWggp7jg',
    }

  def request_data(self):
    my_dict = {}
    for page in range(1, self.pages):
      print(page)
      params = {
          'page': page,
      }
      url_contest = 'https://pickaw.app/api/v1/users/me/contests'
      response = requests.get(url_contest, params=params, cookies=self.cookies, headers=self.headers).json()
      datas = response['data']
      for data in datas:
        entries_count = data['entries_count']
        my_dict[data['draw']['seed']] = entries_count
    return my_dict

  def check_seed(self, data_baru):
    f = open(self.seed_list, 'r')
    data_lama = f.read()
    data_lama = ast.literal_eval(data_lama)
    dict_baru = {}
    for key, value in data_baru.items():
      if key not in data_lama.keys():
        dict_baru[key] = value
    f.close()
    merge_dict = {**data_lama, **dict_baru}
    self.create_file(self.seed_list, merge_dict)
    self.dict_baru = dict_baru
    return dict_baru

  def get_contest(self):
    is_new = not os.path.isfile(self.seed_list)
    if is_new: #Jika baru
      print("bikin baru")
      data = self.request_data()
      self.create_file(self.seed_list, data)
    else:
      print("sudah ada")
      data_baru = self.request_data()
      data = self.check_seed(data_baru)
    print(data)
    return data

  def get_winners(self, seed_code):
    if(len(seed_code) != 0):
      my_dict = []
      for seed, value in seed_code.items():
        url_seed = f'https://pickaw.app/api/v1/draws/seed/{seed}'
        response = requests.get(url_seed, cookies=self.cookies, headers=self.headers).json()
        entries_count = response['sources'][0]['remote_entries_count']
        weighted_entries_count = response['sources'][0]['weighted_entries_count']
        drawn_at = response['drawn_at'] 
        loaded_at = response['loaded_at'] 
        winner_entries = response['draw']['picked']['data'][0]['pos_end']
        winner_account = response['draw']['picked']['data'][0]['account']['url']
        ga_host = response['sources'][0]['account']['screen_name']
        entries_percentage = round(winner_entries/entries_count*100)
        if entries_percentage>=75:
          category_entries = ">=75"
        elif entries_percentage>=50:
          category_entries = ">=50"
        elif entries_percentage>=25:
          category_entries = ">=25"
        else:
          category_entries = "<=25"
        print(f"{seed} -> {winner_entries} / {entries_count} => {entries_percentage}")
        my_dict.append({'host': ga_host, 'seed': seed, 'url_seed': url_seed, 'drawn_at': drawn_at, 'loaded_at': loaded_at, 'winner': winner_account, 'winner_entries': winner_entries, 'entries_count': entries_count, 'weighted_entries_count': weighted_entries_count,'entries_percentage': entries_percentage, 'category_entries': category_entries})
      df = self.save_to_dataframe(my_dict)
    self.update_readme(seed_code)

  def save_to_dataframe(self, my_dict):
    df = pd.DataFrame(my_dict, columns=my_dict[0].keys())
    df.to_csv(self.output_file, mode='a', index=False, header=not os.path.exists(self.output_file))
    return df

  def create_file(self, name_file, data):
      f = open(name_file, 'w')
      f.write(str(data))
      f.close()
      print("selesai")

  def update_readme(self, data_baru=None):
      jkt = timezone('Asia/Jakarta')
      now = datetime.now(jkt)
      with open('README.md', 'w') as f:
         f.write(f"# Data tanggal: {now}\n\n")
         f.write(f'* {data_baru}\n')
         f.close()

model = PickawContest()
seed_code = model.get_contest()
model.get_winners(seed_code)
