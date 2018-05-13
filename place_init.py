import re

class User:
    def __init__(self, id, age, sex, occupation, zip):
        self.id = int(id)
        self.age = int(age)
        self.sex = sex
        self.occupation = occupation
        self.zip = zip
        self.avg_r = 0.0

class Item:
    def __init__(self, id, p_name,
    beaches, lakes, hill_stations, mountain, waterfalls):
        self.id = int(id)
        self.p_name = p_name
        self.beaches = int(beaches)
        self.lakes = int(lakes)
        self.hill_stations = int(hill_stations)
        self.mountain = int(mountain)
        self.waterfalls = int(waterfalls)


class Rating:
    def __init__(self, user_id, item_id, rating):
        self.user_id = int(user_id)
        self.item_id = int(item_id)
        self.rating = int(rating)


class Dataset:
    def load_users(self, file, u):
        f = open(file, "r")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('|', 5)
            if len(e) == 5:
                u.append(User(e[0], e[1], e[2], e[3], e[4]))
        f.close()

    def load_items(self, file, i):
        f = open(file, "r")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('|', 10)
            if len(e) == 10:
                i.append(Item(e[0], e[1], e[5], e[6], e[7], e[8], e[9]))
        f.close()

    def load_ratings(self, file, r):
        f = open(file, "r")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('\t', 3)
            if len(e) == 3:
                r.append(Rating(e[0], e[1], e[2]))
        f.close()
