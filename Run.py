
from place_init import *
from sklearn.cluster import KMeans

import numpy as np
import pickle
import random

user = []
item = []

d = Dataset()
d.load_users("data/u.user", user)
d.load_items("data/u.item", item)

n_users = len(user)
n_items = len(item)

utility_matrix = pickle.load( open("utility_matrix.pkl", "rb") )

for i in range(0, n_users):
    x = utility_matrix[i]
    user[i].avg_r = sum(a for a in x if a > 0) / sum(a > 0 for a in x)

def pcs(x, y, ut):
    num = 0
    den1 = 0
    den2 = 0
    A = ut[x - 1]
    B = ut[y - 1]
    num = sum((a - user[x - 1].avg_r) * (b - user[y - 1].avg_r) for a, b in zip(A, B) if a > 0 and b > 0)
    den1 = sum((a - user[x - 1].avg_r) ** 2 for a in A if a > 0)
    den2 = sum((b - user[y - 1].avg_r) ** 2 for b in B if b > 0)
    den = (den1 ** 0.5) * (den2 ** 0.5)
    if den == 0:
        return 0
    else:
        return num / den

place_genre = []
for place in item:
    place_genre.append([place.beaches, place.lakes, place.hill_stations, place.mountain, place.waterfalls])

place_genre = np.array(place_genre)
cluster = KMeans(n_clusters=5)
cluster.fit_predict(place_genre)

ask = random.sample(item, 5)
new_user = np.zeros(19)

print ("Please rate the following s (1-5):")

for place in ask:
	print (place.p_name + ": ")
	a = int(input())
	if new_user[cluster.labels_[place.id - 1]] != 0:
		new_user[cluster.labels_[place.id - 1]] = (new_user[cluster.labels_[place.id - 1]] + a) / 2
	else:
		new_user[cluster.labels_[place.id - 1]] = a

utility_new = np.vstack((utility_matrix, new_user))

user.append(User(944, 21, 'M', 'student', 110018))
pcs_matrix = np.zeros(n_users)

print ("Finding users which have similar preferences.")
for i in range(0, n_users + 1):
    if i != 943:
        pcs_matrix[i] = pcs(944, i + 1, utility_new)

user_index = []
for i in user:
	user_index.append(i.id - 1)
user_index = user_index[:943]
user_index = np.array(user_index)

top_5 = [x for (y,x) in sorted(zip(pcs_matrix, user_index), key=lambda pair: pair[0], reverse=True)]
top_5 = top_5[:5]

top_5_genre = []

for i in range(0, 5):
	maxi = 0
	maxe = 0
	for j in range(0, 5):
		if maxe < utility_matrix[top_5[i]][j]:
			maxe = utility_matrix[top_5[i]][j]
			maxi = j
	top_5_genre.append(maxi)
print ("Places you'd like:")
new_arr = []

for i in top_5_genre:
    if i == 0:
        new_arr.append("Beaches")

    elif i == 1:
        new_arr.append("Lakes")

    elif i == 2:
        new_arr.append("Hill Stations")

    elif i == 3:
        new_arr.append("Mountains")

    else:
        new_arr.append("Waterfall")


final_list = []
for num in new_arr:
    if num not in final_list:
        final_list.append(num)

for i in final_list:
    print(i)

beach_list = []
lakes_list = []
hill_stations = []
mountains = []
waterfalls = []

f = []

for i in range(0, len(final_list)):
    if final_list[i] == "Beaches":
        fileHandle = open("data/beach.txt", "r")  # open file name
        # get lines from file
        for line in fileHandle:
            line = line.rstrip()
            textList = line.split("|")  # split the line into a list
            beach_list.append(textList[1])
        print("~~~~~~~~Beaches you would like to visit~~~~~~~~~~~~~~")
        f = (random.sample(beach_list, 5))
        for m in f:
            print(m)
    if final_list[i] == "Lakes":
        fileHandle = open("data/lakes.txt", "r")  # open file name
        # get lines from file
        for line in fileHandle:
            line = line.rstrip()
            textList = line.split("|")  # split the line into a list
            lakes_list.append(textList[1])
        print("~~~~~~~~~~~Lakes you would like to visit~~~~~~~~~")
        f = (random.sample(lakes_list, 5))
        for m in f:
            print(m)
    if final_list[i] == "Hill Stations":
        fileHandle = open("data/hill_station.txt", "r")  # open file name
        # get lines from file
        for line in fileHandle:
            line = line.rstrip()
            textList = line.split("|")  # split the line into a list
            hill_stations.append(textList[1])
        print("~~~~~~~~~~~Hill Stations you would like to visit~~~~~~~~~~~")
        f = (random.sample(hill_stations, 5))
        for m in f:
            print(m)
    if final_list[i] == "Mountains":
        fileHandle = open("data/mountains.txt", "r")  # open file name
        # get lines from file
        for line in fileHandle:
            line = line.rstrip()
            textList = line.split("|")  # split the line into a list
            mountains.append(textList[1])
        print("~~~~~~~~~~~~~~Mountains you would like to visit~~~~~~~~~~~")
        f = (random.sample(mountains, 5))
        for m in f:
            print(m)
    if final_list[i] == "Waterfall":
        fileHandle = open("data/waterfalls.txt", "r")  # open file name
        # get lines from file
        for line in fileHandle:
            line = line.rstrip()
            textList = line.split("|")  # split the line into a list
            waterfalls.append(textList[1])
        print("~~~~~~~~~~~Waterfalls you would like to visit~~~~~~~~~~~~~~")
        f = (random.sample(waterfalls, 5))
        for m in f:
            print(m)