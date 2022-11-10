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
        '_ga': 'GA1.2.446364208.1668063435',
        '_gid': 'GA1.2.1117744384.1668063435',
        '_fbp': 'fb.1.1668063435998.1574362805',
        'crisp-client%2Fsession%2Fad02dfcf-7460-460d-bc6d-658345899d51': 'session_48cab73f-5712-45dd-be34-269a84145b25',
        'registration': '9db9df5915c88c1a2404cefa43ab879eHVABF27fxqz1GI6NNE5QGLUCCSRcsEBKr6oW4MxhngIriMXKG62U2fVgCz47r%2FyJx5jxlCKqY5wD%2FGOliYKlMiqYG3cUQK94qUFvcGRxiZA%2BRtTuqIEL91wzED4pZvSeoxx8Wo87u5NuWLZA83iFQnnztMKpYh%2Ff%2FpLIrxHFNego4o%2F%2B%2BUkUAni5fHfRmsBnfPZUyr3Od9wQuI3KghLCXdXK5MuyL9zJlZgNOCD%2FMXR%2FXuntfHRucnwrbNpwokgu54KDILNMoXszjvOM4arJItBiqE9YY1jCJ%2BECoOp9u96Daunmwpcpm8nDLbQJQqFfaOu08f1w2yyndQoS%2FwqWqi1fQPxneQQOoeQYXFLTYfip%2FZQwJglW%2BvzOvVzkncjaGIaeZtqZevZXdZiI1oIyK2UbaRGZjf%2B43eO0ynTVe7BbCkTdWT2u4NDDpWEp8BR%2BVhyzRl85gy4QTRIO3CYTriYrWauu74Rkhx%2Fd9GCiitooDi9haJLtoodM0Lk%2BgnnDaCJDwwd0lkn9CEwexUlMSRTjA8vq9wDR2CmTZpbbcYkqLa2JgjjT%2FsIqE%2FuhJbqPktJ0%2BnNMs504aDn2yFCCy4KXtLhc6s%2B2QMHl0xX1BjaAN%2BATeEXSKkuubhpcrpv9vbXegEQo5BG0ZZfj03mTYPUKA%2BBc5V%2B6Ep%2FVi0jQk2gkc0pazM91vrjppynWv6EAl8jSEwZJ6OZtRuARwz%2Bb2cmHTCuxM9Wa9N1xhAW37bsiRyebxVDRCeW%2BdW3%2Bdv1Ktc9dF0bv1dgjaRiQHJkrWf2iTmhlf03%2Fu9%2BJY8Fd9GPDwYVdkPZO53rFsNNXgV8wHr%2FeuESbde85P8oQej%2Bt2g%3D%3D',
        'crisp-client%2Fsocket%2Fad02dfcf-7460-460d-bc6d-658345899d51': '1',
        '_gat': '1',
        'session': '425c18f98bb263b20cc49c008c6752c2Xbi%2BfiGwJGKUFgK9QHSiygiFokqe2nbYcOOvfqN%2FMyWMIUvuz7yP9O6bTlKG25bKugPFjnSN12oa8T6P7nq9EGY1V57gwLs3qE1jNL%2BnwQLcyFrsL%2BoYIchscurZUeWn',
        'XSRF-TOKEN': '070db65ed26acca8dbc651a03f3e0894%2BlDL2iTGTEL25q3oNeLMtkhOpE2JQfOJaZr70eq3hPcHLjaEOWR%2FUKt5OJqeGNXxrWBEt7hWfwbdvoatD7kRJc4BLelK4tV0YU40d0GXP%2B6Np7Yv%2Bxxf05nDLx9gBwfn',
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
        'x-websocket-id': 'to8YijX_7EyApLxrArDy',
        'x-xsrf-token': '070db65ed26acca8dbc651a03f3e0894+lDL2iTGTEL25q3oNeLMtkhOpE2JQfOJaZr70eq3hPcHLjaEOWR/UKt5OJqeGNXxrWBEt7hWfwbdvoatD7kRJc4BLelK4tV0YU40d0GXP+6Np7Yv+xxf05nDLx9gBwfn',
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
