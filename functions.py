import pandas as pd
import numpy as np

# changes string to date
def str_to_date(x):
    '''This function changes string to date. 
    Required string format: ('%Y-%m-%d')'''

    from datetime import datetime
    x = datetime.strptime(x, '%Y-%m-%d').date()
    return x



def uniques_users_daily(df):
    '''This functions filters table based on unique
    combination of date and id'''
    
    uq_user_daily = df.drop_duplicates(subset=['user_id', 'time_stamp']) # ensuring that one user is counted only once a day
    uq_user_daily = uq_user_daily[['time_stamp', 'user_id']].sort_values('time_stamp').reset_index(drop=True) # cleanup

    return uq_user_daily


# calculates retention for a given dataframe
def retention_calculator(df, show_no = False):
    '''This function calculates retention_rate, 
    and returns DataFrame in format (date, retention_rate)'''
    
    from datetime import timedelta

    # Selecting dates to calculate the retention for
    dates = np.sort(df['time_stamp'].unique())[:len(df['time_stamp'].unique())-3]

    # List containing lists: [date, retention_rate] 
    retention_list = []

    for i in dates:
        # Day that I'm calculating retention for
        day_0 = i
        # Last day for the user to return in order to be included in retention
        day_3 = day_0 + timedelta(days=3)

        # Users who visited the page in a given day
        users_day_0 = df[df['time_stamp'] == day_0]
        # Users who visited the page in next 3 days
        users_up_to_day_3 = df[(df['time_stamp'] > day_0) & (df['time_stamp'] <= day_3)]

        # Loop calculating retention rate
        returned = [] # list of 0/1 values (0 - user has not returned, 1 - user has returned)
        for i in users_day_0['user_id']: # for every user in a given day
            if i in list(users_up_to_day_3['user_id']): # check if this user is in users who visited the page in next 3 days
                returned.append(1) # if yes, append 1
            else:
                returned.append(0) # if no, append 0
        retention_list.append([day_0, sum(returned), round(sum(returned)/len(users_day_0)*100, 2)])

    col_names = ['date', 'returned', 'retention_rate'] # colnames for result DataFrame
    retendion_df = pd.DataFrame(retention_list, columns=col_names)
    retendion_df.set_index('date', inplace=True) # setting date to index
    
    if show_no==False:
        retendion_df.drop(columns='returned', inplace=True)

    return retendion_df