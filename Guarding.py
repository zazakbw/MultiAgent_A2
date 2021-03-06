from ReadJson import FetchData
from plots import  plot_map
from plots import plot_cover_range
import matplotlib.pylab as plt
import numpy as np
from shapely.geometry import Point,LineString
from scipy.spatial.distance import euclidean
import itertools


def positioning_Guards(data,N,triesForSingleStation):
    stations = []
    items = data.items
    sensor_range = data.sensor_range
    totalCovered = 0
    for i in range(N):
        tries = triesForSingleStation
        maxCovered = 0
        maxStation =[0,0]
        while True:
            if not tries:
                break
            x = np.random.uniform(low=data.approximatedBoundary[0], high=data.approximatedBoundary[2])
            y = np.random.uniform(low=data.approximatedBoundary[1], high=data.approximatedBoundary[3])

            # #do not get too close to the boundary, a bit arbitrary now
            # x = np.random.uniform(low=data.approximatedBoundary[0]+sensor_range/2., high=data.approximatedBoundary[2]-sensor_range/2.)
            # y = np.random.uniform(low=data.approximatedBoundary[1]+sensor_range/2., high=data.approximatedBoundary[3]-sensor_range/2.)

            pos = Point(x, y)
            isFreeState = True
            # check if it is in the boundary
            if not data.boundary_polygon_polygon.contains(pos):
                isFreeState = False
            # check if it is out of the obstacles
            if isFreeState:
                for poly in data.obstacles_polygon:
                    if poly.contains(pos):
                        isFreeState = False

            # # do not get to too close to existing stations
            # if stations and isFreeState:
            #     for station in stations:
            #         #a bit arbitrary about how close is too close now
            #         if euclidean(station,[x,y])<sensor_range:
            #             isFreeState=False

            if isFreeState:
                tries -=1
                #count how many items can this new station cover
                cover_count = 0
                for item in items:
                    # if euclidean(item,[x,y])<= sensor_range:
                    if isInSight(data,[x,y],item):
                        cover_count +=1
                        # items.remove(item)
                if cover_count>maxCovered:
                    maxCovered = cover_count
                    maxStation = [x,y]
        stations.append(maxStation)
        for item in items:
            if euclidean(item, maxStation) <= sensor_range:
                items.remove(item)
        totalCovered += maxCovered
    return stations,totalCovered

def isInSight(map,station,item):
    polygons = map.obstacles_polygon
    # print(station,item)
    sensor_range = map.sensor_range
    line = LineString([station,item])
    if euclidean(station,item)>sensor_range:
        return False
    for polygon in polygons:
        if line.crosses(polygon):
            return False
    return True



if __name__ == "__main__":
    data = FetchData("Problems/problem_A12.json")
    plot_map(data)
    stations,totalCovered = positioning_Guards(data,4,200)
    print(totalCovered)#83 for 3,100; 252 for 10,100; 258 for 10,1000;452 for 25,100; for 4,1000
    sensor_range = data.sensor_range
    # plot_map(data)
    plot_cover_range(stations,sensor_range)
    plt.show()



