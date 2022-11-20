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
        'crisp-client%2Fsession%2Fad02dfcf-7460-460d-bc6d-658345899d51': 'session_8f0c6528-cdc5-410a-b2a8-4fdf36761cd0',
        'registration': 'acf35034dff90f381b14fb3aac34c079aKf5xxRxwEnDozIO80V1LPN4fTdCptpysKs89wzWcDw7uRA2qObH4wqfOGamSXQUumB%2B9zpjrQaupyhoW46ZcC4D%2BWZ%2BzCNK%2FMlY3xH5Wqpi2bfGFys0N0wufKH4kyXTc9Aq%2B27yXflmNrYzfEpcSa3%2B%2BKQ24XnobqVoHY0P9psyJzkQk3mnTWZGIMQCVd6Xyerfg7oqmBTklGDGb2CyyPFdPY8%2BDwMNKxGferQ6xaN0gGxzU0a%2FUg%2Fn2dGPEOp428YG96o3y0cVrIHLcrId2tlrUjRbKxXe8w20fvEQ%2BnhnI8VWnwBoq%2BDlybMuvLKpoOLKPu9GSSmbzrRIRcdw82i977aK5Wq1WOMRVWD9vkCA7NGHwId4djGWl9VKHDA%2BDSPEMHDmRSjec6IjIoq2P7cIRzBX%2FipR6RR1aybWaLLvRSvM6h%2F%2FXyICqysnOEIQXU4DzXnyr8kXI3nAn%2FttCTGFp5dNwP0feU2iz%2BuC1NbbiHyCRBlC504lNxfOIRc5t4EsnPgz12nqxglhaQ5VqjEglSYbowjdLMqzr6L38%2BEI8BhwtdjDZNk7aHVttJkZ8u98AmtjJyhsrNmuo9Y18OH2f%2BbMd9QFPRQlE6KJHjqXiIteKXjJ%2BGJwB3afqxiHmY9Nn1KoEtWOhgNKFeH%2BCYG5PGWdLNXkwyOjevfp83Fi9Z9cvyz2mc%2FLY4U%2BuF08ZBx2YGsb7%2BnEkfXn7Z2%2B2WxRvR8amLUGjJnVRiAQIO5esZ71i4T4nQ0eGe0JCu6WwQagHtWjqtyhm%2BvsYWlarxilX7%2BlflT2BVyNl%2F5Jb5KCQ%2FzGoRxvB2W3lrYTp%2FHhCbglVtkMIgLo5cIfP120VfVkt1D1fBVx3QccfGSPBaM%3D',
        'crisp-client%2Fsocket%2Fad02dfcf-7460-460d-bc6d-658345899d51': '1',
        'session': 'ea46b8b6fc358c357724e614596ba407EdwG7yON1Gih%2BdyHpGgBjNTbRUE6xb6W5vYOPjGSs0StEMBfDjAzFjRCLn80dKfmQwfDxYkoe0Y6cgM%2BhU8USfGqwHQ2POxmSBz2kcVTmv4xCZLUy8tJ3or34v5oo9Tx',
        'XSRF-TOKEN': '20a871b3ec1f6f00efe1198b8df3639buDXkkL%2BcxuhhzQ9beVeZAru6dYPZiDanwV6WL5Tr%2FclQjgoViA8hDiD8opB5pswsjAQ4MTWMX4qeD%2FNI0mSXe15pT5N5hIEblBffUfpD1d%2BgbuXMrVoS3uv9%2BxVhETaY',
    }

    self.headers = {
        'authority': 'pickaw.app',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9',
        'referer': 'https://pickaw.app/me/contests',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-pickaw-version': '1.23.1',
        'x-requested-with': 'XMLHttpRequest',
        'x-websocket-id': 'XVrjeaRA6YMhX3SnAbfX',
        'x-xsrf-token': '20a871b3ec1f6f00efe1198b8df3639buDXkkL+cxuhhzQ9beVeZAru6dYPZiDanwV6WL5Tr/clQjgoViA8hDiD8opB5pswsjAQ4MTWMX4qeD/NI0mSXe15pT5N5hIEblBffUfpD1d+gbuXMrVoS3uv9+xVhETaY',
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
