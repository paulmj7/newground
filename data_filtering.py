#%%
import requests
import json
import pandas as pd

headers = {'Content-type': 'application/json'}
#api_key = [enter key here]

def get_json(url):
    req = requests.get(url=url, headers=headers)
    return req.json()['results']

#%%


#%%
def get_df():
    url = 'http://api.reimaginebanking.com/enterprise/customers?key=' + api_key
    X = get_json(url)
    addresses = [cust['address'] for cust in X]
    X = [{k: v for k, v in d.items() if k != 'address'} for d in X]
    X = [{**d1, **d2} for d1, d2 in zip(X, addresses)]

    #%%
    cust_df = pd.DataFrame(data=X)


    #%%
    url = 'http://api.reimaginebanking.com/enterprise/accounts?key=' + api_key
    X = get_json(url)

    #%%
    acc_df = pd.DataFrame(data=X)
    merged_df = pd.merge(
        cust_df,
        acc_df,
        how='inner',
        left_on='_id',
        right_on='customer_id'
    )
    mask = (merged_df['type'] != 'Credit Card') \
        & (merged_df['zip'].str.match(r"\d\d\d\d\d"))
    return merged_df[mask]

#%%
def filter_by_income(merged_df, min_balance=1000, max_balance=10000):
    mask = merged_df['balance'].between(min_balance, max_balance)
    filtered_df = merged_df[mask]
    return filtered_df

#%%
def filter_by_state(merged_df, state="North Carolina"):
    mask = (merged_df['state'] == state)
    filtered_df = merged_df[mask]
    return filtered_df

#%%
def filter_by_zipcode(merged_df, zipcode="27514"):
    mask = (merged_df['zip'] == zipcode)
    filtered_df = merged_df[mask]
    return filtered_df

#%%
