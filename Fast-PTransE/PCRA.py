import os,sys
import math
import random
import time
from tqdm import tqdm
def map_add(mp, key1,key2, value):
    if (key1 not in mp):
        mp[key1] = {}
    if (key2 not in mp[key1]):
        mp[key1][key2] = 0.0
    mp[key1][key2] += value


def map_add1(mp,key):
    if (key not in mp):
        mp[key] = 0
    mp[key]+=1

f = open("data/FB15K/relation2id.txt","r")
relation2id = {}
id2relation = {}
relation_num = 0
for line in f:
    seg = line.strip().split()
    if len(seg)  == 1: continue
    relation2id[seg[0]] = int(seg[1])
    id2relation[int(seg[1])]=seg[0]
    id2relation[int(seg[1])+1345]="~"+seg[0]
    relation_num+=1
f.close()

ent2id, id2ent = dict(), dict()
for line in open('data/FB15K/entity2id.txt', 'r'):
    if len(line.split()) == 1: continue
    [ent, id] = line.split()
    ent2id[ent] = int(id)
    id2ent[int(id)]  = ent

# print(ent2id['/m/06cx9'])

f = open("data/FB15K/train.txt","r")
entityPairHasRelation = {}
entityEdge ={}

num=0
step=0


for line in f:
    seg = line.strip().split()
    e1 = seg[0]
    e2 = seg[2]
    rel = seg[1]
    # print(e1,e2,rel)
    if (e1+" "+e2 not in entityPairHasRelation):
        entityPairHasRelation[e1 + " " + e2]={}
    entityPairHasRelation[e1 + " " + e2][relation2id[rel]]=1
    if (e2+" "+e1 not in entityPairHasRelation):
        entityPairHasRelation[e2 + " " + e1]={}
    entityPairHasRelation[e2 + " " + e1][relation2id[rel] + relation_num]=1
    if (e1 not in entityEdge):
        entityEdge[e1]={}
    if (relation2id[rel] not in entityEdge[e1]):
        entityEdge[e1][relation2id[rel]]={}
    entityEdge[e1][relation2id[rel]][e2]=1
    if (e2 not in entityEdge):
        entityEdge[e2]={}
    if ((relation2id[rel]+relation_num) not in entityEdge[e2]):
        entityEdge[e2][relation2id[rel] + relation_num]={}
    entityEdge[e2][relation2id[rel] + relation_num][e1]=1
f.close()


f = open("data/FB15K/test.txt","r")
for line in f:
    seg = line.strip().split()
    if (seg[0]+" "+seg[1] not in entityPairHasRelation):
        entityPairHasRelation[seg[0] + ' ' + seg[1]]={}
    if (seg[1]+" "+seg[0] not in entityPairHasRelation):
        entityPairHasRelation[seg[1] + ' ' + seg[0]]={}
f.close()

h_e_p = {}

# f = open("data/FB15K/e1_e2.txt","r")
# for line in f:
#     seg = line.strip().split()
#     ok[seg[0]+" "+seg[1]] = {}
#     ok[seg[1]+" "+seg[0]] = {}
# f.close()


g = open("data/FB15K/path2.txt","w")


path_dict = {}
path_r_dict = {}
train_path = {}


step = 0
time1= time.time()
path_num = 0

