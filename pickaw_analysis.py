import requests
import pandas as pd
import os 
import ast
from datetime import datetime
from pytz import timezone
import json

class PickawContest:
  def __init__(self):
    self.output_file = "list_pickaw_contest.csv"
    self.seed_list = "seed_list.json"
    self.cookies = {
        'i18n-lang': 'en',
        '_ga': 'GA1.2.908142620.1664860279',
        '_gid': 'GA1.2.1394393021.1664860279',
        '_fbp': 'fb.1.1664860279910.400619248',
        'crisp-client%2Fsession%2Fad02dfcf-7460-460d-bc6d-658345899d51': 'session_10a4289d-c94f-473e-9d0a-8a690793e675',
        'crisp-client%2Fsocket%2Fad02dfcf-7460-460d-bc6d-658345899d51': '1',
        '_gat': '1',
        'session': 'a47a21556d64a6e9438080703024d0f70%2BEMjmvsElAOYJDXEabQP%2FiemN0LHRdQW4gFbhoNnKF40Mm7yL7D7myEuq7CwT3orfnUAk4GJUJxtwBMIDf76M2KsivhHbG1FCnsULyMj3wxdevY9J3evbrqfvDUQL4y',
        'XSRF-TOKEN': '95fc6fd1e8a71870e41cc33ff4fa309eka0uDKVWhA0ickjZpsHuLhg0A%2FidsUXPgmhkNGDZhLaDRa8qOiI1kDY38UIdwl3vJ1swAHZzzyP5ltGqPhcF7OubniiaUnpn%2FTXr2aDotATByMMrNjXvON4TBlsdUdk3',
    }

    self.headers = {
        'authority': 'pickaw.app',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9',
        'if-none-match': 'W/"3ac8-VZ/y3GoEVHf/Z+TqnYsgk68AR0g"',
        'referer': 'https://pickaw.app/contests/check',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'x-pickaw-version': '1.22.0',
        'x-requested-with': 'XMLHttpRequest',
        'x-websocket-id': '',
        'x-xsrf-token': '95fc6fd1e8a71870e41cc33ff4fa309eka0uDKVWhA0ickjZpsHuLhg0A/idsUXPgmhkNGDZhLaDRa8qOiI1kDY38UIdwl3vJ1swAHZzzyP5ltGqPhcF7OubniiaUnpn/TXr2aDotATByMMrNjXvON4TBlsdUdk3',
    }

  def request_data(self, pages):
    my_dict = {}
    for page in range(1, pages):
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
    return dict_baru

  def get_contest(self, pages):
    is_new = not os.path.isfile(self.seed_list)
    if is_new: #Jika baru
      print("bikin baru")
      data = self.request_data(pages)
      self.create_file(self.seed_list, data)
    else:
      print("sudah ada")
      data_baru = self.request_data(pages)
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
    self.update_readme()


  def save_to_dataframe(self, my_dict):
    df = pd.DataFrame(my_dict, columns=my_dict[0].keys())
    df.to_csv(self.output_file, mode='a', index=False, header=not os.path.exists(self.output_file))
    return df

  def create_file(self, name_file, data):
      f = open(name_file, 'w')
      f.write(str(data))
      f.close()
      print("selesai")

  def update_readme(self):
      jkt = timezone('Asia/Jakarta')
      now = datetime.now(jkt)
      with open('README.md', 'w') as f:
         f.write(f"# Data tanggal: {now}\n\n")
         f.close()

model = PickawContest()
seed_code = model.get_contest(pages=3)
model.get_winners(seed_code)
