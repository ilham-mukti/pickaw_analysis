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
        '_ga': 'GA1.2.511745224.1666173838',
        '_gid': 'GA1.2.1358129550.1666173838',
        '_fbp': 'fb.1.1666173838731.2809702',
        'crisp-client%2Fsession%2Fad02dfcf-7460-460d-bc6d-658345899d51': 'session_cf119850-771e-4636-a963-571863ee31a6',
        'registration': '86a719bcb494a956865de1a35a2c9a06qS4fAZm%2FLIXoMhbZzQFM1IgWwsXC2ibXKYkubFed%2Fkw2VOTTyDlSFFu4%2FqOeenwxSRCTFEerPg4jvAVp6IoJ%2Byo6GTgSK5MpUNlVBeo6YuhVIyxD0%2Fp7tiH8rV%2B0X1zu9RM61MqNDp2z3MvnRh1PL%2Bot9ZzXEqD8OXDDoWdMI4NtcAZRWtMaOJ5rjCBxo525Pirk0zcZYJs7r2D7KMa%2FakcrWpjLbAH1I5omRwON0Q6mpfMdBk5eG3noCxIJ7fCE1w7njm3w0GQ7iCXTKTMGY%2FqqW78XDMGpuQmPY7P8F02dt0Dbgoqk5HXkifUWaMPFw6W37PCQATnORn5fxOFdNNQyRW03xmy2EivABOluxOy4JvVXtwNSx0kf7it4oolyRh7M1Hb9wj%2FFPsVmXn8QiqSViAcSxZdoR7t9rQPDu%2BmkvQPC8uyCRpI9%2FRNmN4BgyBJY%2BVsPeVxOclvfKHjVMRlxhWhYFC6PcX%2FHfjM8UwchAanavN%2BIA18kADfd9X5V4QWIznOr9hskp0Xc7EQFwFmPXGE%2Fc7vuZW8ndGT1zJpAYzq6Nodw4r5pYxiaAccNGgwfUw4R7nSLJ2yoW%2B4BijwYtT9FuI3tcSigoZLWc8CCJ4uRCIyEmgPmI5iOYC5wuWntYDZ583cEZx%2Bqk5u1wVvKxJbz%2FSIqH6VVpPGkFvr4h%2FcJyeU8Al9Exk%2BHinmWMLcc1BHfC3BvfpzUQu8lAbdTAmkAJroXhtaXGajSqQt5r3fEtTgWKnvNNPYTKe%2FeuHc8G%2BCQ6QJGtJYJ9oXmY3vAaAfNuNmlF2RH8L%2BYGKdL2tfH%2Bb960kyL1%2BPsIK3qBX%2BowoNcIgYmJ9cJP26Mz4ij5k0DbbVFqFpZK%2Bv7Iok%3D',
        'crisp-client%2Fsocket%2Fad02dfcf-7460-460d-bc6d-658345899d51': '1',
        'session': 'f1e1897fb589f2e6807a85f4cdb1a93eoUhOzVlQINqFxuRtm7g0XaFQng%2FnhdT0bVgyDxKzvtX%2F%2FM%2BQYywYT6FVVj3sYKX3QzaQLOvUMD0gcZ54IKeXAaRoMCko5ocuAw1XDw%2BSDG%2Byl5GoxethTWyaa%2Bfh5QOg',
        'XSRF-TOKEN': 'f949c10a37fc9d5e33b670e20d7cffff4iiiWlWfgMNVRSLQim4eeAw2%2FcwEek4d10s7yOQWafjuu6o2aubLWub5MTaKvU2whu5Fyu4AMrnyz15qmuvdDJuz1n2oDIt6qFr6SNgTDHwNLZEie73sQFB3buoE4Ek2',
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
        'x-websocket-id': '__OD71aqEw63_JGdAHgr',
        'x-xsrf-token': 'f949c10a37fc9d5e33b670e20d7cffff4iiiWlWfgMNVRSLQim4eeAw2/cwEek4d10s7yOQWafjuu6o2aubLWub5MTaKvU2whu5Fyu4AMrnyz15qmuvdDJuz1n2oDIt6qFr6SNgTDHwNLZEie73sQFB3buoE4Ek2',
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