h_e_p={}
for e1 in tqdm(entityEdge):
    step+=1
    # print(step, end=' ')
    for rel1 in entityEdge[e1]:
        e2_set = entityEdge[e1][rel1]
        for e2 in e2_set:
            map_add1(path_dict,str(rel1))
            for key in entityPairHasRelation[e1 + ' ' + e2]:
                map_add1(path_r_dict,str(rel1)+"->"+str(key))
            map_add(h_e_p,e1+' '+e2,str(rel1),1.0/len(e2_set))
    for rel1 in entityEdge[e1]:
        e2_set = entityEdge[e1][rel1]
        for e2 in e2_set:
            if (e2 in entityEdge):
                for rel2 in entityEdge[e2]:
                    e3_set = entityEdge[e2][rel2]
                    for e3 in e3_set:
                        map_add1(path_dict,str(rel1)+" "+str(rel2))
                        if (e1+" "+e3 in entityPairHasRelation):
                            for key in entityPairHasRelation[e1 + ' ' + e3]:
                                map_add1(path_r_dict,str(rel1)+" "+str(rel2)+"->"+str(key))
                        if (e1+" "+e3 in entityPairHasRelation):# and h_e_p[e1+' '+e2][str(rel1)]*1.0/len(e3_set)>0.01):
                            map_add(h_e_p,e1+' '+e3,str(rel1)+' '+str(rel2),h_e_p[e1+' '+e2][str(rel1)]*1.0/len(e3_set))
    '''
    for rel1 in a[e1]:
        e2_set = a[e1][rel1]
        for e2 in e2_set:
            if (e2 in a):
                for rel2 in a[e2]:
                    e3_set = a[e2][rel2]
                    for e3 in e3_set:
                        if (e1+" "+e3 in h_e_p and str(rel1)+' '+str(rel2) in h_e_p[e1+" "+e3]):
                            for rel3 in a[e3]:
                                e4_set = a[e3][rel3]
                                if (h_e_p[e1+" "+e3][str(rel1)+' '+str(rel2)]/len(e4_set)<0.01):
                                    continue
                                for e4 in e4_set:
                                    if (e1+" "+e4 in ok):
                                        map_add(h_e_p,e1+' '+e4,str(rel1)+' '+str(rel2)+" "+str(rel3),h_e_p[e1+" "+e3][str(rel1)+' '+str(rel2)]*1.0/len(e4_set))
  '''
    for e2 in entityEdge:
        e_1 = e1
        e_2 = e2
        if (e_1+" "+e_2 in h_e_p):
            path_num+=len(h_e_p[e_1+" "+e_2])
            bb = {}
            aa = {}
            g.write(str(e_1)+" "+str(e_2)+"\n")
            sum = 0.0
            for rel_path in h_e_p[e_1+' '+e_2]:
                bb[rel_path] = h_e_p[e_1+' '+e_2][rel_path]
                sum += bb[rel_path]
            for rel_path in bb:
                bb[rel_path]/=sum
                if bb[rel_path]>0.01:
                    aa[rel_path] = bb[rel_path]
            g.write(str(len(aa)))
            for rel_path in aa:
                train_path[rel_path] = 1
                g.write(" "+str(len(rel_path.split()))+" "+rel_path+" "+str(aa[rel_path]))
            g.write("\n")
    # print(path_num, time.time()-time1)
    sys.stdout.flush()
g.close()

g = open("data/FB15K/confidence.txt","w")
for rel_path in train_path:

    out = []
    for i in range(0,relation_num):
        if (rel_path in path_dict and rel_path+"->"+str(i) in path_r_dict):
            out.append(" "+str(i)+" "+str(path_r_dict[rel_path+"->"+str(i)]*1.0/path_dict[rel_path]))
    if (len(out)>0):
        g.write(str(len(rel_path.split()))+" "+rel_path+"\n")
        g.write(str(len(out)))
        for i in range(0,len(out)):
            g.write(out[i])
        g.write("\n")
g.close()
def work(dir):
    f = open("data/FB15K/"+dir+".txt","r")
    g = open("data/FB15K/"+dir+"_pra.txt","w")
    lines = f.readlines()
    g.write(f"{len(lines)}\n")
    for line in lines:
        seg = line.strip().split()
        e1 = seg[0]
        e2 = seg[2]
        rel = relation2id[seg[1]]
        g.write(f"{ent2id[e1]} {ent2id[e2]} {rel}\n")#(str(ent2id[e1])+" "+ent2id[e2]+' '+str(rel)+"\n")
        b = {}
        a = {}
        if (e1+' '+e2 in h_e_p):
            sum = 0.0
            for rel_path in h_e_p[e1+' '+e2]:
                b[rel_path] = h_e_p[e1+' '+e2][rel_path]
                sum += b[rel_path]
            for rel_path in b:
                b[rel_path]/=sum
                if b[rel_path]>0.01:
                    a[rel_path] = b[rel_path]
        g.write(str(len(a)))
        for rel_path in a:
            g.write(" "+str(len(rel_path.split()))+" "+rel_path+" "+str(a[rel_path]))
        g.write("\n")
        # g.write(str(e2)+" "+str(e1)+' '+str(rel+relation_num)+"\n")
        # e1 = seg[1]
        # e2 = seg[0]
        # b = {}
        # a = {}
        # if (e1+' '+e2 in h_e_p):
        #     sum = 0.0
        #     for rel_path in h_e_p[e1+' '+e2]:
        #         b[rel_path] = h_e_p[e1+' '+e2][rel_path]
        #         sum += b[rel_path]
        #     for rel_path in b:
        #         b[rel_path]/=sum
        #         if b[rel_path]>0.01:
        #             a[rel_path] = b[rel_path]
        # g.write(str(len(a)))
        # for rel_path in a:
        #     g.write(" "+str(len(rel_path.split()))+" "+rel_path+" "+str(a[rel_path]))
        # g.write("\n")
    f.close()
    g.close()
work("train")
work("test")
