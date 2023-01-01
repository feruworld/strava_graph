import os 
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

input_filename = '../data/activities.csv'
output_dir = '../results'

df = pd.read_csv(input_filename)

df['キロ時間'] = df['経過時間'] / df['距離'] / 60
df['ID'] = df.index + 1
df['アクティビティ実行日'] = pd.to_datetime(df['アクティビティ実行日'])


# 横軸範囲
sxmin = '2022-06-01'
sxmax = '2022-12-31'
xmin = datetime.datetime.strptime(sxmin, '%Y-%m-%d')
xmax = datetime.datetime.strptime(sxmax, '%Y-%m-%d')

# 縦軸範囲
pacemin = 4.55
pacemax = 7.20

# 全データ推移
fig, ax = plt.subplots(figsize=(20, 4))

ax.plot(df['アクティビティ実行日'], df['キロ時間'], marker='.')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d')) 
ax.set_ylabel('min / km')
fig.autofmt_xdate(rotation=45)
output_filename = os.path.join(output_dir, 'time_per_kilometer.png')
plt.savefig(output_filename)

# 全データに色を付けてみる
fig, ax = plt.subplots(figsize=(27, 6))

ax.plot(df['アクティビティ実行日'], df['キロ時間'], linewidth=0.5, color='gray')
sc = ax.scatter(df['アクティビティ実行日'], df['キロ時間'], c=df['距離'], cmap='Set1', edgecolors='black')
fig.colorbar(sc, label='km')

# 特定の日付に線を入れる
markered_days = ['2022-06-12', '2022-07-14', '2022-08-21', '2022-09-25', '2022-12-10', '2022-12-15']
for day in markered_days:
    x = datetime.datetime.strptime(day, '%Y-%m-%d')
    ax.plot([x, x], [pacemin, pacemax], linewidth=0.5, linestyle='dashed', color='gray')

ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d')) 
ax.set_ylabel('min / km')
fig.autofmt_xdate(rotation=45)
ax.set_xlim(xmin, xmax)
ax.set_ylim(pacemin, pacemax)

output_filename = os.path.join(output_dir, 'time_per_kilometer.png')
plt.savefig(output_filename)

# 5kmのみ
df_5km = df[(4.9 < df['距離']) & (df['距離'] < 5.1)]

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(df_5km['アクティビティ実行日'], df_5km['キロ時間'], marker='.')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
# ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=7, tz=None))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax.set_ylabel('min / km')
fig.autofmt_xdate(rotation=45)

output_filename = os.path.join(output_dir, 'time_per_kilometer_5km.png')
plt.savefig(output_filename)


# 10kmのみ
df_10km = df[(9.9 < df['距離']) & (df['距離'] < 10.3)]

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(df_10km['アクティビティ実行日'], df_10km['キロ時間'], marker='.')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
# ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=None, interval=7, tz=None))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d')) 
ax.set_ylabel('min / km')
fig.autofmt_xdate(rotation=45)

output_filename = os.path.join(output_dir, 'timeperkilometer_10km.png')
plt.savefig(output_filename)


# 5km and 10km

fig, ax = plt.subplots(figsize=(12, 4))

ax.plot(df_5km['アクティビティ実行日'], df_5km['キロ時間'], marker='.', label='5km')
ax.plot(df_10km['アクティビティ実行日'], df_10km['キロ時間'], marker='.', label='10km')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d')) 
ax.set_ylabel('min / km')
ax.grid(axis='y')
fig.autofmt_xdate(rotation=45)
ax.legend()

output_filename = os.path.join(output_dir, 'timeperkilometer_5-10km.png')
plt.savefig(output_filename)


# 距離

fig, ax = plt.subplots(figsize=(40, 4))

ax.set_yticks([0, 2.5, 5, 7.5, 10, 12.5, 15])
ax.grid(which = "major", axis = "y", color = "gray", alpha = 0.5)

ax.bar(df['アクティビティ実行日'], df['距離'], width=0.75, ec='black')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d')) 
ax.set_ylabel('km')
ax.set_xlim(xmin, xmax)
fig.autofmt_xdate(rotation=45)

output_filename = os.path.join(output_dir, 'distance_bar.png')
plt.savefig(output_filename, bbox_inches='tight', pad_inches=0)
