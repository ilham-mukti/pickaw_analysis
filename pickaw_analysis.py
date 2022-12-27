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
        '_ga': 'GA1.2.966894380.1672163046',
        '_gid': 'GA1.2.1151518720.1672163046',
        '_fbp': 'fb.1.1672163046311.953956500',
        'crisp-client%2Fsession%2Fad02dfcf-7460-460d-bc6d-658345899d51': 'session_ddbda3cd-3908-4049-8700-beae6f5d4c17',
        'session': '9ae366c9f5616062d16b721c4a415084Eqk4aaVsXnw%2FTcn9ex30PKmpQQJAwUperb%2BwmTwweliqy6hjx7k%2B0OO0%2BkD0TVAIeJlXtQfUtOri5GhSMmIpXqIcBp01GlDBPrhdNiC5o4%2Bgy2by2FiJS0CQb1dEOvQd',
        'XSRF-TOKEN': 'ff6725193b569036fa405c96fa9e0fbb6AdFIkSa0wQnx%2BdjM7OzoFzQV%2Fldrix2Too6WFFKZsCbnlGm8WK9aAHI5UcjxD37XvNTiewUXwVczBFIwh67mw6IUKNd2amDWsBeVEvfORlHPT12ImRXCrqr4yBIjyYZ',
        '_gat': '1',
    }

    self.headers = {
        'authority': 'pickaw.app',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9',
        'referer': 'https://pickaw.app/me/contests',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-pickaw-version': '1.23.3',
        'x-requested-with': 'XMLHttpRequest',
        'x-websocket-id': 'U93iXlfSDrco9GxaAju7',
        'x-xsrf-token': 'ff6725193b569036fa405c96fa9e0fbb6AdFIkSa0wQnx+djM7OzoFzQV/ldrix2Too6WFFKZsCbnlGm8WK9aAHI5UcjxD37XvNTiewUXwVczBFIwh67mw6IUKNd2amDWsBeVEvfORlHPT12ImRXCrqr4yBIjyYZ',
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
