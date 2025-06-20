"""
This is a boilerplate pipeline 'trajectory'
generated using Kedro 0.18.1
"""
from __future__ import annotations
import sys
import os
import pandas as pd
from typing import Callable
from ..load_cmap_dataset.data_manipulation.game_session import GameSession
import math
import numpy as np



def calculateDistance(x1 : float, y1: float, x2 : float, y2: float):
    p1 = [x1*0.25684, y1*0.16902]
    p2 = [x2*0.25684, y2*0.16902]
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    return(distance)

def calculateDistanceTotale(array):
    dist = 0
    i=0
    x_user = np.zeros(len(array))
    y_user = np.zeros(len(array))
    
    for i in range(0,len(array)) :
        x_user[i] = array[i][0]
        y_user[i] = array[i][1]
    for i in range(0,len(x_user)-1):
        dist += calculateDistance(x_user[i], y_user[i], x_user[i+1], y_user[i+1])
    return(dist)

def reduction_trajectoires(array):
    k=0
    length = len(array)
    xs = [0 for i in range(length)]
    ys = [0 for i in range(length)]
    for i in range(length):
        xs[i] = array[i][0]
        ys[i] = array[i][1]
    del xs[1:length:2]
    del ys[1:length:2]

    array2 = [[0,0,0] for i in range(len(xs))]
    for i in range(len(xs)):
        array2[i] = [xs[i],ys[i], array[0][2]]
    length = len(array2)
    for i in range(0,len(array2)-11, 10):
        for n in range(5):
            if(calculateDistanceTotale(array2[i:i+n]) < 0.004):
                array2[i:i+n] = reduction_trajectoires(array2[i:i+n])
    return (array2)

def trajectory_segmentation(validated_json_dataset: dict[str, Callable]) -> dict[str,Callable]:
    print('trajectory_segmentation')
    n = len(validated_json_dataset.items())
    trajectoires = {}
    #for key, data_loading_func in validated_dataset.items():
        #game_session = GameSession.from_dict(data_loading_func())
    path = "c:\\Users\\lenovo\\Documents\\GitHub\\kedro\\o-kidia"
    session=[0 for i in range(n)]
    for i in range(0, n):
        session[i] = GameSession.from_json(os.path.join(path ,"data", "02_intermediate","logs", "%s.json"%(i+1)))

    for challenge in range(len(session[1].sorted_activities[0].challenges)):
        tra_list = [0 for i in range(n)]
        tra_list2 = [0 for i in range(n)]
        for i in range(0, n):
            curve_user = pd.DataFrame.from_records([{"x": point[0], "y": point[1], "challenge": challenge} for point in session[i].sorted_activities[0].challenges[challenge].digit_curve()])
            tra_list[i] = curve_user.to_numpy()
            
        for i in range(len(tra_list)):
            tra_list2[i] = reduction_trajectoires(tra_list[i])
        key = str(challenge)+".pkl"
        trajectoires[key] = tra_list2
    return trajectoires

def calc_dis_Hausdorff(reduced_points):
    print('calc_dis_Hausdorff')
    matrix_haus = "[matrix]"
    return matrix_haus

def apply_DBSCAN(matrix_haus):
    print('apply_DBSCAN')
    ep = '3'
    num_clusters = '4'
    return [ep, num_clusters]

def clustering_analysis(ep, num_clusters):
    print('clustering_analysis')
    return num_clusters