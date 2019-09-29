import math

import numpy as np
import copy
from datetime import datetime
# one unit is one min
# arrival_time needs to be datetime format
from app.utils import get_route


class SiteClass:
    def __init__(self, rating, recommend_time = None, open_time=datetime(year=2019, month=9, day=29, hour=1,minute=0, second=0),
                 close_time=datetime(year=2019, month=9, day=30, hour=1,minute=0, second=0)):
        self.open_time = open_time              # needed, datetime formate
        self.close_time = close_time            # needed, datetime formate
        self.rate = rating*10000000000000000000/hash(rating) % 90 + 30       # needed
        self.recommend_time = hash(rating) % 90 + 30   # needed, integer, unit is min
        # if(self.recommend_time % 10 != 0):
        #     self.recommend_time=self.recommend_time-self.recommend_time%10
        if(self.recommend_time % 10 == 0):
            self.recommend_time=self.recommend_time+2

    def max_stay_time(self, arrive_time, ags):
        if arrive_time >= self.close_time:
            print("Time compare:  ",arrive_time,"  ",self.close_time)
            return 0
        else:
            # return min(  (datetime.timestamp(self.close_time) - datetime.timestamp(arrive_time)) /60 // ags.STAY_SLOT, self.recommend_time // ags.STAY_SLOT )
            return int((datetime.timestamp(self.close_time) - datetime.timestamp(arrive_time)) / 60 // ags.STAY_SLOT)

    def get_happiness(self, arrive_time, stay_time, ags):
        if arrive_time < self.open_time:
            stay_time -= self.open_time - arrive_time

        if arrive_time >= self.close_time:
            return 0

        if stay_time <= 0:
            return 0
        else:
            if stay_time > (self.recommend_time//ags.STAY_SLOT):
                stay_time = self.recommend_time
            return self.rate * stay_time


class Arguments:
    def __init__(self, DESTINATION_AMOUNT, TIME_LIMITATION, cost_map, sties, STAY_SLOT = 10, DESTINATION_INDEX=0):
        self.DESTINATION_AMOUNT = DESTINATION_AMOUNT     # needed number of destinations, not including starting point and end point
        self.TIME_LIMITATION = TIME_LIMITATION      # needed, datetime formate, end time
        self.STAY_SLOT = STAY_SLOT             # needed length of time unit
        self.cost_map = cost_map
        # self.cost_map = np.array([      # needed distance matrix
        #     [0, 40, 60, 30],
        #     [40, 0, 30, 50],
        #     [60, 30, 0, 25],
        #     [30, 50, 25, 0]])
        # self.site_name = ['E', 'A', 'B', 'C']   # needed name of sites
        self.site_name = list(range(DESTINATION_AMOUNT+1))
        self.site = sties   # needed  siteClass for each site
        self.DESTINATION_INDEX = DESTINATION_INDEX
        self.START_INDEX = 0
        self.max_happiness = 0
        self.remain = DESTINATION_AMOUNT
        self.visited = [0] * (DESTINATION_AMOUNT + 1)
        self.current_path = []
        self.best_path = []



#
# def get_happiness(current_time, current_location, time_length, arguments):
#     ret = time_length / arguments.max_stay[current_location]
#     ret *= arguments.HAPPINESS_THRESHOLD
#     return ret

def datetime_add(date_tmp, add_min):
    return datetime.fromtimestamp(int(date_tmp.timestamp()+add_min*60))



def get_cost(current_time, start, destination, ags):
    destination = int(destination)
    return ags.cost_map[start][destination] #min


def dfs(current_location, current_time, current_happiness, ags):
    print("Enter dfs  ",current_location,"Destination amount  ",ags.DESTINATION_AMOUNT)
    if datetime_add(current_time, get_cost(current_time, current_location, ags.DESTINATION_INDEX, ags) + 20)> ags.TIME_LIMITATION:
        print("OutOfTimeLimitation:\t", current_location)
        print("\ttime information: ",current_time,'  ',get_cost(current_time, current_location, ags.DESTINATION_INDEX, ags),'  ',ags.TIME_LIMITATION)
        return
    if ags.remain == 0:
        if current_happiness > ags.max_happiness:
            ags.max_happiness = current_happiness
            ags.best_path = copy.deepcopy(ags.current_path)
        return

    # index 0 means starting point
    for nxt in range(1, ags.DESTINATION_AMOUNT + 1):
        print("visited ",nxt,":  ",ags.visited[nxt])
        if ags.visited[nxt] == 0:
            journey_cost = get_cost(current_time, current_location, nxt, ags)
            # here one step means 10 mins
            # print(nxt , "   " , len(ags.site))
            print("stay time range\t",ags.site[nxt].max_stay_time(datetime_add(current_time, journey_cost), ags))
            for stay_time in range(1, ags.site[nxt].max_stay_time(datetime_add(current_time, journey_cost), ags) + 1):
                print("try stay time  ", stay_time)
                ags.visited[nxt] = 1
                ags.remain -= 1

                ags.current_path.append([ags.site_name[nxt], stay_time*10])  # sitename, stay_time
                dfs(nxt,
                    datetime_add(current_time, (journey_cost + stay_time * ags.STAY_SLOT)),
                    current_happiness + ags.site[nxt].get_happiness(datetime_add(current_time, journey_cost), stay_time, ags),
                    ags)
                ags.visited[nxt] = 0
                ags.remain += 1
                ags.current_path.pop()

#departure_time is datetime format. departure and Destination is the name of the places
def get_cost_latest(departure_time, departure, destination):
    sec = get_route(departure, destination, departure_time)[0]['legs'][0]['duration']['value']
    return math.ceil(sec/60)


def update_plan(startime, schedule, end_point, ags):
    time_sum = 0
    result_dict = {}
    # cost_for_comming, arrvival_time, time_to_spend, leave_time
    result_dict[ags.site_name[0]] = (0, 0, 0, startime)
    startime_tmp = startime
    for i in range(1, len(schedule)):
        cost = get_cost_latest(startime_tmp,ags.site_name[i-1], ags.site_name[i])
        result_dict[ags.site_name[i]] = (cost, datetime_add(startime_tmp,cost), schedule[i], datetime_add(startime_tmp, cost+schedule[i]))
        startime_tmp = datetime_add(startime_tmp, (cost+schedule[i]))
    cost = get_cost_latest(startime_tmp,ags.site_name[-1], end_point)
    result_dict[end_point] = [cost,datetime_add(startime_tmp, cost), 0, 0 ]
    print("cost_for_comming, arrvival_time, time_to_spend, leave_time")
    for i in result_dict.keys():
        print(result_dict[i])
    return result_dict