import requests
from collections import deque
from itertools import permutations
import random
import os
import json

#Bryce Palmer
#--------------------------------------------------------------------------------------
#This is an implementation of the Nearest Neighbor Algorithm to find the optimal travel
#route to complete errands in the most time efficient possible.
#Currently Implemented:
# 1. Nearest Neighbor Algorithm
# 2. Ability to enter places a person is going
#Need to implement:
#1. Google Directions API to get travel times with traffic

#This little snippet reads the google directions API from a .txt file so i dont have to place it here in the code
file = open("./GoogleDirectionsAPIToken.txt", "r")
api_key = file.read()

def permute(array):
    return deque(permutations(array))

def get_best_route(points):
    
    start_point = points[0]

    perms = permute(points[1:])

    print(len(perms))

    routes = {}

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

                if dict_key not in routes and reversed_key not in routes:
                    routes[dict_key] = get_duration(start_point, i[j])
                
                if dict_key2 not in routes and reversed_key2 not in routes:
                   routes[dict_key2] = get_duration(i[j], i[j+1])

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

                if dict_key not in routes and reversed_key not in routes:
                    routes[dict_key] = get_duration(i[j], start_point)
                
                if dict_key not in routes and reversed_key in routes:
                    path_weight += routes[reversed_key]
                else:
                    path_weight += routes[dict_key]

            
            else:
                dict_key = i[j] + "2" + i[j+1]
                reversed_key = i[j+1] + "2" + i[j]

                if dict_key not in routes and reversed_key not in routes:
                    routes[dict_key] = get_duration(i[j], i[j+1])

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

    print(len(routes))
    print(routes)
    optimal_path.insert(0, start_point)
    print(optimal_weight["lowest"])
    print(optimal_path)

    return optimal_path

#this function is a function that will be used to get the duration in traffic value from location1 to 
#location2 from the Google Directions API
def get_duration(loc1, loc2):
    origin = loc1.replace(" ", "+")
    destination = loc2.replace(" ", "+")

    url = "https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&departure_time=now&key={2}".format(origin, destination, api_key)

    resp = requests.post(url)
    data = resp.json()

    traffic_duration = data['routes'][0]['legs'][0]['duration_in_traffic']['value']
    return(traffic_duration)

    
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


