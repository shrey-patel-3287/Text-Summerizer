from audioop import reverse
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

def read_article(file_name):
    with open(file_name) as f:
        a = " ".join(line.strip() for line in f)
    with open(file_name,"r+") as f:
        f.truncate(0)
        f.write(a)
    file = open(file_name,"r")
    filedata = file.readlines()
    #print(filedata)
    article = filedata[0].split(". ")
    sentances=[]
    for sentance in article:
        sentances.append(sentance.replace("[^a-zA-Z]","").split(" "))
    sentances.pop()
    return sentances 

def sentance_similarity(sent1,sent2,stopwords=None):
    if stopwords is None:
        stopwords=[]
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1+sent2))

    vector1= [0] * len(all_words)
    vector2= [0] * len(all_words)
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1-cosine_distance(vector1,vector2)

def gen_sim_matrix(sentances,stop_words):
    similarity_matrix=np.zeros((len(sentances),len(sentances)))
    for idx1 in range(len(sentances)):
        for idx2 in range(len(sentances)):
            if idx1 == idx2:
                continue
            similarity_matrix[idx1][idx2]=sentance_similarity(sentances[idx1],sentances[idx2],stop_words)

    return similarity_matrix

def generate_summary(file_name,top_n=5):
    stop_words=stopwords.words('english')
    summarize_text=[]
    sentances = read_article(file_name)
    matrix=gen_sim_matrix(sentances,stop_words)
    graph=nx.from_numpy_array(matrix)
    scores = nx.pagerank(graph)
    ranked_sentance=sorted(((scores[i],s)for i,s in enumerate(sentances)),reverse=True)
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentance[i][1]))
    text = ". ".join(summarize_text)
    return text


