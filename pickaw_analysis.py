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
        '_ga': 'GA1.2.926523033.1667389426',
        '_gid': 'GA1.2.1172006335.1667389426',
        '_fbp': 'fb.1.1667389426426.755417775',
        'crisp-client%2Fsession%2Fad02dfcf-7460-460d-bc6d-658345899d51': 'session_640c82e3-6369-4a11-8213-f77041d42dff',
        'oauth_state': 'af239eef97f3998c9633b4f52510c666qdWJjxO15bD4sJEDeR3cftBT%2F7pcrHtn2nb1URDbDQv7coFancCmXcm409xHmd33JdKnhWwQzrYd1uiTBvKfElD5XVlfaNHkLZILq6REDQBsL6sEbBStLmk4MdjpQCgC',
        'registration': '3e956366373e343fdfb3c57fdb1e2e2bsxUyhtV9cx9mBrdkASW5jzvxUJQWFrR2z1ZTmztbV1vH6T1DZMxJL6FGp%2Bi%2Bs5oPYAZu3adVbrkWvVEj%2FvwWpkSxRq2gy4Ry7d48dVLyePaajy2hvnCygXjC7FP%2BSTJBEoH%2F8bF10530ggVwvLcmK8qx3fVVB1oCHHoFM8xp%2BHqFJMXh86KkXHTYDwFHE%2BAmTbCCaDPDgwpUXwGFc8UZrbEmQqfGPVnoIvNjiHs8loeJy5sY39wZ3%2BVHa3D67CaRtKeWcfhii4HnOwaRvzDDycqi%2FJ25ydEj4nSVayl9A%2FzymhCe%2FmzRItvBmaWouau0guzclPUq%2B4%2Bj5fQ4XIIgyEUypwaruJKfTtZ6uff9X7mPAQB9FjixRafnFjlOVzWH9CPUdJqD1tCpF6RlIDgBb4NbFgZ1Q7lPtQC969Gkbip5jF31VJJP7YxvIWAUpIMaUZ6NkSQDjySPUioAKBcgEmh7%2FlPT3UBnx8MYtitW%2BIdysOJv5Q7UfN%2BhJk8axKH4nnSMVssuFbEQvFxKJ6WmUd2GEjHSPCuvH5iNO4W%2FnRtIXOw2GWM1nnTE8rd7IOEumlFl%2B9Ax%2FJEw1%2BxFjpb2YTp3sdAQ8slHTJGNMmplhxBFZ78sgvxb4InsolysK3oNSJyhqVLRoG6kOtpjM8LwMHF1g7cUSdf3d%2BLiCtFWEp0Wz3NbAfGTIkYlhnrRS%2B5mi6bd43YZvHeOogHTNR0F1WzDxq%2FHPNu4v1ZUgitTrXiu6k2y5ANMaam5fAR3Z1oMUQSfUaoZ4G4%2FmtBDjhQUfILAI3pPzyld6qB1hq3%2FNsWS1nYpdsJtTRPtwSbs381RL%2BI2niR04eSsiWFS3XRg9A%3D%3D',
        'crisp-client%2Fsocket%2Fad02dfcf-7460-460d-bc6d-658345899d51': '1',
        '_gat': '1',
        'session': '39646f0484dc0d02974f51ef4f56d9c3khQyTIvmrz0PiETETW%2F2RLjiN0VtyE5RThhKcG3liQg1LUFN4dVUCgHDr29syBrDB%2BYaBpYLOJ0E%2BdSD%2FN0hTytrm%2BDXgcyp9YANuwl40GBjOKuoQrCUOA3Fqb%2FIDmRV',
        'XSRF-TOKEN': '2f8ff4b0aca423d1bb5b71524104011fGxNob2FIY%2BNnzx0%2F%2BcvTnsLeJRuWNpjBxeft%2FINcNzJY5AtUHywulMyImvKjKsnISDnVrg208Et8Yb7dbxqn2h8hROQXR93g%2BqJ7o2A2hOcoZIQGLGb0ymYxMiWsoH06',
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
        'x-websocket-id': 'U2aHMAr1MxOxkqtDAR4O',
        'x-xsrf-token': '2f8ff4b0aca423d1bb5b71524104011fGxNob2FIY+Nnzx0/+cvTnsLeJRuWNpjBxeft/INcNzJY5AtUHywulMyImvKjKsnISDnVrg208Et8Yb7dbxqn2h8hROQXR93g+qJ7o2A2hOcoZIQGLGb0ymYxMiWsoH06',
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
