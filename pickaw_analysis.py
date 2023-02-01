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
        '_ga': 'GA1.2.1235118764.1675263230',
        '_gid': 'GA1.2.1230196898.1675263230',
        '_gat': '1',
        '_fbp': 'fb.1.1675263230127.657079218',
        '_hjFirstSeen': '1',
        '_hjIncludedInSessionSample': '0',
        '_hjSession_3321793': 'eyJpZCI6IjVhYTQwZDc5LWEzNTEtNGRiNy05NDk0LTkxZjMzYzU1ZWM1ZCIsImNyZWF0ZWQiOjE2NzUyNjMyMzA5NDQsImluU2FtcGxlIjpmYWxzZX0=',
        '_hjAbsoluteSessionInProgress': '0',
        'crisp-client%2Fsession%2Fad02dfcf-7460-460d-bc6d-658345899d51': 'session_00243d91-70e3-4c8c-80ae-b93cb4f0019b',
        '_hjSessionUser_3321793': 'eyJpZCI6ImEzZmM1YThkLTc5YzUtNWQ5NS1hZmIyLTlhODYzZDNhNzYxNSIsImNyZWF0ZWQiOjE2NzUyNjMyMzAwNTksImV4aXN0aW5nIjp0cnVlfQ==',
        'session': '7cb761b3794ed963e770a035757413daTXf5N6YzbWYuvSxFqGmR2ZMcou682B1rphAMjpbd9fN2tKfxxXFBDE9ByEvSmy6t2%2BWBuvXzF%2BJjN7EoiMVTVgTvaycmrPWdy4M10Ng9KnB2rgJcAdj7idiOmRHvkDwY',
        'XSRF-TOKEN': '2a3f25cf033a957367ca5d358b348841Ri4Cq5NM1mCc9qfEvdNJbFw6q0atr0wPBGcJvcVTWZQriIJ3W7VoWDqMmE%2FrxUgdE0GAP3rOpOiKCbHyEPxQ18oM%2Bg5NTq6BfZIMl8K9odU5M4qROMJwjF1KzIAEvdu%2B',
    }

    self.headers = {
        'authority': 'pickaw.app',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9',
        'referer': 'https://pickaw.app/me/contests',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'x-pickaw-version': '1.24.11',
        'x-requested-with': 'XMLHttpRequest',
        'x-websocket-id': '-OJgpTn_a6aSM1qvACp8',
        'x-xsrf-token': '2a3f25cf033a957367ca5d358b348841Ri4Cq5NM1mCc9qfEvdNJbFw6q0atr0wPBGcJvcVTWZQriIJ3W7VoWDqMmE/rxUgdE0GAP3rOpOiKCbHyEPxQ18oM+g5NTq6BfZIMl8K9odU5M4qROMJwjF1KzIAEvdu+',
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
