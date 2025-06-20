"""
This is a boilerplate pipeline 'heatmaps'
generated using Kedro 0.18.0
"""
from array import array
from copy import deepcopy
#from curses import keyname
import string
import sys
sys.path.insert(0,"c:\\Users\\lenovo\\Documents\\GitHub\\kedro\\o-kidia")
from src.okidia.pipelines.load_cmap_dataset.data_manipulation.game_session import GameSession
from typing import Callable, Dict
import pandas as pd 
import numpy as np
import os
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
import cv2
import pickle

from keras.applications.vgg19 import VGG19
from keras.preprocessing.image import img_to_array
from keras.applications.vgg19 import preprocess_input
from keras.preprocessing.image import load_img

from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans, SpectralClustering
kmeans_kwargs = {"init": "k-means++","n_init": 10,"max_iter": 300,"random_state": 42,}
import tensorflow as tf

def create_heatmap(validated_json_dataset: Dict[str, Callable]) -> Dict[str,Callable]:
    images={}
    for key , data_loading_funct in validated_json_dataset.items():
        game_session = GameSession.from_dict(data_loading_funct())
        for challenge in range(0,14):
            #curve = pd.DataFrame.from_records([{"x_model": point[0], "y_model": point[1]} for point in game_session.sorted_activities[0].challenges[challenge].curve_points()])
            key_ch=key[:-5]+"_"+str(challenge)+'.png'
            curve_user = pd.DataFrame.from_records([{"x_user": point[0], "y_user": point[1]} for point in game_session.sorted_activities[0].challenges[challenge].digit_curve()])
            data_user = curve_user.to_numpy();
            x_user = np.zeros(len(data_user))
            y_user = np.zeros(len(data_user))
            
            for i in range(0,len(data_user)) :
                x_user[i] = data_user[i][0]
                y_user[i] = data_user[i][1]
            heatmap,xedges,yedges = np.histogram2d(x_user,y_user,bins=(200,200))
            heatmap = gaussian_filter(heatmap, sigma=8)
            extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

            plt.clf()
            plt.imshow(heatmap.T, extent=extent, origin='lower',cmap=cm.jet)
            plt.title("Model")
            images[key_ch] = plt.figure()
            #import pdb
            #pdb.set_trace()

    #plt.savefig(os.path.join('\\data\\test.png')) 
    return images

def vgg19(heatmap_dataset: Dict[str, Callable]) -> Dict[str,Callable]:
    features={}
    Matrice=np.zeros((60,1000))
    model = VGG19()
    Dictionary={'Mat_1.pickle','Mat_2.pickle','Mat_3.pickle','Mat_4.pickle','Mat_5.pickle','Mat_6.pickle','Mat_7.pickle','Mat_8.pickle','Mat_9.pickle','Mat_10.pickle','Mat_11.pickle','Mat_12.pickle','Mat_13.pickle','Mat_14.pickle'}
    for key in Dictionary:     
        challenge = 0
        for passation in range(1,61):
            image = load_img('data/03_primary/logs/'+str(passation)+'_'+str(challenge)+'.png',target_size=(224, 224))
            # convert the image pixels to a numpy array
            image = img_to_array(image)
            # reshape data for the model
            image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
            # prepare the image for the VGG model
            image = preprocess_input(image)
            # predict the probability across all output classes
            Matrice[passation-1]=model.predict(image)
        challenge = challenge +1
        print(len(Matrice[10]))
        print(len(Matrice))
        features[key] = Matrice
    return features

def dataFrame_Similarity_perChallenge(num_challenge: int, M):   
    id_participant=[GameSession.from_json(os.path.join("data","02_intermediate", "logs", str(i+1)+".json")).student_id for i in range(60)]
    best_score=0
    nbr_clusters=0
    silhouette_coefficients=[]
    # searching the k that has the best silhouette score: in our example k = 2 or 3 
    for k in range(2, 11):
        #sc= SpectralClustering(n_clusters=k,affinity="precomputed")
        #sc.fit(M)
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(M)
        #score = silhouette_score(M, sc.labels_)
        score = silhouette_score(M,kmeans.labels_)
        silhouette_coefficients.append(score)
        if score>best_score: 
            best_score=score
            nbr_clusters=k
    #clustering the datasetactiva
    #sc = SpectralClustering(n_clusters=nbr_clusters,affinity="precomputed")
    kmeans = KMeans(n_clusters=nbr_clusters, **kmeans_kwargs)
    #y=sc.fit_predict(M)
    kmeans.fit(M)
    y=kmeans.predict(M)
    data={'num_challenge':num_challenge,'participant_id':id_participant,'cluster_id':y}
    return pd.DataFrame(data)


def clustering(features_dataset: Dict[str, Callable]):
    Matrice=np.zeros((14,60,1000))
    for i in range(1,15):
        with open(os.path.join("c:/Users/lenovo/Documents/GitHub/kedro/o-kidia/data/04_feature/logs/Mat_"+str(i)+".pickle"),"rb") as f:
            Matrice[i-1] = pickle.load(f)
            print(Matrice[i-1])
            print(Matrice.shape)

    data=pd.concat([dataFrame_Similarity_perChallenge(i,Matrice[i]) for i in range(14)], ignore_index=True)
    data.to_csv("c:/Users/lenovo/Documents/GitHub/kedro/o-kidia/data/07_model_output/logs/vgg_clustering.csv",index=False)
    return data