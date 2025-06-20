"""
This is a boilerplate pipeline 'DTW'
generated using Kedro 0.18.1
"""

from __future__ import annotations

from typing import Callable
import numpy as np
from ..load_cmap_dataset.data_manipulation.game_session import GameSession
#implementing dtw score between two participants 
from tslearn.metrics import dtw

def dtw_score_challenge(game_session1:GameSession , game_session2: GameSession):
    return [1/(1 + dtw(
        np.asarray([ (point[0], point[1]) for point in challenge1.digit_curve()]),
        np.asarray([ (point[0], point[1]) for point in challenge2.digit_curve()])
        )) for challenge1, challenge2 in zip(game_session1.sorted_activities[0].challenges, game_session2.sorted_activities[0].challenges)]  


def dtw_score_similarity_matrix(validated_dataset: dict[str,Callable])-> dict[str,Callable] :
    similarity_matrix={}
    n=len(validated_dataset.items())
    L=[np.zeros((n,n)) for num_challenge in range(14)]
    for i, (key1, data_loading_func1) in enumerate(validated_dataset.items()):
        for j, (key2, data_loading_func2) in enumerate(validated_dataset.items()):
            game_session1 = GameSession.from_dict(data_loading_func1())
            game_session2 = GameSession.from_dict(data_loading_func2())
            A=dtw_score_challenge(game_session1,game_session2)
            for num_challenge in range(14):
                L[num_challenge][i,j]=A[num_challenge]
                if (i!=j):
                    L[num_challenge][j,i]=A[num_challenge]
    for num_challenge in range(14):
        similarity_matrix["DTW_Similarity_Challenge"+str(num_challenge+1)+".pkl"]=L[num_challenge]
    return similarity_matrix
    
def clustering_dtw(DTW_Similarity_dataset):
    return DTW_Similarity_dataset