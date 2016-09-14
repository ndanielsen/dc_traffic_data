
# coding: utf-8

# ## Loading Parking Violation Data and cleaning operations
import pandas as pd
import glob

files = glob.glob('./parkingdata/**')

parking_violations = [f for f in files if 'parking_violations' in f]

### Combine all csvs into one data frame

list_ = []
for file_ in parking_violations[:]:
    df = pd.read_csv(file_,index_col=None, header=0)
    filename = file_[len('./parkingdata/'):]
    df['filename'] = filename
    list_.append(df)

frame = pd.concat(list_)

print('concat-ed all files')

# TESTs
assert frame.filename.nunique() == len(parking_violations)
frame.columns = [col.lower() for col in frame.columns]
frame = frame.reset_index(drop=True)
df = frame.copy()

### Construct datetime object from issue_time raw string

def mil_to_time(x):
    "Convert messy issue_time to datetime object based upon length of issue_time string"
    if x == 'nan':
        return '00:00:00.000Z'

    x = x.split('.')[0]
    lg = len(x)

    if lg == 4:
        t = x[:2] + ':' + x[2:] + ':00.000Z'

    elif lg == 3:
        t = '0' + x[0] + ':' + x[1:] + ':00.000Z'

    elif lg == 2:
        t = '0' + '0' + ':' + x + ':00.000Z'

    elif lg == 1:
        t = '0' + '0' + ':' + '0' + x + ':00.000Z'

    else:
        t = '00:00.000Z'

    # correction for timedate if one element is greater than 5.
    # double check this
    if int(t[3]) > 5:
        t = t[:2]+ ':' + '5' + t[4:]

    return t
print('converting datetime')
df['issue_time_military'] = df.issue_time.apply(str).apply(mil_to_time)
dates = df.ticket_issue_date.str[:10] + 'T' #+
df['ticket_issue_datetime'] = dates + df.issue_time_military


### Optional Test that datetime contruction is correct

### Holiday value to Boolean

df['holiday'] = df.holiday != 0

### Delete redundant columns

del df['day_of_week']
del df['month_of_year']
del df['week_of_year']
del df['issue_time']
del df['issue_time_military']
del df['ticket_issue_date']


### Drop Duplicates and Fill in Empy Rows

df.drop_duplicates(subset='rowid_', inplace=True)
df.streetsegid.fillna(0, inplace=True)


df.to_pickle('parking_eda.pkle')


### Export to CSV
print('preparing csvs')
df.to_csv('./cleaned_data/clean_parking_violations.tsv', sep='\t', index=False)

df.sample(10000).to_csv('./sampled_data/clean_parking_violations_10k_sample.tsv', sep='\t', index=False)

df.sample(100000).to_csv('./sampled_data/clean_parking_violations_100k_sample.tsv', sep='\t', index=False)

df.sample(1000000).to_csv('./sampled_data/clean_parking_violations_1million_sample.tsv', sep='\t', index=False)

