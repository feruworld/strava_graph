import gpxpy
import gpxpy.gpx

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib


def hyubeni(rlat_a, rlat_b, rlon_a, rlon_b):
    # ヒュベニの公式により緯度経度から2点間の距離を計算

    A = 6378137.000  # WGS84測地系の楕円体の長半径a
    B = 6356752.314  # WGS84測地系の楕円体の短半径b
    E = np.sqrt((A**2 - B**2) / A**2)  # 離心率
    Dy = rlat_a - rlat_b  # 2点の緯度(latitude)の差 [rad]
    Dx = rlon_a - rlon_b  # 2点の経度(longitude)の差 [rad]
    P = (rlat_a + rlat_b) / 2  # 2点の緯度(latitude)の平均 [rad]
    W = np.sqrt(1 - E**2 * np.sin(P)**2)
    M = A * (1 - E**2) / W**3  # 子午線曲率半径
    N = A / W  # 卯酉線曲線半径
    D = np.sqrt((Dy * M)**2 + (Dx * N * np.cos(P))**2)
    return D  # 2点間の距離 [m]

# class Song:
#     def __init__(self, name, length, bpm):
#         self.name = name
#         self.length = length
#         self.bpm = bpm

with open('../data/20230108.gpx') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

route_info = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            route_info.append({
                'latitude': point.latitude,
                'longitude': point.longitude,
                'elevation': point.elevation,
                'time': point.time
            })

print(len(route_info))

route_df = pd.DataFrame(route_info)

plt.figure(figsize=(14,8))
plt.scatter(route_df['longitude'], route_df['latitude'], s=5)
plt.savefig('../results/route.png')

# 走行距離と時間の差を計算
distances = []
times = []
velocities = []

for i in range(len(route_info)):
    if i==0: distances.append(0); times.append(0); velocities.append(0); continue

    rlat_a = np.radians(route_info[i-1]['latitude'])
    rlat_b = np.radians(route_info[i]['latitude'])
    rlon_a = np.radians(route_info[i-1]['longitude'])
    rlon_b = np.radians(route_info[i]['longitude'])

    distance = hyubeni(rlat_a, rlat_b, rlon_a, rlon_b)
    distances.append(distance)

    time_diff = route_info[i]['time'] - route_info[i-1]['time']
    times.append(time_diff.seconds)

    velocities.append(distance / time_diff.seconds * 3.6)

distances = np.array(distances)
distances_cum = np.cumsum(distances)
print(distances_cum)

# 累積距離グラフ
plt.figure(figsize=(14,8))
plt.plot(distances_cum)
plt.savefig('../results/distances_cumsum.png')

# DataFrameに進んだ距離情報と時間の経過を追加
route_df['distance_delta'] = distances
route_df['time_delta'] = times
route_df['time_cum'] = np.cumsum(times)
route_df['velocity'] = velocities

# 速度をグラフに出力
plt.figure(figsize=(12,4))
plt.plot(route_df['time_cum'], route_df['velocity'])
plt.savefig('../results/velocity.png')

# 移動平均を算出
route_df['velocity_movingave_5'] = route_df['velocity'].rolling(5).mean()
route_df['velocity_movingave_10'] = route_df['velocity'].rolling(10).mean()

plt.plot(route_df['time_cum'], route_df['velocity_movingave_10'])

# 曲情報 (別ファイルに書き出したい)
# BPM等の情報は https://docs.google.com/spreadsheets/d/10bVvNTOX1RnFZ45Ghb5-GR2SoXExMB0fj6GNZMvJoE4/edit#gid=0
running_musics = []

song_names = ['ACROSS', 'ファンタズム', 'Poison Lily', 'アンティフォーナ', '恋想花火', 'ブランブル']
song_lengths = [3*60+54, 3*60+38, 3*60+42, 3*60+33, 5*60+6, 3*60+46]
song_bpms = [165, 156, 188, 140, 127, 144]
song_endtimes = np.cumsum(song_lengths)
song_starttimes = [0]
song_starttimes.extend(song_endtimes[:-1])

# for name, length, bpm in zip(song_names, song_lengths, song_bpms):
#     running_musics.append(Song(name, length, bpm))

# 曲情報を入れて移動平均グラフ描画
fig, ax = plt.subplots(figsize=(12,4))
ymin = 5
ymax = 18

ax.plot(route_df['time_cum'], route_df['velocity_movingave_10'])

# 曲の境界線
for name, starttime, endtime, bpm in zip(song_names, song_starttimes, song_endtimes, song_bpms):
    ax.plot([endtime, endtime], [ymin, ymax], linewidth=0.5, linestyle='dashed', color='gray')

    velocity_ave = route_df[(route_df['time_cum']>starttime) & (route_df['time_cum']<endtime)]['velocity'].mean()
    ax.text(starttime+5, ymin+1, "{}\nBPM: {}\nave: {:.2f}km/h".format(name, bpm, velocity_ave))

ax.set_xlabel('second')
ax.set_ylabel('km/h')
ax.set_ylim(ymin, ymax)

output_filename = '../results/velocity_withsong.png'
plt.savefig(output_filename, bbox_inches='tight', pad_inches=0.05)