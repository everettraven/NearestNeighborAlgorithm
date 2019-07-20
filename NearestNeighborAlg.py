import requests
from collections import deque
from itertools import permutations
import random

#Bryce Palmer
#--------------------------------------------------------------------------------------
#This is an implementation of the Nearest Neighbor Algorithm to find the optimal travel
#route to complete errands in the most time efficient possible.
#Currently Implemented:
# 1. Nearest Neighbor Algorithm
# 2. Ability to enter places a person is going
#Need to implement:
#1. Google Directions API to get travel times with traffic



def permute(array):
    return deque(permutations(array))

def get_best_route(points):
    start_point = points[0]

    perms = permute(points[1:])

    routes = {}

    for i in perms:
        for j in range(len(i)):
            random_value = random.randint(1,10)
            if j == 0:
                dict_key = start_point + "2" + i[j]
                reversed_key = i[j] + "2" + start_point
                dict_key2 = i[j] + "2" + i[j+1]
                reversed_key2 = i[j+1] + "2" + i[j]

                if dict_key not in routes and reversed_key not in routes:
                    routes[dict_key] = random_value
                
                if dict_key2 not in routes and reversed_key2 not in routes:
                    routes[dict_key2] = random_value

            elif j == len(i) - 1:
                dict_key = i[j] + "2" + start_point
                reversed_key = start_point + "2" + i[j]

                if dict_key not in routes and reversed_key not in routes:
                    routes[dict_key] = random_value
            
            else:
                dict_key = i[j] + "2" + i[j+1]
                reversed_key = i[j+1] + "2" + i[j]

                if dict_key not in routes and reversed_key not in routes:
                    routes[dict_key] = random_value

    print(len(routes))
    print(routes)


    optimal_path = []
    path_builder = []
    optimal_weight = {}
    path_weight = 0


    for i in perms:
        for j in range(len(i)):
            if j == 0:
                dict_key = start_point + "2" + i[j]
                reversed_key = i[j] + "2" + start_point
                dict_key2 = i[j] + "2" + i[j+1]
                reversed_key2 = i[j+1] + "2" + i[j]

                if dict_key not in routes and reversed_key in routes:
                    path_weight += routes[reversed_key]
                else:
                    path_weight += routes[dict_key]
                
                if dict_key2 not in routes and reversed_key2 in routes:
                    path_weight += routes[reversed_key2]
                else:
                    path_weight += routes[dict_key2]

            elif j == len(i) - 1:
                dict_key = i[j] + "2" + start_point
                reversed_key = start_point + "2" + i[j]

                if dict_key not in routes and reversed_key in routes:
                    path_weight += routes[reversed_key]
                else:
                    path_weight += routes[dict_key]
            
            else:
                dict_key = i[j] + "2" + i[j+1]
                reversed_key = i[j+1] + "2" + i[j]

                if dict_key not in routes and reversed_key in routes:
                    path_weight += routes[reversed_key]
                else:
                    path_weight += routes[dict_key]

            path_builder.append(i[j])

        if "lowest" in optimal_weight:
            if path_weight < optimal_weight["lowest"]:
                optimal_weight["lowest"] = path_weight
                optimal_path = path_builder
        else:
            optimal_weight["lowest"] = path_weight
            optimal_path = path_builder
        
        path_builder = []
        path_weight = 0

    optimal_path.insert(0, start_point)
    print(optimal_weight["lowest"])
    print(optimal_path)

    return optimal_path


#This is the test portion to make sure the main algorithm is working.
#Glad to say that it works!

location_count = int(input("How many locations do you plan to visit? (including your current location) "))

points = []
for i in range(location_count):
    if i == 0:
        location = input("What is your starting location? ")
    else:
        location = input("What is location {}? ".format(i))
    points.append(location)

print(points)

print(get_best_route(points))

