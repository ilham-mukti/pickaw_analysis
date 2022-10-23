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
        '_ga': 'GA1.2.1652170695.1666508161',
        '_gid': 'GA1.2.722014581.1666508161',
        '_fbp': 'fb.1.1666508161309.556427539',
        'crisp-client%2Fsocket%2Fad02dfcf-7460-460d-bc6d-658345899d51': '1',
        'registration': '13e2fd90f8c5d3a9e457a8b57298ad945tyUJTraRvm1%2FdruRU4fDxWz1Oy3w5ZN0ZA7ZtpoqPLSCyMAfn1TgybvYmYZhkU7sYqHEvrskv%2BwjIwu%2BgsMkOhovx%2FdgJ%2F1f6Vkw2FniEpp196k%2FQ%2FrqoezgZVED2sF7SwS4bHbl9%2BVSy3vu%2F%2Fm35cwz0U5jrRnAnw%2BHY1antibrGVr989X2ADQzJhTnilzEj10fztTQT7%2Bm6phghfCsZY9JdDC%2FbN4m329aFbcDo%2B7WLruMhX3Qcljd%2Ff9RhYDCk5wXGPZ7qVzDSJZEdwZSIkBGWovDW1L8QA6it3HQuBX4MaenKF34lxM0t6LH6Cujrn5sGGbrec%2FPxSFXo0bP3njUaIiNtcfSLBaVC6I46RKkv2drs2PGsHaY3mUZji3bvYOrdm3Z%2FqmkZYfZopLf6bnAkWxd%2BZpbH94oC14tZgBYv5tE9Gy7GbUac2ssP8sbbe3lnELOJ%2FFTqhMqFzvsBrqHw5XtUd6wbAzUl5KdXdTJYJi888QzML19srDjJRwNVuxbMOLtXfverJqnRkkckQ2R4cJeS%2BYzGs02ayWhaVDunMQX%2FgSd9tlDc1Wy3cytJXBbLxiiMf6hphWAAmysVqN%2BbKYJO05HQ3kBswevyfWuYtSFR41i7qNNb2eVrIKxiByZFRVbM5DVj%2FtrIfrAk%2FbMohwLjH6XfqN3S8Yw1Z7DJU%2Bv14gFj7Zfhf5x6%2BGNDHPHdQTarBUFqMhYMYXCoPqiEgL%2F6ZvRLK9dYgJXBQ2xuJX%2FQhl45PgDGFJr6U1Gw%2BqWrHe3%2BVIODHbAyDT%2Fs4nDqFR%2FFeg8rf3TKMr2GERcndRuzSqmkPVzHjl3R%2BKFozZoSI1NuUjdWpd3Rgmww%3D%3D',
        'crisp-client%2Fsession%2Fad02dfcf-7460-460d-bc6d-658345899d51': 'session_8540b413-3498-4097-9bec-facc26ceb220',
        'session': 'ec815007366df03f520a6cb678cda2e2T8yja7kLcSI%2BQirarce1jU4ZMsWsTVqrpqXjaG6u2%2BSm4Wy%2FPa44TVrzjJwxH5AsYTK8qKFpiV6rbIK4mIREBsNG13INccUNU6g5DeXKsLiCfEksWOVV32oXld%2FR3Q07',
        'XSRF-TOKEN': 'cf79548b0d04a303f2394fb5e44af5efMNtDGl2LqIUvKvhK2IBAZMG5JQQVukWmdIUCOb%2BAGnATSK0%2FHzrrhLnNKZv4nIQwynmWjazJY2q%2FFjF%2BKRdc3Fmvu1%2FcE%2BlDQ4yMDT3idH%2BrcaUVImCwCuAovHH%2FBI5P',
    }

    self.headers = {
        'authority': 'pickaw.app',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9',
        'if-none-match': 'W/"26d2-QMQgpqhhkFbHADce2RgFqxuDlWk"',
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
        'x-websocket-id': '4aArsnUJICXyIMcYATOU',
        'x-xsrf-token': 'cf79548b0d04a303f2394fb5e44af5efMNtDGl2LqIUvKvhK2IBAZMG5JQQVukWmdIUCOb+AGnATSK0/HzrrhLnNKZv4nIQwynmWjazJY2q/FjF+KRdc3Fmvu1/cE+lDQ4yMDT3idH+rcaUVImCwCuAovHH/BI5P',
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
