# -*- coding: utf-8 -*-
from math import sqrt
import collections


class Recommender:

    def __init__(self, Rmin, Rmax, user_dataset, item_dataset):
        self.Rmin = Rmin
        self.Rmax = Rmax
        self.Rmid = (self.Rmin + self.Rmax) / 2.0

        self.place = {}
        for line in open(item_dataset):
            (id, title) = line.split('|')[0:2]
            self.place[id] = title

        self.userData = {}
        for line in open(user_dataset):
            (user, placeid, rating) = line.split('\t')
            self.userData.setdefault(user, {})
            self.userData[user][self.place[placeid]] = float(rating)

        self.UsersList = [i for i in self.userData]

    def Agreement(self, r1, r2):
        self.r1 = r1
        self.r2 = r2
        if (self.r1 > self.Rmid and self.r2 < self.Rmid) or (self.r1 < self.Rmid and self.r2 > self.Rmid):
            return False
        return True

    def Proximity(self, r1, r2):
        if self.Agreement(r1, r2):
            self.absDist = abs(r1 - r2)
        self.absDist = 2 * abs(r1 - r2)
        return ((2 * (self.Rmax - self.Rmin) + 1) - self.absDist) ** 2

    def Impact(self, r1, r2):
        return (((abs(r1 - self.Rmid) + 1) * (abs(r2 - self.Rmid) + 1)) if self.Agreement(r1, r2) else (
        1.0 / ((abs(r1 - self.Rmid) + 1) * (abs(r2 - self.Rmid) + 1))))

    def Popularity(self, r1, r2, item):
        itemRating = []
        for itm in self.itemData[item]:
            itemRating.append(self.itemData[item][itm])

        self.avg = self.mean(itemRating)
        return ((1 + (((r1 + r2) / 2.0 - self.avg) ** 2)) if (r1 > self.avg and r2 > self.avg) or (
        r1 < self.avg and r2 < self.avg) else 1)

    def distance(self, user1, user2, choice):
        if choice:
            data = self.userData
        else:
            data = self.itemData
        commonItem = {}
        for item in data[user1]:
            if item in data[user2]:
                commonItem[item] = 1

        if len(commonItem) == 0: return 0

        sum_of_squares = sum(
            [pow(data[user1][item] - data[user2][item], 2) for item in data[user1] if item in data[user2]])

        return 1 / (1 + sum_of_squares)

    def cosin(self, user1, user2, choice):
        if choice:
            data = self.userData
        else:
            data = self.itemData

        commonItem = {}
        for item in self.userData[user1]:
            if item in self.userData[user2]: commonItem[item] = 1

        n = len(commonItem)

        if n == 0: return 0

        s1Sq = sum([pow(self.userData[user1][it], 2) for it in commonItem])
        s2Sq = sum([pow(self.userData[user2][it], 2) for it in commonItem])

        neu = sum([self.userData[user1][it] * self.userData[user2][it] for it in commonItem])

        deno = sqrt(s1Sq * s2Sq)
        if deno == 0: return 0
        print(neu/deno)
        return neu / deno

    def mean(self, listinput):
        total = 0.0
        for entry in listinput:
            total += entry
        return total / len(listinput)

    def UserRecommendation(self, user, distanceType):
        tot = collections.defaultdict(float)
        sums = collections.defaultdict(float)

        for other in self.userData:

            if other == user: continue
            simi = distanceType(user, other, True)

            if simi <= 0: continue
            for item in self.userData[other]:

                if item not in self.userData[user] or self.userData[user][item] == 0:
                    tot[item] += self.userData[other][item] * simi

                    sums[item] += simi

        rankings = [item for (item, total) in tot.items()]
        rankings.sort()
        rankings.reverse()

        return rankings

    def ItemRecommendation(self, user, distType, n=10):
        item = {}
        userRatings = self.userData[user]
        scrs = {}
        tot = {}

        self.createItemData()
        for itm in self.itemData:
            scores = [(distType(itm, other, False), other) for other in self.itemData if other != itm]
            scores.sort()
            scores.reverse()
            item[itm] = scores[0:n]

        for (itm, rating) in userRatings.items():

            for (similar, itm2) in item[itm]:

                if itm2 in userRatings: continue

                scrs.setdefault(itm2, 0)
                scrs[itm2] += similar * rating

                tot.setdefault(itm2, 0)
                tot[itm2] += similar

        rankings = [(score / tot[itm], itm) for itm, score in scrs.items()]

        rankings.sort(reverse=True)
        return rankings

    def createItemData(self):
        result = collections.defaultdict(dict)
        for person in self.userData:
            for item in self.userData[person]:
                result[item][person] = self.userData[person][item]
        self.itemData = result


obj1 = Recommender(1, 5, "data/u.test", "data/u.item")
u=input("Enter user ID: ")
obj2=obj1.UserRecommendation(u,obj1.cosin)[0:5]
print('UserBased Recommendation: \n\n', '\n'.join(map(str, obj2)),'\n')
