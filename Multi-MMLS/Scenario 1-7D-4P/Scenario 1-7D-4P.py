#!/usr/bin/env python
# coding: utf-8

# In[25]:


#General Scenario 147 with Processivity


# ### Header Files

# In[26]:


import xlsxwriter 
import random
import matplotlib.pyplot as plt
import math
import numpy as np
import seaborn as sns
import csv
from timeit import default_timer as timer
import pdb
import os

from queue import Queue
from collections import deque
import queue
from numpy.random import permutation

from matplotlib.colors import LogNorm
from PIL import Image, ImageDraw, ImageFont
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from textwrap import wrap
import glob
import pandas as pd
import matplotlib.ticker as ticker



from matplotlib.colors import LinearSegmentedColormap
cmap_name = 'my_list'
colors = [(1, 1, 1), (0, 0, 1), (1, 0, 0)]  # White -> Blue -> Red
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=3) 


# In[27]:


script_dir = os.getcwd()
    
images_dir = os.path.join(script_dir, 'Outputs/')

if not os.path.isdir(images_dir):
    os.makedirs(images_dir)


# ### Output Files

# In[28]:


association_rate = float(input("Enter the association rate: "))
association_rate = association_rate*2

rows_count = 3
cols_count = 1000
segments = 3

cols1 = range(0,1000)


# Velocity steps:

# Velocity ratio : Va/Vb (Varying it)
vel_a = 5  #1000nm/s 
vel_b = 3  #800nm/s  


#Keeping processivity of A and B same ie Pa/Pb = 1
process_a = 1005   
process_b = 150

#Lifetime
lifetime = 250 #10 secs lifetime

gap = 0
minimum = 0
reservoir_length = 50

total_runtime2 = 4002
total_runtime = 3002 #1 min
time_stamp = 0.04

scenario = "1-7D-4P"
stagger1 = 25
stagger2 = 25


# In[29]:





# ### Data Inputs

# In[30]:


input_res = [Queue(maxsize = total_runtime) for l in range(segments+1)]

#Association
motor_cargo_a = [0 for l in range(segments)]    #no of a type motor cargos
motor_cargo_b = [0 for l in range(segments)]    #no of b type motor cargos
    
#Detachment at the end
throughput_a = [0 for l in range(segments)] #cargo_a output
throughput_b = [0 for l in range(segments)] #cargo_b output
    
lateral_a = [0 for l in range(segments)]
lateral_b = [0 for l in range(segments)]

#Motors lost due to detachment
detachment_a = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)] 
detachment_b = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]
    
#Motors used due to reattachment
reattachment_a = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]
reattachment_b = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]

heat_map_a = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]      
heat_map_b = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]
heat_map_a_2 = [[[0 for j in range(100)] for i in range(rows_count)] for l in range(segments)]      
heat_map_b_2 = [[[0 for j in range(100)] for i in range(rows_count)] for l in range(segments)]
heat_map_a_3 = [[[0 for j in range(200)] for i in range(rows_count)] for l in range(segments)]      
heat_map_b_3 = [[[0 for j in range(200)] for i in range(rows_count)] for l in range(segments)]

particle = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]
span = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]
velocity = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]
lifetime_cells = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]

waiting_a = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]  
waiting_b = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]  

leakage_a = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)] 
leakage_b = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)] 

productive_a = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)] 
productive_b = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)] 

non_productive_a = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)] 
non_productive_b = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]


wait_a = [0 for l in range(segments)]
wait_b = [0 for l in range(segments)]
leak_a = [0 for l in range(segments)]
leak_b = [0 for l in range(segments)]
detach_a = [0 for l in range(segments)]
detach_b = [0 for l in range(segments)]
reattach_a = [0 for l in range(segments)]
reattach_b = [0 for l in range(segments)]
detach_process_a = [0 for l in range(segments)]
detach_process_b = [0 for l in range(segments)]

reservoir_a_graph = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)] 
reservoir_b_graph = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)] 

output_a = [[[0 for j in range(total_runtime)] for i in range(rows_count)] for l in range(segments)] 
output_b = [[[0 for j in range(total_runtime)] for i in range(rows_count)] for l in range(segments)]

# In[31]:


class props(object): #detachment time and lifetime
    def __init__(self, joins, life):
        self.joins = joins
        self.life = life
        return
    
reservoir_a = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]
reservoir_b = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]

for t in range(segments):
    for i in range(rows_count):
        for j in range(cols_count):
            reservoir_a[t][i][j] = Queue(maxsize = reservoir_length)
            reservoir_b[t][i][j] = Queue(maxsize = reservoir_length)
        


# ### Functions

# #### Input Queue

# In[32]:


res_in_a_len = int((association_rate*total_runtime)/100)
res_in_b_len = int((association_rate*total_runtime)/100)
res_in_len_1 = total_runtime-(res_in_a_len + res_in_b_len)
res_in_len = total_runtime-res_in_len_1

res_in_l = []
res_in_l = deque()


for i in range(res_in_len_1):
    res_in_l.append(0)

for i in range(res_in_a_len):
    res_in_l.append(1)

for i in range(res_in_b_len):
    res_in_l.append(2)

random.shuffle(res_in_l)

# for i in range(res_in_len):
#     res_in_l.append(0)

for i in range(total_runtime):
    input_res[0].put(res_in_l[i])


# #### Attachment of cargo at the start

# In[33]:



def initial_association1(input_res, motor_cargo_a, motor_cargo_b, segment):
    
    start = timer()
    
    channels = list(range(0,rows_count))        # All channels
    random.shuffle(channels)
    c1 = channels[0]
    channels.remove(channels[0])
    c2 = channels[0]
    channels.remove(channels[0])
    c3 = channels[0]
    
    if(particle[segment][c1][0] == 0):
        particle[segment][c1][0] = input_res[segment].get()
        span[segment][c1][0] = 1
        lifetime_cells[segment][c1][0] = 1
        
        if(particle[segment][c1][0] == 1):
            motor_cargo_a[segment] += 1
            velocity[segment][c1][0] = vel_a

        elif(particle[segment][c1][0] == 2):
            motor_cargo_b[segment] += 1
            velocity[segment][c1][0] = vel_b
        
    
    elif(particle[segment][c2][0] == 0):
        particle[segment][c2][0] = input_res[segment].get()
        span[segment][c2][0] = 1
        lifetime_cells[segment][c2][0] = 1
        
        if(particle[segment][c2][0] == 1):
            motor_cargo_a[segment] += 1
            velocity[segment][c1][0] = vel_a

        elif(particle[segment][c2][0] == 2):
            motor_cargo_b[segment] += 1
            velocity[segment][c1][0] = vel_b
    
    elif(particle[segment][c3][0] == 0):
        particle[segment][c3][0] = input_res[segment].get()
        span[segment][c3][0] = 1
        lifetime_cells[segment][c3][0] = 1
        
        if(particle[segment][c3][0] == 1):
            motor_cargo_a[segment] += 1
            velocity[segment][c1][0] = vel_a
            
        elif(particle[segment][c3][0] == 2):
            motor_cargo_b[segment] += 1
            velocity[segment][c1][0] = vel_b

    end = timer()
    #print("Assocaition of 1 takes", end - start)
    #pdb.set_trace()
    #print(1)
    return input_res, motor_cargo_a, motor_cargo_b


# In[34]:



def initial_association4(input_res, motor_cargo_a, motor_cargo_b, segment):
    
    start = timer()
    
    c1 = 1
    
    if(particle[segment][c1][0] == 0):
        particle[segment][c1][0] = input_res[segment].get()
        span[segment][c1][0] = 1
        lifetime_cells[segment][c1][0] = 1
        
        if(particle[segment][c1][0] == 1):
            motor_cargo_a[segment] += 1
            velocity[segment][c1][0] = vel_a

        elif(particle[segment][c1][0] == 2):
            motor_cargo_b[segment] += 1
            velocity[segment][c1][0] = vel_b

    end = timer()
    #print("Association of 4 take", end - start)
    #pdb.set_trace()
    #print(2)
    return input_res, motor_cargo_a, motor_cargo_b


# In[35]:



def initial_association7(input_res, motor_cargo_a, motor_cargo_b, segment):
    
    start = timer()
    
    channels = list(range(0,rows_count))        # All channels
    random.shuffle(channels)
    c1 = channels[0]
    channels.remove(channels[0])
    c2 = channels[0]
    channels.remove(channels[0])
    c3 = channels[0]
    
    if(particle[segment][c1][0] == 0):
        particle[segment][c1][0] = input_res[segment].get()
        span[segment][c1][0] = 1
        lifetime_cells[segment][c1][0] = 1
        
        if(particle[segment][c1][0] == 1):
            motor_cargo_a[segment] += 1
            velocity[segment][c1][0] = vel_a

        elif(particle[segment][c1][0] == 2):
            motor_cargo_b[segment] += 1
            velocity[segment][c1][0] = vel_b
        
    
    elif(particle[segment][c2][0] == 0):
        particle[segment][c2][0] = input_res[segment].get()
        span[segment][c2][0] = 1
        lifetime_cells[segment][c2][0] = 1
        
        if(particle[segment][c2][0] == 1):
            motor_cargo_a[segment] += 1
            velocity[segment][c1][0] = vel_a

        elif(particle[segment][c2][0] == 2):
            motor_cargo_b[segment] += 1
            velocity[segment][c1][0] = vel_b
    
    elif(particle[segment][c3][0] == 0):
        particle[segment][c3][0] = input_res[segment].get()
        span[segment][c3][0] = 1
        lifetime_cells[segment][c3][0] = 1
        
        if(particle[segment][c3][0] == 1):
            motor_cargo_a[segment] += 1
            velocity[segment][c1][0] = vel_a
            
        elif(particle[segment][c3][0] == 2):
            motor_cargo_b[segment] += 1
            velocity[segment][c1][0] = vel_b

    end = timer()
    #print("Assocaition of 1 takes", end - start)
    #pdb.set_trace()
    #print(1)
    return input_res, motor_cargo_a, motor_cargo_b


# In[36]:


### Empty the queue with dead reservoirs
def empty_queues(rows_count, cols_count, reservoir_a, reservoir_b, leakage_a, leakage_b, time):
    for l in range(segments):
        for i in range(rows_count):
            for j in range(cols_count):
                if(reservoir_a[l][i][j].qsize() != 0):
                    t1 = reservoir_a[l][i][j].queue[0].joins
                    t2 = reservoir_a[l][i][j].queue[0].life
                    if(time-t1+t2 > lifetime):
                        #remove the element as leakage
                        #print("Leak A")
                        reservoir_a[l][i][j].get()
                        leakage_a[l][i][j] += 1
                        
                if(reservoir_b[l][i][j].qsize() != 0):
                    t3 = reservoir_b[l][i][j].queue[0].joins
                    t4 = reservoir_b[l][i][j].queue[0].life
                    if(time-t3+t4 > lifetime):
                        #remove the element as leakage
                        #print("Leak B")
                        reservoir_b[l][i][j].get()
                        leakage_b[l][i][j] += 1

    return reservoir_a, reservoir_b


# #### Lateral Reattachment

# In[37]:



def lateral_association1(rows_count, cols_count, reservoir_a, reservoir_b, reattachment_a, reattachment_b, reattach_a, reattach_b, leakage_a, leakage_b, segment, time):
    
    start = timer()
    i=0
    j=0
    k=0
    temp = 0
    track = 0
    site = 0
    flag = 0
    flag2 = 0
    for i in range(rows_count):
        for j in range(cols_count):
            if(reservoir_a[segment][i][j].qsize() != 0 and reservoir_b[segment][i][j].qsize() == 0):
                flag = 0
            elif(reservoir_a[segment][i][j].qsize() == 0 and reservoir_b[segment][i][j].qsize() != 0):
                flag = 1 
            elif(reservoir_a[segment][i][j].qsize() != 0 and reservoir_b[segment][i][j].qsize() != 0):
                flag = random.randint(0,1)
            else:
                flag = 10
            
            if(flag == 0):
                channels = list(range(0,rows_count))
                channels.remove(i)
                random.shuffle(channels)
                track1 = channels[0]
                track2 = channels[1]
                track = i
                site = j
                if(j == cols_count-1):
                    if(particle[segment][i][j] == 0): site = j; track = i
                    elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                    elif(particle[segment][track1][j] == 0): site = j; track = track1
                    elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                    elif(particle[segment][track2][j] == 0): site = j; track = track2
                    elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                    else:  continue
                else:
                    if(particle[segment][i][j+1] == 0): site = j+1; track = i
                    elif(particle[segment][track1][j+1] == 0): site = j+1; track = track1
                    elif(particle[segment][track2][j+1] == 0): site = j+1; track = track2
                    elif(particle[segment][i][j] == 0): site = j; track = i
                    elif(particle[segment][track1][j] == 0): site = j; track = track1
                    elif(particle[segment][track2][j] == 0): site = j; track = track2 
                    elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                    elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                    elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                    else:  continue
                        
                        
                particle[segment][track][site] = 1
                span[segment][track][site] = 1
                velocity[segment][track][site] = vel_a

                t = reservoir_a[segment][i][j].get()
                lifetime_cells[segment][track][site] = time-t.joins+t.life
                #print("Reattach A")
                reattachment_a[segment][track][site] += 1
                reattach_a[segment] += 1
    
            elif(flag == 1):
                channels = list(range(0,rows_count))
                channels.remove(i)
                random.shuffle(channels)
                track1 = channels[0]
                track2 = channels[1]
                track = i
                site = j
                if(j == cols_count-1):
                    if(particle[segment][i][j] == 0): site = j; track = i
                    elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                    elif(particle[segment][track1][j] == 0): site = j; track = track1
                    elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                    elif(particle[segment][track2][j] == 0): site = j; track = track2
                    elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                    else:  continue
                else:
                    if(particle[segment][i][j+1] == 0): site = j+1; track = i
                    elif(particle[segment][track1][j+1] == 0): site = j+1; track = track1
                    elif(particle[segment][track2][j+1] == 0): site = j+1; track = track2
                    elif(particle[segment][i][j] == 0): site = j; track = i
                    elif(particle[segment][track1][j] == 0): site = j; track = track1
                    elif(particle[segment][track2][j] == 0): site = j; track = track2 
                    elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                    elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                    elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                    else:  continue
                    
                particle[segment][track][site] = 2
                span[segment][track][site] = 1
                velocity[segment][track][site] = vel_b

                t = reservoir_b[segment][i][j].get()
                lifetime_cells[segment][track][site] = time-t.joins+t.life
                #print("Reattach B")
                reattachment_b[segment][track][site] += 1
                reattach_b[segment] += 1
            else:
                continue
                
                
    end = timer()
    #print("Lateral 1 take", end - start)
    #pdb.set_trace()
    #print(4)
    return reservoir_a, reservoir_b, reattachment_a, reattachment_b, reattach_a, reattach_b, leakage_a, leakage_b


# In[38]:



def lateral_association4(rows_count, cols_count, reservoir_a, reservoir_b, reattachment_a, reattachment_b, reattach_a, reattach_b, leakage_a, leakage_b, segment, time):
    
    start = timer()
    i=0
    j=0
    k=0
    temp = 0
    track = 0
    site = 0
    flag = 0
    flag2 = 0
    for i in range(rows_count):
        for j in range(cols_count):
            if(reservoir_a[segment][i][j].qsize() != 0 and reservoir_b[segment][i][j].qsize() == 0):
                flag = 0
            elif(reservoir_a[segment][i][j].qsize() == 0 and reservoir_b[segment][i][j].qsize() != 0):
                flag = 1 
            elif(reservoir_a[segment][i][j].qsize() != 0 and reservoir_b[segment][i][j].qsize() != 0):
                flag = random.randint(0,1)
            else:
                flag = 10
            
            if(flag == 0):
                channels = list(range(0,rows_count))
                channels.remove(i)
                random.shuffle(channels)
                track1 = channels[0]
                track2 = channels[1]
                track = i
                site = j
                if(j == cols_count-1):
                    if(particle[segment][i][j] == 0): site = j; track = i
                    elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                    elif(particle[segment][track1][j] == 0): site = j; track = track1
                    elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                    elif(particle[segment][track2][j] == 0): site = j; track = track2
                    elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                    else:  continue 
                else:
                    if(i == 1 and j == 1):
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][i][j] == 0): site = j; track = i
                    
                    elif(i == 1 and j <= (stagger1/100)*cols_count):
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][i][j] == 0): site = j; track = i
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        else: continue
                    
                    elif(j > (stagger1/100)*cols_count):
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][track1][j+1] == 0): site = j+1; track = track1
                        elif(particle[segment][track2][j+1] == 0): site = j+1; track = track2
                        elif(particle[segment][i][j] == 0): site = j; track = i
                        elif(particle[segment][track1][j] == 0): site = j; track = track1
                        elif(particle[segment][track2][j] == 0): site = j; track = track2 
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                        elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                        else:  continue 
                        
                        
                particle[segment][track][site] = 1
                span[segment][track][site] = 1
                velocity[segment][track][site] = vel_a

                t = reservoir_a[segment][i][j].get()
                lifetime_cells[segment][track][site] = time-t.joins+t.life
                #print("Reattach A")
                reattachment_a[segment][track][site] += 1
                reattach_a[segment] += 1
    
            elif(flag == 1):
                channels = list(range(0,rows_count))
                channels.remove(i)
                random.shuffle(channels)
                track1 = channels[0]
                track2 = channels[1]
                track = i
                site = j
                if(j == cols_count-1):
                    if(particle[segment][i][j] == 0): site = j; track = i
                    elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                    elif(particle[segment][track1][j] == 0): site = j; track = track1
                    elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                    elif(particle[segment][track2][j] == 0): site = j; track = track2
                    elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                    else:  continue 
                else:
                    if(i == 1 and j == 1):
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][i][j] == 0): site = j; track = i
                    
                    elif(i == 1 and j <= (stagger1/100)*cols_count):
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][i][j] == 0): site = j; track = i
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        else: continue
                    
                    elif(j > (stagger1/100)*cols_count):
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][track1][j+1] == 0): site = j+1; track = track1
                        elif(particle[segment][track2][j+1] == 0): site = j+1; track = track2
                        elif(particle[segment][i][j] == 0): site = j; track = i
                        elif(particle[segment][track1][j] == 0): site = j; track = track1
                        elif(particle[segment][track2][j] == 0): site = j; track = track2 
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                        elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                        else:  continue 
                    
                particle[segment][track][site] = 2
                span[segment][track][site] = 1
                velocity[segment][track][site] = vel_b

                t = reservoir_b[segment][i][j].get()
                lifetime_cells[segment][track][site] = time-t.joins+t.life
                #print("Reattach B")
                reattachment_b[segment][track][site] += 1
                reattach_b[segment] += 1
            else:
                continue
                
                
    end = timer()
    #print("Lateral 4 take", end - start)
    #pdb.set_trace()
    #print(5)
    return reservoir_a, reservoir_b, reattachment_a, reattachment_b, reattach_a, reattach_b, leakage_a, leakage_b


# In[39]:



def lateral_association7(rows_count, cols_count, reservoir_a, reservoir_b, reattachment_a, reattachment_b, reattach_a, reattach_b, leakage_a, leakage_b, segment, time):
    
    start = timer()
    i=0
    j=0
    k=0
    temp = 0
    track = 0
    site = 0
    flag = 0
    flag2 = 0
    for i in range(rows_count):
        for j in range(cols_count):
            if(reservoir_a[segment][i][j].qsize() != 0 and reservoir_b[segment][i][j].qsize() == 0):
                flag = 0
            elif(reservoir_a[segment][i][j].qsize() == 0 and reservoir_b[segment][i][j].qsize() != 0):
                flag = 1 
            elif(reservoir_a[segment][i][j].qsize() != 0 and reservoir_b[segment][i][j].qsize() != 0):
                flag = random.randint(0,1)
            else:
                flag = 10
            
            if(flag == 0):
                channels = list(range(0,rows_count))
                channels.remove(i)
                random.shuffle(channels)
                track1 = channels[0]
                track2 = channels[1]
                track = i
                site = j
                if(i==1):
                    if(j==cols_count-1):
                        if(particle[segment][i][j] == 0): site = j; track = i 
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        else:  continue
                    else:
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][i][j] == 0): site = j; track = i
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        else: continue
                
                else:
                    if(j>=(cols_count-(stagger2/100)*cols_count)):
                        if(particle[segment][1][j+1] == 0): site = j+1; track = 1
                        elif(particle[segment][1][j] == 0): site = j; track = 1
                        elif(particle[segment][1][j-1] == 0): site = j-1; track = 1
                        else: continue
                    elif(j<(cols_count-(stagger2/100)*cols_count)):
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][track1][j+1] == 0): site = j+1; track = track1
                        elif(particle[segment][track2][j+1] == 0): site = j+1; track = track2
                        elif(particle[segment][i][j] == 0): site = j; track = i
                        elif(particle[segment][track1][j] == 0): site = j; track = track1
                        elif(particle[segment][track2][j] == 0): site = j; track = track2 
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                        elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                        else:  continue
                        
                particle[segment][track][site] = 1
                span[segment][track][site] = 1
                velocity[segment][track][site] = vel_a

                t = reservoir_a[segment][i][j].get()
                lifetime_cells[segment][track][site] = time-t.joins+t.life
                #print("Reattach A")
                reattachment_a[segment][track][site] += 1
                reattach_a[segment] += 1
    
            elif(flag == 1):
                channels = list(range(0,rows_count))
                channels.remove(i)
                random.shuffle(channels)
                track1 = channels[0]
                track2 = channels[1]
                track = j
                if(i==1):
                    if(j==cols_count-1):
                        if(particle[segment][i][j] == 0): site = j; track = i 
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        else:  continue
                    else:
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][i][j] == 0): site = j; track = i
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        else: continue
                
                else:
                    if(j>=(cols_count-(stagger2/100)*cols_count)):
                        if(particle[segment][1][j+1] == 0): site = j+1; track = 1
                        elif(particle[segment][1][j] == 0): site = j; track = 1
                        elif(particle[segment][1][j-1] == 0): site = j-1; track = 1
                        else: continue
                    elif(j<(cols_count-(stagger2/100)*cols_count)):
                        if(particle[segment][i][j+1] == 0): site = j+1; track = i
                        elif(particle[segment][track1][j+1] == 0): site = j+1; track = track1
                        elif(particle[segment][track2][j+1] == 0): site = j+1; track = track2
                        elif(particle[segment][i][j] == 0): site = j; track = i
                        elif(particle[segment][track1][j] == 0): site = j; track = track1
                        elif(particle[segment][track2][j] == 0): site = j; track = track2 
                        elif(particle[segment][i][j-1] == 0): site = j-1; track = i
                        elif(particle[segment][track1][j-1] == 0): site = j-1; track = track1
                        elif(particle[segment][track2][j-1] == 0): site = j-1; track = track2 
                        else:  continue
                
                    
                particle[segment][track][site] = 2
                span[segment][track][site] = 1
                velocity[segment][track][site] = vel_b

                t=reservoir_b[segment][i][j].get()
                lifetime_cells[segment][track][site] = time-t.joins+t.life
                #print("Reattach B")
                reattachment_b[segment][track][site] += 1
                reattach_b[segment] += 1
            
            else:
                continue
                
                
    end = timer()
    #print("Lateral 7 take", end - start)
    #pdb.set_trace()
    #print(6)
    return reservoir_a, reservoir_b, reattachment_a, reattachment_b, reattach_a, reattach_b, leakage_a, leakage_b


# #### Transport (Cellular Automata)

# In[40]:



def transport1(input_res, rows_count, cols_count, vel_a, vel_b, process_a, process_b, throughput_a, throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b, detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, segment, output_a, output_b, time):
    
    start=timer()
    flag = 0
    for i in range(rows_count):
        gap=0
        minimum=0
        for j in range(cols_count-1,-1,-1):
            if(particle[segment][i][j] == 0):
                gap += 1
                continue
            else:
                #Output
                if(particle[segment][i][j] == 1):
                    if(gap < vel_a):
                        minimum = 0 
                    elif(gap >= vel_a):      
                        minimum = vel_a 
                
                #Constant velocity
                elif(particle[segment][i][j] == 2):
                    if(gap < vel_b):
                        minimum = 0 
                    elif(gap >= vel_b):      
                        minimum = vel_b
                        
                             
                #Movement
                if(minimum > 0):
                    if(particle[segment][i][j] == 1):
                        if((j + vel_a) >= cols_count-1):
                            throughput_a[segment] += 1
                            output_a[segment][i][time] += 1
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            flag = 1
                            input_res[segment+1].put(1)
                        
                        else:
                            particle[segment][i][j+minimum] = 1
                            span[segment][i][j+minimum] = span[segment][i][j] + minimum
                            velocity[segment][i][j+minimum] = vel_a
                            lifetime_cells[segment][i][j+minimum] = lifetime_cells[segment][i][j]
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            if(span[segment][i][j+minimum] >= process_a):    
                                #detachment if motor exceeds its processivity
                                particle[segment][i][j+minimum] = 0
                                span[segment][i][j+minimum] = 0
                                velocity[segment][i][j+minimum] = 0
                                #print('y1')
                                if(reservoir_a[segment][i][j].qsize()==reservoir_length):
                                    reservoir_a[segment][i][j].get()
                                    leakage_a[segment][i][j] += 1
                                    
                                reservoir_a[segment][i][j].put(props(time,lifetime_cells[segment][i][j+minimum]))
                                
                                lifetime_cells[segment][i][j+minimum]=0
                                detachment_a[segment][i][j+minimum] += 1
                                detach_a[segment] += 1
                                detach_process_a[segment] += 1
                                
                    elif(particle[segment][i][j] == 2):
                        if((j + vel_b) >= cols_count-1):
                            throughput_b[segment] += 1
                            output_b[segment][i][time] += 1
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            flag = 1
                            input_res[segment+1].put(2)
                        
                        else:
                            particle[segment][i][j+minimum] = 2
                            span[segment][i][j+minimum] = span[segment][i][j] + minimum
                            velocity[segment][i][j+minimum] = vel_b
                            lifetime_cells[segment][i][j+minimum] = lifetime_cells[segment][i][j]
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            if(span[segment][i][j+minimum] >= process_b):    
                                #detachment if motor exceeds its processivity
                                particle[segment][i][j+minimum] = 0
                                span[segment][i][j+minimum] = 0
                                velocity[segment][i][j+minimum] = 0
                                #print('y2')
                                if(reservoir_b[segment][i][j].qsize()==reservoir_length):
                                    reservoir_b[segment][i][j].get()
                                    leakage_b[segment][i][j] += 1
                                
                                reservoir_b[segment][i][j].put(props(time,lifetime_cells[segment][i][j+minimum]))
                                
                                lifetime_cells[segment][i][j+minimum]=0
                                detachment_b[segment][i][j+minimum] += 1
                                detach_b[segment] += 1
                                detach_process_b[segment] += 1
                #Detachment         
                elif(minimum == 0):
                    if(particle[segment][i][j] == 1):
                        # Lateral association will happen to only cargos lost at initial stages
                        channels = list(range(0,rows_count))        # All channels
                        channels.remove(i)
                        random.shuffle(channels)
                        y1 = channels[0]
                        channels.remove(channels[0])
                        y2 = channels[0]
            
                        if((j + vel_a) >= cols_count-1):
                            throughput_a[segment] += 1
                            output_a[segment][i][time] += 1
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            lateral_a[segment] += 1
                            flag = 1
                            input_res[segment+1].put(1)
                        
                        else:    
                            if(particle[segment][y1][j+vel_a] == 0):
                                particle[segment][y1][j+vel_a] = 1
                                span[segment][y1][j+vel_a] = span[segment][i][j] + vel_a
                                velocity[segment][y1][j+vel_a] = vel_a
                                lifetime_cells[segment][y1][j+vel_a] = lifetime_cells[segment][i][j]
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                lifetime_cells[segment][i][j] = 0
                                lateral_a[segment] += 1
                            
                            elif(particle[segment][y2][j+vel_a] == 0):
                                particle[segment][y2][j+vel_a] = 1
                                span[segment][y2][j+vel_a] = span[segment][i][j] + vel_a
                                velocity[segment][y2][j+vel_a] = vel_a
                                lifetime_cells[segment][y2][j+vel_a] = lifetime_cells[segment][i][j]
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                lifetime_cells[segment][i][j] = 0
                                lateral_a[segment] += 1
                            
                            else:
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                #print('y3')
                                if(reservoir_a[segment][i][j].qsize()==reservoir_length):
                                    reservoir_a[segment][i][j].get()
                                    leakage_a[segment][i][j] += 1
                                
                                reservoir_a[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))
                                
                                lifetime_cells[segment][i][j]=0
                                detachment_a[segment][i][j] += 1
                                detach_a[segment] += 1

                    elif(particle[segment][i][j] == 2):
                        channels = list(range(0,rows_count))        # All channels
                        channels.remove(i)
                        random.shuffle(channels)
                        y1 = channels[0]
                        channels.remove(channels[0])
                        y2 = channels[0]
                        
                        if((j + vel_b) >= cols_count-1):
                            throughput_b[segment] += 1
                            output_b[segment][i][time] += 1
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            lateral_b[segment] += 1
                            flag = 1
                            input_res[segment+1].put(2)
                        
                        else:    
                            if(particle[segment][y1][j+vel_b]== 0):
                                particle[segment][y1][j+vel_b] = 2
                                span[segment][y1][j+vel_b] = span[segment][i][j] + vel_b
                                velocity[segment][y1][j+vel_b] = vel_b
                                lifetime_cells[segment][y1][j+vel_b] = lifetime_cells[segment][i][j]
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                lifetime_cells[segment][i][j] = 0
                                lateral_b[segment] += 1
                            
                            elif(particle[segment][y2][j+vel_b]== 0):
                                particle[segment][y2][j+vel_b] = 2
                                span[segment][y2][j+vel_b] = span[segment][i][j] + vel_b
                                velocity[segment][y2][j+vel_b] = vel_b
                                lifetime_cells[segment][y2][j+vel_b] = lifetime_cells[segment][i][j]
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                lifetime_cells[segment][i][j] = 0
                                lateral_b[segment] += 1
                                
                            else:
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                #print('y4')
                                if(reservoir_b[segment][i][j].qsize()==reservoir_length):
                                    reservoir_b[segment][i][j].get()
                                    leakage_b[segment][i][j] += 1
                                
                                reservoir_b[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))
                                
                                lifetime_cells[segment][i][j]=0
                                detachment_b[segment][i][j] += 1
                                detach_b[segment] += 1
                
                gap = 0
    
    if(flag == 0):
        input_res[segment+1].put(0)
        
    end = timer()
    #print("Transport 1 take", end - start)            
    #pdb.set_trace()
    #print(7)
    return input_res, throughput_a, throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b, detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, output_a, output_b


# In[41]:



def transport4(input_res, rows_count, cols_count, vel_a, vel_b, process_a, process_b, throughput_a, throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b, detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, segment, output_a, output_b, time):
    
    start=timer()
    flag = 0
    for i in range(rows_count):
        gap=0
        minimum=0
        for j in range(cols_count-1,-1,-1):
            if(particle[segment][i][j] == 0):
                gap += 1
                continue
            else:
                #Output
                if(particle[segment][i][j] == 1):
                    if(gap < vel_a):
                        minimum = 0 
                    elif(gap >= vel_a):      
                        minimum = vel_a 
                
                #Constant velocity
                elif(particle[segment][i][j] == 2):
                    if(gap < vel_b):
                        minimum = 0 
                    elif(gap >= vel_b):      
                        minimum = vel_b
                        
                             
                #Movement
                if(minimum > 0):
                    if(particle[segment][i][j] == 1):
                        if((j + vel_a) >= cols_count-1):
                            throughput_a[segment] += 1
                            output_a[segment][i][time] += 1
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            flag = 1
                            input_res[segment+1].put(1)
                        
                        else:
                            particle[segment][i][j+minimum] = 1
                            span[segment][i][j+minimum] = span[segment][i][j] + minimum
                            velocity[segment][i][j+minimum] = vel_a
                            lifetime_cells[segment][i][j+minimum] = lifetime_cells[segment][i][j]
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            if(span[segment][i][j+minimum] >= process_a):    
                                #detachment if motor exceeds its processivity
                                particle[segment][i][j+minimum] = 0
                                span[segment][i][j+minimum] = 0
                                velocity[segment][i][j+minimum] = 0
                                #print('y1')
                                if(reservoir_a[segment][i][j].qsize()==reservoir_length):
                                    reservoir_a[segment][i][j].get()
                                    leakage_a[segment][i][j] += 1
                                    
                                reservoir_a[segment][i][j].put(props(time,lifetime_cells[segment][i][j+minimum]))
                                
                                lifetime_cells[segment][i][j+minimum]=0
                                detachment_a[segment][i][j+minimum] += 1
                                detach_a[segment] += 1
                                
                    elif(particle[segment][i][j] == 2):
                        if((j + vel_b) >= cols_count-1):
                            throughput_b[segment] += 1
                            output_b[segment][i][time] += 1
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            flag = 1
                            input_res[segment+1].put(2)
                        
                        else:
                            particle[segment][i][j+minimum] = 2
                            span[segment][i][j+minimum] = span[segment][i][j] + minimum
                            velocity[segment][i][j+minimum] = vel_b
                            lifetime_cells[segment][i][j+minimum] = lifetime_cells[segment][i][j]
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            if(span[segment][i][j+minimum] >= process_b):    
                                #detachment if motor exceeds its processivity
                                particle[segment][i][j+minimum] = 0
                                span[segment][i][j+minimum] = 0
                                velocity[segment][i][j+minimum] = 0
                                #print('y2')
                                if(reservoir_b[segment][i][j].qsize()==reservoir_length):
                                    reservoir_b[segment][i][j].get()
                                    leakage_b[segment][i][j] += 1
                                
                                reservoir_b[segment][i][j].put(props(time,lifetime_cells[segment][i][j+minimum]))
                                
                                lifetime_cells[segment][i][j+minimum]=0
                                detachment_b[segment][i][j+minimum] += 1
                                detach_b[segment] += 1
                                
                #Detachment         
                elif(minimum == 0):
                    if(particle[segment][i][j] == 1):
                        if(j>(stagger1/100)*cols_count):
                            # Lateral association will happen to only cargos lost at initial stages
                            channels = list(range(0,rows_count))        # All channels
                            channels.remove(i)
                            random.shuffle(channels)
                            y1 = channels[0]
                            channels.remove(channels[0])
                            y2 = channels[0]

                            if((j + vel_a) >= cols_count-1):
                                throughput_a[segment] += 1
                                output_a[segment][i][time] += 1
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                lifetime_cells[segment][i][j] = 0
                                lateral_a[segment] += 1
                                flag = 1
                                input_res[segment+1].put(1)
                            
                            else:    
                                if(particle[segment][y1][j+vel_a] == 0):
                                    particle[segment][y1][j+vel_a] = 1
                                    span[segment][y1][j+vel_a] = span[segment][i][j] + vel_a
                                    velocity[segment][y1][j+vel_a] = vel_a
                                    lifetime_cells[segment][y1][j+vel_a] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_a[segment] += 1

                                elif(particle[segment][y2][j+vel_a] == 0):
                                    particle[segment][y2][j+vel_a] = 1
                                    span[segment][y2][j+vel_a] = span[segment][i][j] + vel_a
                                    velocity[segment][y2][j+vel_a] = vel_a 
                                    lifetime_cells[segment][y2][j+vel_a] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_a[segment] += 1

                                else:
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    #print('y3')
                                    if(reservoir_a[segment][i][j].qsize()==reservoir_length):
                                        reservoir_a[segment][i][j].get()
                                        leakage_a[segment][i][j] += 1

                                    reservoir_a[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                                    lifetime_cells[segment][i][j]=0
                                    detachment_a[segment][i][j] += 1
                                    detach_a[segment] += 1
                                    
                        elif(j<=(stagger1/100)*cols_count):
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            #print('y3')
                            if(reservoir_a[segment][i][j].qsize()==reservoir_length):
                                reservoir_a[segment][i][j].get()
                                leakage_a[segment][i][j] += 1

                            reservoir_a[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                            lifetime_cells[segment][i][j]=0
                            detachment_a[segment][i][j] += 1
                            detach_a[segment] += 1

                    elif(particle[segment][i][j] == 2):
                        if(j>(stagger1/100)*cols_count):
                            channels = list(range(0,rows_count))        # All channels
                            channels.remove(i)
                            random.shuffle(channels)
                            y1 = channels[0]
                            channels.remove(channels[0])
                            y2 = channels[0]

                            if((j + vel_b) >= cols_count-1):
                                throughput_b[segment] += 1
                                output_b[segment][i][time] += 1
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                lifetime_cells[segment][i][j] = 0
                                lateral_b[segment] += 1
                                flag = 1
                                input_res[segment+1].put(2)
                            
                            else:    
                                if(particle[segment][y1][j+vel_b]== 0):
                                    particle[segment][y1][j+vel_b] = 2
                                    span[segment][y1][j+vel_b] = span[segment][i][j] + vel_b
                                    velocity[segment][y1][j+vel_b] = vel_b
                                    lifetime_cells[segment][y1][j+vel_b] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_b[segment] += 1
                                
                                elif(particle[segment][y2][j+vel_b]== 0):
                                    particle[segment][y2][j+vel_b] = 2
                                    span[segment][y2][j+vel_b] = span[segment][i][j] + vel_b
                                    velocity[segment][y2][j+vel_b] = vel_b
                                    lifetime_cells[segment][y2][j+vel_b] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_b[segment] += 1
                                    
                                else:
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    #print('y4')
                                    if(reservoir_b[segment][i][j].qsize()==reservoir_length):
                                        reservoir_b[segment][i][j].get()
                                        leakage_b[segment][i][j] += 1

                                    reservoir_b[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                                    lifetime_cells[segment][i][j]=0
                                    detachment_b[segment][i][j] += 1
                                    detach_b[segment] += 1
                            
                        elif(j<=(stagger1/100)*cols_count):
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            #print('y4')
                            if(reservoir_b[segment][i][j].qsize()==reservoir_length):
                                reservoir_b[segment][i][j].get()
                                leakage_b[segment][i][j] += 1

                            reservoir_b[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                            lifetime_cells[segment][i][j]=0
                            detachment_b[segment][i][j] += 1
                            detach_b[segment] += 1
                
                gap = 0
    
    if(flag == 0):
        input_res[segment+1].put(0)
        
    end = timer()
    #print("Transport 4 take", end - start)            
    #pdb.set_trace()
    #print(8)
    
    return input_res, throughput_a, throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b, detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, output_a, output_b


# In[42]:



def transport7(input_res, rows_count, cols_count, vel_a, vel_b, process_a, process_b, throughput_a, throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b, detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, segment, output_a, output_b, time):
    
    start=timer()
    flag = 0
    
    for i in range(rows_count):
        gap=0
        minimum=0
        for j in range(cols_count-1,-1,-1):
            if(particle[segment][i][j] == 0):
                gap += 1
                continue
            else:
                #Output
                if(particle[segment][i][j] == 1):
                    if(i==1):
                        if(gap < vel_a):
                            minimum = 0 
                        elif(gap >= vel_a):      
                            minimum = vel_a
                    else:
                        if(j>(cols_count-(stagger2/100)*cols_count) or gap < vel_a):
                            minimum = 0 
                        elif(gap >= vel_a):      
                            minimum = vel_a 
                
                #Constant velocity
                elif(particle[segment][i][j] == 2):
                    if(i==1):
                        if(gap < vel_b):
                            minimum = 0 
                        elif(gap >= vel_b):      
                            minimum = vel_b
                    else:
                        if(j>(cols_count-(stagger2/100)*cols_count) or gap < vel_b):
                            minimum = 0 
                        elif(gap >= vel_b):      
                            minimum = vel_b
                        
                             
                #Movement
                if(minimum > 0):
                    if(particle[segment][i][j] == 1):
                        if((j + vel_a) >= cols_count-1):
                            throughput_a[segment] += 1
                            output_a[segment][i][time] += 1
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            flag = 1
                            input_res[segment+1].put(1)
                        
                        else:
                            particle[segment][i][j+minimum] = 1
                            span[segment][i][j+minimum] = span[segment][i][j] + minimum
                            velocity[segment][i][j+minimum] = vel_a 
                            lifetime_cells[segment][i][j+minimum] = lifetime_cells[segment][i][j]
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            if(span[segment][i][j+minimum] >= process_a):    
                                #detachment if motor exceeds its processivity
                                particle[segment][i][j+minimum] = 0
                                span[segment][i][j+minimum] = 0
                                velocity[segment][i][j+minimum] = 0
                                #print('y1')
                                if(reservoir_a[segment][i][j].qsize()==reservoir_length):
                                    reservoir_a[segment][i][j].get()
                                    leakage_a[segment][i][j] += 1
                                    
                                reservoir_a[segment][i][j].put(props(time,lifetime_cells[segment][i][j+minimum]))
                                
                                lifetime_cells[segment][i][j+minimum]=0
                                detachment_a[segment][i][j+minimum] += 1
                                detach_a[segment] += 1
                                
                    elif(particle[segment][i][j] == 2):
                        if((j + vel_b) >= cols_count-1):
                            throughput_b[segment] += 1
                            output_b[segment][i][time] += 1
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            flag = 1
                            input_res[segment+1].put(2)
                        
                        else:
                            particle[segment][i][j+minimum] = 2
                            span[segment][i][j+minimum] = span[segment][i][j] + minimum
                            velocity[segment][i][j+minimum] = vel_b
                            lifetime_cells[segment][i][j+minimum] = lifetime_cells[segment][i][j]
                            particle[segment][i][j] = 0
                            span[segment][i][j] = 0
                            velocity[segment][i][j] = 0
                            lifetime_cells[segment][i][j] = 0
                            if(span[segment][i][j+minimum] >= process_b):    
                                #detachment if motor exceeds its processivity
                                particle[segment][i][j+minimum] = 0
                                span[segment][i][j+minimum] = 0
                                velocity[segment][i][j+minimum] = 0 
                                #print('y2')
                                if(reservoir_b[segment][i][j].qsize()==reservoir_length):
                                    reservoir_b[segment][i][j].get()
                                    leakage_b[segment][i][j] += 1
                                
                                reservoir_b[segment][i][j].put(props(time,lifetime_cells[segment][i][j+minimum]))
                                
                                lifetime_cells[segment][i][j+minimum]=0
                                detachment_b[segment][i][j+minimum] += 1
                                detach_b[segment] += 1
                                
                #Detachment         
                elif(minimum == 0):
                    if(particle[segment][i][j] == 1):
                        if(j<((cols_count-(stagger2/100)*cols_count)-vel_a)):
                            # Lateral association will happen to only cargos lost at initial stages
                            channels = list(range(0,rows_count))        # All channels
                            channels.remove(i)
                            random.shuffle(channels)
                            y1 = channels[0]
                            channels.remove(channels[0])
                            y2 = channels[0]

                            if((j + vel_a) >= cols_count-1):
                                throughput_a[segment] += 1
                                output_a[segment][i][time] += 1
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                lifetime_cells[segment][i][j] = 0
                                lateral_a[segment] += 1
                                flag = 1
                                input_res[segment+1].put(1)
                            else:    
                                if(particle[segment][y1][j+vel_a] == 0):
                                    particle[segment][y1][j+vel_a] = 1
                                    span[segment][y1][j+vel_a] = span[segment][i][j] + vel_a
                                    velocity[segment][y1][j+vel_a] = vel_a
                                    lifetime_cells[segment][y1][j+vel_a] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_a[segment] += 1

                                elif(particle[segment][y2][j+vel_a] == 0):
                                    particle[segment][y2][j+vel_a] = 1
                                    span[segment][y2][j+vel_a] = span[segment][i][j] + vel_a
                                    velocity[segment][y2][j+vel_a] = vel_a
                                    lifetime_cells[segment][y2][j+vel_a] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_a[segment] += 1

                                else:
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    #print('y3')
                                    if(reservoir_a[segment][i][j].qsize()==reservoir_length):
                                        reservoir_a[segment][i][j].get()
                                        leakage_a[segment][i][j] += 1

                                    reservoir_a[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                                    lifetime_cells[segment][i][j]=0
                                    detachment_a[segment][i][j] += 1
                                    detach_a[segment] += 1
                                    
                        elif(j >= ((cols_count-(stagger2/100)*cols_count)-vel_a)):
                            if(i == 1):
                                if((j + vel_a) >= cols_count-1):
                                    throughput_a[segment] += 1
                                    output_a[segment][i][time] += 1
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    flag = 1
                                    input_res[segment+1].put(1)
                                
                                else:
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    #print('y3')
                                    if(reservoir_a[segment][i][j].qsize()==reservoir_length):
                                        reservoir_a[segment][i][j].get()
                                        leakage_a[segment][i][j] += 1

                                    reservoir_a[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                                    lifetime_cells[segment][i][j]=0
                                    detachment_a[segment][i][j] += 1
                                    detach_a[segment] += 1
                            
                            else:
                                if(particle[segment][1][j+vel_a] == 0):
                                    particle[segment][1][j+vel_a] = 1
                                    span[segment][1][j+vel_a] = span[segment][i][j] + vel_a
                                    velocity[segment][1][j+vel_a] = vel_a 
                                    lifetime_cells[segment][1][j+vel_a] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_a[segment] += 1

                                else:
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    #print('y3')
                                    if(reservoir_a[segment][i][j].qsize()==reservoir_length):
                                        reservoir_a[segment][i][j].get()
                                        leakage_a[segment][i][j] += 1

                                    reservoir_a[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                                    lifetime_cells[segment][i][j]=0
                                    detachment_a[segment][i][j] += 1
                                    detach_a[segment] += 1

                    elif(particle[segment][i][j] == 2):
                        if(j < ((cols_count-(stagger2/100)*cols_count)-vel_b)):
                            channels = list(range(0,rows_count))        # All channels
                            channels.remove(i)
                            random.shuffle(channels)
                            y1 = channels[0]
                            channels.remove(channels[0])
                            y2 = channels[0]

                            if((j + vel_b) >= cols_count-1):
                                throughput_b[segment] += 1
                                output_b[segment][i][time] += 1
                                particle[segment][i][j] = 0
                                span[segment][i][j] = 0
                                velocity[segment][i][j] = 0
                                lifetime_cells[segment][i][j] = 0
                                lateral_b[segment] += 1
                                flag = 1
                                input_res[segment+1].put(2)
                            else:    
                                if(particle[segment][y1][j+vel_b]== 0):
                                    particle[segment][y1][j+vel_b] = 2
                                    span[segment][y1][j+vel_b] = span[segment][i][j] + vel_b
                                    velocity[segment][y1][j+vel_b] = vel_b
                                    lifetime_cells[segment][y1][j+vel_b] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_b[segment] += 1
                                
                                elif(particle[segment][y2][j+vel_b]== 0):
                                    particle[segment][y2][j+vel_b] = 2
                                    span[segment][y2][j+vel_b] = span[segment][i][j] + vel_b
                                    velocity[segment][y2][j+vel_b] = vel_b
                                    lifetime_cells[segment][y2][j+vel_b] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_b[segment] += 1
                                    
                                else:
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    #print('y4')
                                    if(reservoir_b[segment][i][j].qsize()==reservoir_length):
                                        reservoir_b[segment][i][j].get()
                                        leakage_b[segment][i][j] += 1

                                    reservoir_b[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                                    lifetime_cells[segment][i][j]=0
                                    detachment_b[segment][i][j] += 1
                                    detach_b[segment] += 1
                            
                        elif(j >= ((cols_count-(stagger2/100)*cols_count)-vel_b)):
                            if(i == 1):
                                if((j + vel_b) >= cols_count-1):
                                    throughput_b[segment] += 1
                                    output_b[segment][i][time] += 1
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    flag = 1
                                    input_res[segment+1].put(2)
                                else:
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    #print('y4')
                                    if(reservoir_b[segment][i][j].qsize()==reservoir_length):
                                        reservoir_b[segment][i][j].get()
                                        leakage_b[segment][i][j] += 1

                                    reservoir_b[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                                    lifetime_cells[segment][i][j]=0
                                    detachment_b[segment][i][j] += 1
                                    detach_b[segment] += 1
                            
                            else:
                                if(particle[segment][1][j+vel_b]== 0):
                                    particle[segment][1][j+vel_b] = 2
                                    span[segment][1][j+vel_b] = span[segment][i][j] + vel_b
                                    velocity[segment][1][j+vel_b] = vel_b 
                                    lifetime_cells[segment][1][j+vel_b] = lifetime_cells[segment][i][j]
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    lifetime_cells[segment][i][j] = 0
                                    lateral_b[segment] += 1

                                else:
                                    particle[segment][i][j] = 0
                                    span[segment][i][j] = 0
                                    velocity[segment][i][j] = 0
                                    #print('y4')
                                    if(reservoir_b[segment][i][j].qsize()==reservoir_length):
                                        reservoir_b[segment][i][j].get()
                                        leakage_b[segment][i][j] += 1

                                    reservoir_b[segment][i][j].put(props(time,lifetime_cells[segment][i][j]))

                                    lifetime_cells[segment][i][j]=0
                                    detachment_b[segment][i][j] += 1
                                    detach_b[segment] += 1
                                
                
                gap = 0
    
    if(flag == 0):
        input_res[segment+1].put(0)
        
    end = timer()
    #print("Transport 7 take", end - start)            
    #pdb.set_trace()
    #print(9)
    
    return input_res, throughput_a, throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b, detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, output_a, output_b


# ### Output / Main Function

# In[43]:


# column = "Site,Waiting_A_Track_1,Waiting_B_Track_1,Waiting_A_Track_2,Waiting_B_Track_2,Waiting_A_Track_3,Waiting_B_Track_3,Leakage_A_Track_1,Leakage_B_Track_1,Leakage_A_Track_2,Leakage_B_Track_2,Leakage_A_Track_3,Leakage_B_Track_3\n"

# dir_1 = "Scenario 147 Segment 1 Productive and Non-Productive.csv"
# csv1 = open(dir_1, "a", newline='') 
# writer1 = csv.writer(csv1, dialect='excel')
# csv1.write(column)

# dir_4 = "Scenario 147 Segment 2 Productive and Non-Productive.csv"
# csv4 = open(dir_4, "a", newline='') 
# writer4 = csv.writer(csv4, dialect='excel')
# csv4.write(column)

# dir_7 = "Scenario 147 Segment 3 Productive and Non-Productive.csv"
# csv7 = open(dir_7, "a", newline='') 
# writer7 = csv.writer(csv7, dialect='excel')
# csv7.write(column)


print("Here we modelled a multisegment with " + str(scenario)+ " scenario formation")


# workbook = xlsxwriter.Workbook('Time Metric ' + str(scenario)+ ' Outputs '+ str(association_rate/2) + '1.xlsx')
# worksheet9 = workbook.add_worksheet()
# worksheet9.write(0, 0, "Iteration")
# worksheet9.write(0, 1, "Segment 1A")
# worksheet9.write(0, 2, "Segment 1B")
# worksheet9.write(0, 3, "Segment 2A")
# worksheet9.write(0, 4, "Segment 2B")
# worksheet9.write(0, 5, "Segment 3A")
# worksheet9.write(0, 6, "Segment 3B")

temp1a = 0
temp1b = 0
temp2a = 0
temp2b = 0
temp3a = 0
temp3b = 0

tmp1a = 0
tmp1b = 0
tmp2a = 0
tmp2b = 0
tmp3a = 0
tmp3b = 0
count = 0

lines = [' ', 'Multisegment' + str(scenario) + 'at' + str(association_rate/2) + 'motors_sec']

with open(script_dir + '/'+ str(scenario) + '_at_' + str(association_rate/2) + '_motors_sec.txt', 'w') as f:
    f.write('\n'.join(lines))

lines = [' ', 'Multisegment' + str(scenario) + 'at' + str(association_rate/2) + 'motors_sec']

with open(script_dir + '/'+ str(scenario) + '_at_' + str(association_rate/2) + '_motors_sec(per_sec).txt', 'w') as f:
    f.write('\n'.join(lines))
    
for iter in range(total_runtime2):
    
    start = timer()
    for segment in range(segments):
        if(segment == 0):

            reservoir_a, reservoir_b, reattachment_a, reattachment_b, reattach_a, reattach_b, leakage_a, leakage_b                     = lateral_association1(rows_count, cols_count,reservoir_a, reservoir_b, reattachment_a, reattachment_b,                                            reattach_a, reattach_b, leakage_a, leakage_b, segment, iter)

            input_res, throughput_a, throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b,             detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, output_a, output_b                    = transport1(input_res, rows_count, cols_count, vel_a, vel_b, process_a, process_b, throughput_a,                                           throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b,                                          detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, segment, output_a, output_b, iter)

            input_res, motor_cargo_a, motor_cargo_b = initial_association1(input_res, motor_cargo_a, motor_cargo_b, segment)
    
        elif(segment == 2):
        
            reservoir_a, reservoir_b, reattachment_a, reattachment_b, reattach_a, reattach_b, leakage_a, leakage_b                     = lateral_association4(rows_count, cols_count,reservoir_a, reservoir_b, reattachment_a, reattachment_b,                                            reattach_a, reattach_b, leakage_a, leakage_b, segment, iter)

            input_res, throughput_a, throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b,             detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, output_a, output_b                    = transport4(input_res, rows_count, cols_count, vel_a, vel_b, process_a, process_b, throughput_a,                                           throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b,                                          detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, segment, output_a, output_b, iter)

            input_res, motor_cargo_a, motor_cargo_b = initial_association4(input_res, motor_cargo_a, motor_cargo_b, segment)
        
        elif(segment == 1):

            reservoir_a, reservoir_b, reattachment_a, reattachment_b, reattach_a, reattach_b, leakage_a, leakage_b                     = lateral_association7(rows_count, cols_count,reservoir_a, reservoir_b, reattachment_a, reattachment_b,                                            reattach_a, reattach_b, leakage_a, leakage_b, segment, iter)

            input_res, throughput_a, throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b,             detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, output_a, output_b                  = transport7(input_res, rows_count, cols_count, vel_a, vel_b, process_a, process_b, throughput_a,                                           throughput_b, reservoir_a, reservoir_b, detachment_a, detachment_b, detach_a, detach_b,                                          detach_process_a, detach_process_b, leakage_a, leakage_b, lateral_a, lateral_b, segment, output_a, output_b, iter)

            input_res, motor_cargo_a, motor_cargo_b = initial_association7(input_res, motor_cargo_a, motor_cargo_b, segment)
    
    
    reservoir_a, reservoir_b = empty_queues(rows_count, cols_count, reservoir_a, reservoir_b, leakage_a, leakage_b, iter)
    
    
    
    
    waiting_a = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]  
    waiting_b = [[[0 for j in range(cols_count)] for i in range(rows_count)] for l in range(segments)]  
    wait_a = [0 for l in range(segments)]
    wait_b = [0 for l in range(segments)]
    leak_a = [0 for l in range(segments)]
    leak_b = [0 for l in range(segments)]
    
    for l in range(segments):
        for i in range(rows_count):
            for j in range(cols_count):
                waiting_a[l][i][j] = reservoir_a[l][i][j].qsize()
                waiting_b[l][i][j] = reservoir_b[l][i][j].qsize()
                productive_a[l][i][j] += waiting_a[l][i][j]
                productive_b[l][i][j] += waiting_b[l][i][j]
                non_productive_a[l][i][j] += leakage_a[l][i][j]
                non_productive_b[l][i][j] += leakage_b[l][i][j]
                reservoir_a_graph[l][i][j] += waiting_a[l][i][j]
                reservoir_b_graph[l][i][j] += waiting_b[l][i][j]
                wait_a[l] += waiting_a[l][i][j]
                wait_b[l] += waiting_b[l][i][j]
                leak_a[l] += leakage_a[l][i][j]
                leak_b[l] += leakage_b[l][i][j]
    
    for l in range(segments):
        for i in range(rows_count):
            for j in range(cols_count):
                temp = int(j/10)
                temp1 = int(j/5)
                if(particle[l][i][j] == 1):
                    heat_map_a[l][i][j] += particle[l][i][j]
                    heat_map_a_2[l][i][temp] += particle[l][i][j]
                    heat_map_a_3[l][i][temp1] += particle[l][i][j]
                elif(particle[l][i][j] == 2):
                    heat_map_b[l][i][j] += particle[l][i][j]
                    heat_map_b_2[l][i][temp] += particle[l][i][j]
                    heat_map_b_3[l][i][temp1] += particle[l][i][j]

    #print("Done")
    #column9 = "Site, Waiting A Track 1, Waiting B Track 1, Waiting A Track 2, Waiting B Track 2, Leakage A Track 1, Leakage B Track 1, Leakage A Track 2, Leakage B Track 2"
    
    d_a = [[0 for j in range(cols_count)] for l in range(segments)]
    d_b = [[0 for j in range(cols_count)] for l in range(segments)]
    r_a = [[0 for j in range(cols_count)] for l in range(segments)]
    r_b = [[0 for j in range(cols_count)] for l in range(segments)]
    w_a = [[0 for j in range(cols_count)] for l in range(segments)]
    w_b = [[0 for j in range(cols_count)] for l in range(segments)]
    l_a = [[0 for j in range(cols_count)] for l in range(segments)]
    l_b = [[0 for j in range(cols_count)] for l in range(segments)]
    
    for l in range(segments):
        for j in range(cols_count):
            for i in range(rows_count):
                d_a[l][j] += detachment_a[l][i][j]
                d_b[l][j] += detachment_b[l][i][j]
                r_a[l][j] += reattachment_a[l][i][j]
                r_b[l][j] += reattachment_b[l][i][j]
                w_a[l][j] += reservoir_a[l][i][j].qsize()
                w_b[l][j] += reservoir_b[l][i][j].qsize()
                l_a[l][j] += leakage_a[l][i][j]
                l_b[l][j] += leakage_b[l][i][j]

    
    end = timer()
    if(iter%100==0):
        print("\n Run: "+ str(iter+1), (end - start))
    
    
    t = str(iter+1).zfill(5)
    time=(iter+1)*time_stamp
    
    ####################################################################################################        
    
    # if(iter!=0 and iter < 10000):
    #     worksheet9.write(iter+1, 0, str(((iter+1)*0.04)))
    #     worksheet9.write(iter+1, 1, throughput_a[0]-temp1a)
    #     worksheet9.write(iter+1, 2, throughput_b[0]-temp1b)
    #     worksheet9.write(iter+1, 3, throughput_a[1]-temp2a)
    #     worksheet9.write(iter+1, 4, throughput_b[1]-temp2b)
    #     worksheet9.write(iter+1, 5, throughput_a[2]-temp3a)
    #     worksheet9.write(iter+1, 6, throughput_b[2]-temp3b)
    #     if(iter == 9999):
    #         print("Done")

    # output_a[0] = throughput_a[0]
    # output_b[0] = throughput_b[0]
    # output_a[1] = throughput_a[1]
    # output_b[1] = throughput_b[1]
    # output_a[2] = throughput_a[2]
    # output_b[2] = throughput_b[2]
    
    if(iter==0):
        continue
    
    temp1a = output_a[0][0][iter] + output_a[0][1][iter] + output_a[0][2][iter] 
    temp1b = output_b[0][0][iter] + output_b[0][1][iter] + output_b[0][2][iter] 
    temp2a = output_a[1][0][iter] + output_a[1][1][iter] + output_a[1][2][iter] 
    temp2b = output_b[1][0][iter] + output_b[1][1][iter] + output_b[1][2][iter] 
    temp3a = output_a[2][0][iter] + output_a[2][1][iter] + output_a[2][2][iter] 
    temp3b = output_b[2][0][iter] + output_b[2][1][iter] + output_b[2][2][iter] 
    
    
    line1 = [' ','Timestep:' + str((iter+1)*40) + 'msecs']
    line2 = [' ','Motor a: Seg 1:' + str(temp1a) + ', Seg 2:' + str(temp2a) + ', Seg 3:' + str(temp3a)]
    line3 = [' ','Motor b: Seg 1:' + str(temp1b) + ', Seg 2:' + str(temp2b) + ', Seg 3:' + str(temp3b)]
    line4 = [' ','Throughput a: Seg 1:' + str(throughput_a[0]) + ', Seg 2:' + str(throughput_a[1]) + ', Seg 3:' + str(throughput_a[2])]
    line5 = [' ','Throughput b: Seg 1:' + str(throughput_b[0]) + ', Seg 2:' + str(throughput_b[1]) + ', Seg 3:' + str(throughput_b[2])]

    with open(script_dir + '/'+ str(scenario) + '_at_' + str(association_rate/2) + '_motors_sec.txt', 'a') as f:
        f.write('\n'.join(line1))
        f.write('\n'.join(line2))
        f.write('\n'.join(line3))
        f.write('\n'.join(line4))
        f.write('\n'.join(line5))
    
    
    if(count!=25):
        tmp1a += temp1a
        tmp1b += temp1b
        tmp2a += temp2a
        tmp2b += temp2b
        tmp3a += temp3a
        tmp3b += temp3b
        count += 1
        
    if(iter%25 == 0):
        
        line1 = [' ','Timestep:' + str(int(iter/25)) + 'sec']
        line2 = [' ','Motor a: Seg 1:' + str(tmp1a) + ', Seg 2:' + str(tmp2a) + ', Seg 3:' + str(tmp3a)]
        line3 = [' ','Motor b: Seg 1:' + str(tmp1b) + ', Seg 2:' + str(tmp2b) + ', Seg 3:' + str(tmp3b)]
        line4 = [' ','Throughput a: Seg 1:' + str(throughput_a[0]) + ', Seg 2:' + str(throughput_a[1]) + ', Seg 3:' + str(throughput_a[2])]
        line5 = [' ','Throughput b: Seg 1:' + str(throughput_b[0]) + ', Seg 2:' + str(throughput_b[1]) + ', Seg 3:' + str(throughput_b[2])]

        
        tmp1a = 0
        tmp1b = 0
        tmp2a = 0
        tmp2b = 0
        tmp3a = 0
        tmp3b = 0
        count = 0
        
        with open(script_dir + '/'+ str(scenario) + '_at_' + str(association_rate/2) + '_motors_sec(per_sec).txt', 'a') as f:
            f.write('\n'.join(line1))
            f.write('\n'.join(line2))
            f.write('\n'.join(line3))
            f.write('\n'.join(line4))
            f.write('\n'.join(line5))

# workbook.close()

output_a_sec = [[[0 for j in range(int(total_runtime*0.04))] for i in range(rows_count)] for l in range(segments)] 
output_b_sec = [[[0 for j in range(int(total_runtime*0.04))] for i in range(rows_count)] for l in range(segments)]

for l in range(segments):
    for i in range (rows_count):
        for t in range(total_runtime-2):
            output_a_sec[l][i][int(t/25)] += output_a[l][i][t]
            output_b_sec[l][i][int(t/25)] += output_b[l][i][t]

# In[ ]:


time=(total_runtime)*time_stamp
plt.figure(3)

fig, (ax0, ax1, ax2) = plt.subplots(ncols=3, nrows = 1, figsize=(20,3), 
                    gridspec_kw={"width_ratios":[1,1,1]})

ax0.plot(cols1, d_a[0], alpha=0.6, color="Blue", label="Kin3 (F)")
ax0.plot(cols1, d_b[0], alpha=0.5, color="Red", label="Kin1 (S)")
ax0.set_ylim(bottom=0)
ax0.set_xlabel('Corresponding Lattice Site', fontsize=13)
ax0.set_ylabel("\n".join(wrap('No of motors', 22)), fontsize=13)
ax0.set_title("\n".join(wrap('Number of motors in Segment 1', 70)), fontsize=14)
ax0.legend(loc="upper right")

ax1.plot(cols1, d_a[1], alpha=0.6, color="Blue", label="Kin3 (F)")
ax1.plot(cols1, d_b[1], alpha=0.5, color="Red", label="Kin1 (S)")
ax1.set_ylim(bottom=0)
ax1.set_xlabel('Corresponding Lattice Site', fontsize=13)
ax1.set_ylabel("\n".join(wrap('No of motors', 22)), fontsize=13)
ax1.set_title("\n".join(wrap('Number of motors in Segment 2', 70)), fontsize=14)
ax1.legend(loc="upper right")

ax2.plot(cols1, d_a[2], alpha=0.6, color="Blue", label="Kin3 (F)")
ax2.plot(cols1, d_b[2], alpha=0.5, color="Red", label="Kin1 (S)")
ax2.set_ylim(bottom=0)
ax2.set_xlabel('Corresponding Lattice Site', fontsize=13)
ax2.set_ylabel("\n".join(wrap('No of motors', 22)), fontsize=13)
ax2.set_title("\n".join(wrap('Number of motors in Segment 3', 70)), fontsize=14)
ax2.legend(loc="upper right")


fig.suptitle("\n".join(wrap('Productive Reservoir in Multi-MMLS (Scenario ' + str(scenario) + ') - FULL BLOCK and RELEASE', 180)), fontsize=18)
fig.tight_layout()
plt.subplots_adjust(top=0.75, hspace = 0.95)
plt.gcf()
plt.savefig('Outputs/'+ str(association_rate/2) +' ' +  str(scenario)+' Productive_AB(together).png',  dpi=300, bbox_inches = 'tight')
plt.show()
plt.close()
print("Graph 3 Done")

####################################################################################################        


plt.figure(4)
fig, ((ax0, ax1, ax2), (ax3, ax4, ax5)) = plt.subplots(ncols=3, nrows = 2, figsize=(20,5), 
                    gridspec_kw={"height_ratios":[1,1], "width_ratios":[1,1,1]})

ax0.plot(cols1, d_a[0], color="Blue", label="Kin3 (F)")
ax0.set_ylim(bottom=0)
ax0.set_xlabel('Corresponding Lattice Site', fontsize=13)
ax0.set_ylabel("\n".join(wrap('No of motors', 22)), fontsize=13)
ax0.set_title("\n".join(wrap('Number of Kin3 (F) motors in Segment 1', 70)), fontsize=14)
ax0.legend(loc="upper right")

ax1.plot(cols1, d_a[1], color="Blue", label="Kin3 (F)")
ax1.set_ylim(bottom=0)
ax1.set_xlabel('Corresponding Lattice Site', fontsize=13)
ax1.set_ylabel("\n".join(wrap('No of motors', 22)), fontsize=13)
ax1.set_title("\n".join(wrap('Number of Kin3 (F) motors in Segment 2', 70)), fontsize=14)
ax1.legend(loc="upper right")

ax2.plot(cols1, d_a[2], color="Blue", label="Kin3 (F)")
ax2.set_ylim(bottom=0)
ax2.set_xlabel('Corresponding Lattice Site', fontsize=13)
ax2.set_ylabel("\n".join(wrap('No of motors', 22)), fontsize=13)
ax2.set_title("\n".join(wrap('Number of Kin3 (F) motors in Segment 3', 70)), fontsize=14)
ax2.legend(loc="upper right")

ax3.plot(cols1, d_b[0], color="Red", label="Kin1 (S)")
ax3.set_ylim(bottom=0)
ax3.set_xlabel('Corresponding Lattice Site', fontsize=13)
ax3.set_ylabel("\n".join(wrap('No of motors', 22)), fontsize=13)
ax3.set_title("\n".join(wrap('Number of Kin1 (S) motors in Segment 1', 70)), fontsize=14)
ax3.legend(loc="upper right")

ax4.plot(cols1, d_b[1], color="Red", label="Kin1 (S)")
ax4.set_ylim(bottom=0)
ax4.set_xlabel('Corresponding Lattice Site', fontsize=13)
ax4.set_ylabel("\n".join(wrap('No of motors', 22)), fontsize=13)
ax4.set_title("\n".join(wrap('Number of Kin1 (S) motors in Segment 2', 70)), fontsize=14)
ax4.legend(loc="upper right")

ax5.plot(cols1, d_b[2], color="Red", label="Kin1 (S)")
ax5.set_ylim(bottom=0)
ax5.set_xlabel('Corresponding Lattice Site', fontsize=13)
ax5.set_ylabel("\n".join(wrap('No of motors', 22)), fontsize=13)
ax5.set_title("\n".join(wrap('Number of Kin1 (S) motors in Segment 3', 70)), fontsize=14)
ax5.legend(loc="upper right")


fig.suptitle("\n".join(wrap('Productive Reservoir in Multi-MMLS (Scenario ' + str(scenario) + ') - FULL BLOCK and RELEASE', 180)), fontsize=18)
fig.tight_layout()
plt.subplots_adjust(top=0.88, hspace = 0.95)
plt.gcf()
plt.savefig('Outputs/'+ str(association_rate/2) + ' ' + str(scenario) +' Productive_AB(seperate).png',  dpi=300, bbox_inches = 'tight')
plt.show()
plt.close()
print("Graph 4 Done")


##################################################################
plt.figure(10)
xlabel='$TIme \ (secs)$'; ylabel='$No\ of\ motors$'

Nlayer = 3
Ncols = 3

topmax = max(max(max(max(output_a))),max(max(max(output_b))))
fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8)) = plt.subplots(Nlayer, Ncols, figsize=(20,3),
                                                        sharex='col', gridspec_kw={'hspace': 0, 'wspace': 0, "height_ratios":[1,1,1], "width_ratios":[1,1,1]})

time_axis = np.linspace(0, total_runtime, total_runtime)
# ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(time_axis/25))

ax0.scatter(time_axis-0.25, output_a[0][2], color="Blue")
ax0.scatter(time_axis+0.25, output_b[0][2], color="Red")
# ax0.set_yticks([])
ax0.set_ylim(bottom=0, top = topmax)
ax1.scatter(time_axis-0.25, output_a[1][2], color="Blue")
ax1.scatter(time_axis+0.25, output_b[1][2], color="Red")
ax1.set_yticks([])
ax1.set_ylim(bottom=0, top = topmax)
ax2.scatter(time_axis-0.25, output_a[2][2], color="Blue")
ax2.scatter(time_axis+0.25, output_b[2][2], color="Red")
ax2.set_yticks([])
ax2.set_ylim(bottom=0, top = topmax)
# ax2.xaxis.set_major_formatter(ticks_x)
a=ax2.get_xticks().tolist()
for i in range(len(a)):
    a[i] = a[i] * 0.04


ax3.scatter(time_axis-0.25, output_a[0][1], color="Blue")
ax3.scatter(time_axis+0.25, output_b[0][1], color="Red")
# ax3.set_yticks([])
ax3.set_ylim(bottom=0, top = topmax)
ax4.scatter(time_axis-0.25, output_a[1][1], color="Blue", label = "Kin3 (F)")
ax4.scatter(time_axis+0.25, output_b[1][1], color="Red", label = "Kin1 (S)")
ax4.set_yticks([])
ax4.set_ylim(bottom=0, top = topmax)
ax4.legend(loc = "upper right")
ax5.scatter(time_axis-0.25, output_a[2][1], color="Blue")
ax5.scatter(time_axis+0.25, output_b[2][1], color="Red")
ax5.set_yticks([])
ax5.set_ylim(bottom=0, top = topmax)
# ax5.xaxis.set_major_formatter(ticks_x)


ax6.scatter(time_axis-0.25, output_a[0][0], color="Blue")
ax6.scatter(time_axis+0.25, output_b[0][0], color="Red")
# ax6.set_yticks([])
ax6.set_ylim(bottom=0, top = topmax)
ax7.scatter(time_axis-0.25, output_a[1][0], color="Blue")
ax7.scatter(time_axis+0.25, output_b[1][0], color="Red")
ax7.set_yticks([])
ax7.set_ylim(bottom=0, top = topmax)
ax8.scatter(time_axis-0.25, output_a[2][0], color="Blue")
ax8.scatter(time_axis+0.25, output_b[2][0], color="Red")
ax8.set_yticks([])
ax8.set_ylim(bottom=0, top = topmax)
# ax8.xaxis.set_major_formatter(ticks_x)
ax6.set_xticklabels(a)
ax7.set_xticklabels(a)
ax8.set_xticklabels(a)

fig.text(0.5, 0.01, xlabel, va='center')
fig.text(0.1, 0.5, ylabel, va='center', rotation='vertical')
fig.suptitle("\n".join(wrap('Output (per 40 msecs) of Kin3 (F) and Kin1 (S) (Scenario ' + str(scenario) + ') for association rate ' + str(association_rate/2) + ' motors/sec - FULL BLOCK and RELEASE', 140)), fontsize=14, y=1.1)
plt.draw()
plt.subplots_adjust(top=0.95, hspace = 0.85)
plt.gcf()
plt.savefig('Outputs/'+ str(association_rate/2) + ' Full Scenario ' + str(scenario)+ 'Output (Scatter).png', format='png', dpi=600, bbox_inches = 'tight')
plt.show()
plt.close()
print("Graph 5 Done")

##################################################################
plt.figure(10)
xlabel='$TIme \ (secs)$'; ylabel='$No\ of\ motors$'

Nlayer = 3
Ncols = 3

topmax = max(max(max(max(output_a))),max(max(max(output_b))))
fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8)) = plt.subplots(Nlayer, Ncols, figsize=(20,3),
                                                        sharex='col', gridspec_kw={'hspace': 0, 'wspace': 0, "height_ratios":[1,1,1], "width_ratios":[1,1,1]})

time_axis = np.linspace(0, total_runtime, total_runtime)
# ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(time_axis/25))

ax0.plot(time_axis-0.25, output_a[0][2], color="Blue")
ax0.plot(time_axis+0.25, output_b[0][2], color="Red")
# ax0.set_yticks([])
ax0.set_ylim(bottom=0, top = topmax)
ax1.plot(time_axis-0.25, output_a[1][2], color="Blue")
ax1.plot(time_axis+0.25, output_b[1][2], color="Red")
ax1.set_yticks([])
ax1.set_ylim(bottom=0, top = topmax)
ax2.plot(time_axis-0.25, output_a[2][2], color="Blue")
ax2.plot(time_axis+0.25, output_b[2][2], color="Red")
ax2.set_yticks([])
ax2.set_ylim(bottom=0, top = topmax)
# ax2.xaxis.set_major_formatter(ticks_x)
a=ax2.get_xticks().tolist()
for i in range(len(a)):
    a[i] = a[i] * 0.04


ax3.plot(time_axis-0.25, output_a[0][1], color="Blue")
ax3.plot(time_axis+0.25, output_b[0][1], color="Red")
# ax3.set_yticks([])
ax3.set_ylim(bottom=0, top = topmax)
ax4.plot(time_axis-0.25, output_a[1][1], color="Blue", label = "Kin3 (F)")
ax4.plot(time_axis+0.25, output_b[1][1], color="Red", label = "Kin1 (S)")
ax4.set_yticks([])
ax4.set_ylim(bottom=0, top = topmax)
ax4.legend(loc = "upper right")
ax5.plot(time_axis-0.25, output_a[2][1], color="Blue")
ax5.plot(time_axis+0.25, output_b[2][1], color="Red")
ax5.set_yticks([])
ax5.set_ylim(bottom=0, top = topmax)
# ax5.xaxis.set_major_formatter(ticks_x)


ax6.plot(time_axis-0.25, output_a[0][0], color="Blue")
ax6.plot(time_axis+0.25, output_b[0][0], color="Red")
# ax6.set_yticks([])
ax6.set_ylim(bottom=0, top = topmax)
ax7.plot(time_axis-0.25, output_a[1][0], color="Blue")
ax7.plot(time_axis+0.25, output_b[1][0], color="Red")
ax7.set_yticks([])
ax7.set_ylim(bottom=0, top = topmax)
ax8.plot(time_axis-0.25, output_a[2][0], color="Blue")
ax8.plot(time_axis+0.25, output_b[2][0], color="Red")
ax8.set_yticks([])
ax8.set_ylim(bottom=0, top = topmax)
# ax8.xaxis.set_major_formatter(ticks_x)
ax6.set_xticklabels(a)
ax7.set_xticklabels(a)
ax8.set_xticklabels(a)

fig.text(0.5, 0.01, xlabel, va='center')
fig.text(0.1, 0.5, ylabel, va='center', rotation='vertical')
fig.suptitle("\n".join(wrap('Output (per 40 msecs) of Kin3 (F) and Kin1 (S) (Scenario ' + str(scenario) + ') for association rate ' + str(association_rate/2) + ' motors/sec - FULL BLOCK and RELEASE', 140)), fontsize=14, y=1.1)
plt.draw()
plt.subplots_adjust(top=0.95, hspace = 0.85)
plt.gcf()
plt.savefig('Outputs/'+ str(association_rate/2) + ' Full Scenario ' + str(scenario)+ 'Output (Plot).png', format='png', dpi=600, bbox_inches = 'tight')
plt.show()
plt.close()
print("Graph 5 Done")

##################################################################

plt.figure(11)
xlabel='$TIme \ (secs)$'; ylabel='$No\ of\ motors$'

Nlayer = 3
Ncols = 3

topmax = max(max(max(max(output_a_sec))),max(max(max(output_b_sec))))
fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8)) = plt.subplots(Nlayer, Ncols, figsize=(20,3),
                                                        sharex='col', gridspec_kw={'hspace': 0, 'wspace': 0, "height_ratios":[1,1,1], "width_ratios":[1,1,1]})

time_axis = np.arange(0, total_runtime*0.04-1)
# ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(time_axis/25))

ax0.scatter(time_axis-0.05, output_a_sec[0][2], color="Blue")
ax0.scatter(time_axis+0.05, output_b_sec[0][2], color="Red")
# ax0.set_yticks([])
ax0.set_ylim(bottom=0, top = topmax)
ax1.scatter(time_axis-0.05, output_a_sec[1][2], color="Blue")
ax1.scatter(time_axis+0.05, output_b_sec[1][2], color="Red")
ax1.set_yticks([])
ax1.set_ylim(bottom=0, top = topmax)
ax2.scatter(time_axis-0.05, output_a_sec[2][2], color="Blue")
ax2.scatter(time_axis+0.05, output_b_sec[2][2], color="Red")
ax2.set_yticks([])
ax2.set_ylim(bottom=0, top = topmax)
# ax2.xaxis.set_major_formatter(ticks_x)
a=ax2.get_xticks().tolist()


ax3.scatter(time_axis-0.05, output_a_sec[0][1], color="Blue")
ax3.scatter(time_axis+0.05, output_b_sec[0][1], color="Red")
# ax3.set_yticks([])
ax3.set_ylim(bottom=0, top = topmax)
ax4.scatter(time_axis-0.05, output_a_sec[1][1], color="Blue", label = "Kin3 (F)")
ax4.scatter(time_axis+0.05, output_b_sec[1][1], color="Red", label = "Kin1 (S)")
ax4.set_yticks([])
ax4.set_ylim(bottom=0, top = topmax)
ax4.legend(loc = "upper right")
ax5.scatter(time_axis-0.05, output_a_sec[2][1], color="Blue")
ax5.scatter(time_axis+0.05, output_b_sec[2][1], color="Red")
ax5.set_yticks([])
ax5.set_ylim(bottom=0, top = topmax)
# ax5.xaxis.set_major_formatter(ticks_x)


ax6.scatter(time_axis-0.05, output_a_sec[0][0], color="Blue")
ax6.scatter(time_axis+0.05, output_b_sec[0][0], color="Red")
# ax6.set_yticks([])
ax6.set_ylim(bottom=0, top = topmax)
ax7.scatter(time_axis-0.05, output_a_sec[1][0], color="Blue")
ax7.scatter(time_axis+0.05, output_b_sec[1][0], color="Red")
ax7.set_yticks([])
ax7.set_ylim(bottom=0, top = topmax)
ax8.scatter(time_axis-0.05, output_a_sec[2][0], color="Blue")
ax8.scatter(time_axis+0.05, output_b_sec[2][0], color="Red")
ax8.set_yticks([])
ax8.set_ylim(bottom=0, top = topmax)
# ax8.xaxis.set_major_formatter(ticks_x)
ax6.set_xticklabels(a)
ax7.set_xticklabels(a)
ax8.set_xticklabels(a)

fig.text(0.5, 0.01, xlabel, va='center')
fig.text(0.1, 0.5, ylabel, va='center', rotation='vertical')
fig.suptitle("\n".join(wrap('Output (per second) of Kin3 (F) and Kin1 (S) (Scenario ' + str(scenario) + ') for association rate ' + str(association_rate/2) + ' motors/sec - FULL BLOCK and RELEASE', 140)), fontsize=14, y=1.1)
plt.draw()
plt.subplots_adjust(top=0.95, hspace = 0.85)
plt.gcf()
plt.savefig('Outputs/'+ str(association_rate/2) + ' Full Scenario ' + str(scenario)+ 'Output (Scatter) persec.png', format='png', dpi=600, bbox_inches = 'tight')
plt.show()
plt.close()
print("Graph 6 Done")

##################################################################
plt.figure(11)
xlabel='$TIme \ (secs)$'; ylabel='$No\ of\ motors$'

Nlayer = 3
Ncols = 3

topmax = max(max(max(max(output_a_sec))),max(max(max(output_b_sec))))
fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8)) = plt.subplots(Nlayer, Ncols, figsize=(20,3),
                                                        sharex='col', gridspec_kw={'hspace': 0, 'wspace': 0, "height_ratios":[1,1,1], "width_ratios":[1,1,1]})

time_axis = np.arange(0, total_runtime*0.04-1)
# ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(time_axis/25))

ax0.plot(time_axis-0.05, output_a_sec[0][2], color="Blue")
ax0.plot(time_axis+0.05, output_b_sec[0][2], color="Red")
# ax0.set_yticks([])
ax0.set_ylim(bottom=0, top = topmax)
ax1.plot(time_axis-0.05, output_a_sec[1][2], color="Blue")
ax1.plot(time_axis+0.05, output_b_sec[1][2], color="Red")
ax1.set_yticks([])
ax1.set_ylim(bottom=0, top = topmax)
ax2.plot(time_axis-0.05, output_a_sec[2][2], color="Blue")
ax2.plot(time_axis+0.05, output_b_sec[2][2], color="Red")
ax2.set_yticks([])
ax2.set_ylim(bottom=0, top = topmax)
# ax2.xaxis.set_major_formatter(ticks_x)
a=ax2.get_xticks().tolist()


ax3.plot(time_axis-0.05, output_a_sec[0][1], color="Blue")
ax3.plot(time_axis+0.05, output_b_sec[0][1], color="Red")
# ax3.set_yticks([])
ax3.set_ylim(bottom=0, top = topmax)
ax4.plot(time_axis-0.05, output_a_sec[1][1], color="Blue", label = "Kin3 (F)")
ax4.plot(time_axis+0.05, output_b_sec[1][1], color="Red", label = "Kin1 (S)")
ax4.set_yticks([])
ax4.set_ylim(bottom=0, top = topmax)
ax4.legend(loc = "upper right")
ax5.plot(time_axis-0.05, output_a_sec[2][1], color="Blue")
ax5.plot(time_axis+0.05, output_b_sec[2][1], color="Red")
ax5.set_yticks([])
ax5.set_ylim(bottom=0, top = topmax)
# ax5.xaxis.set_major_formatter(ticks_x)


ax6.plot(time_axis-0.05, output_a_sec[0][0], color="Blue")
ax6.plot(time_axis+0.05, output_b_sec[0][0], color="Red")
# ax6.set_yticks([])
ax6.set_ylim(bottom=0, top = topmax)
ax7.plot(time_axis-0.05, output_a_sec[1][0], color="Blue")
ax7.plot(time_axis+0.05, output_b_sec[1][0], color="Red")
ax7.set_yticks([])
ax7.set_ylim(bottom=0, top = topmax)
ax8.plot(time_axis-0.05, output_a_sec[2][0], color="Blue")
ax8.plot(time_axis+0.05, output_b_sec[2][0], color="Red")
ax8.set_yticks([])
ax8.set_ylim(bottom=0, top = topmax)
# ax8.xaxis.set_major_formatter(ticks_x)
ax6.set_xticklabels(a)
ax7.set_xticklabels(a)
ax8.set_xticklabels(a)

fig.text(0.5, 0.01, xlabel, va='center')
fig.text(0.1, 0.5, ylabel, va='center', rotation='vertical')
fig.suptitle("\n".join(wrap('Output (per second) of Kin3 (F) and Kin1 (S) (Scenario ' + str(scenario) + ') for association rate ' + str(association_rate/2) + ' motors/sec - FULL BLOCK and RELEASE', 140)), fontsize=14, y=1.1)
plt.draw()
plt.subplots_adjust(top=0.95, hspace = 0.85)
plt.gcf()
plt.savefig('Outputs/'+ str(association_rate/2) + ' Full Scenario ' + str(scenario)+ 'Output (Plot) persec.png', format='png', dpi=600, bbox_inches = 'tight')
plt.show()
plt.close()
print("Graph 6 Done")
# In[ ]:


cmap_name = 'my_list'
colors = [(1, 1, 1), (0, 0, 1), (1, 0, 0)]  # White -> Blue -> Red
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=3) 

colors_red = [(1, 1, 1), (1, 0, 0)]  # White -> Red
c_red = LinearSegmentedColormap.from_list(cmap_name, colors_red, N=100) 

colors_blue = [(1, 1, 1), (0, 0, 1)]  # White -> Blue
c_blue = LinearSegmentedColormap.from_list(cmap_name, colors_blue, N=100)




# In[ ]:


fig5 = plt.figure(figsize=(20,5))
time=(total_runtime)*time_stamp
widths = [1, 1, 1, 0.05]
heights = [1, 1]
spec5 = fig5.add_gridspec(ncols=4, nrows=2, width_ratios=widths, height_ratios=heights)
for row in range(2):
    for col in range(4):
        ax = fig5.add_subplot(spec5[row, col])
        top1 = max(max(max(heat_map_a_3)))
        top2 = max(max(max(heat_map_b_3)))
        if(row==0 and col==0):
            c0 = ax.pcolor(heat_map_a_3[0], linewidths = 0.02, cmap=c_blue, vmin=0 , vmax=top1)
            ax.set_title("Segment 1: Kin3 (F)", fontsize=14)
            ax.set_xlabel('Sites', fontsize=12)
            ax.set_ylabel('Track', fontsize=12)
            plt.setp(ax, xticks=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200], 
                    xticklabels=['0','100','200','300','400','500','600','700','800','900','1000'],  
                    yticks=[0.5, 1.5, 2.5], yticklabels=['1', '2', '3'])


        elif(row==0 and col==1):
            c1 = ax.pcolor(heat_map_a_3[1], linewidths = 0.02, cmap=c_blue, vmin=0 , vmax=top1)
            ax.set_title("Segment 2: Kin3 (F)", fontsize=14)
            ax.set_xlabel('Sites', fontsize=12)
            #ax.set_ylabel('Track')
            plt.setp(ax, xticks=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200], 
                    xticklabels=['0','100','200','300','400','500','600','700','800','900','1000'],  
                    yticks=[0.5, 1.5, 2.5], yticklabels=['1', '2', '3'])

        elif(row==0 and col==2):
            c2 = ax.pcolor(heat_map_a_3[2], linewidths = 0.02, cmap=c_blue, vmin=0 , vmax=top1)
            ax.set_title("Segment 3: Kin3 (F)", fontsize=14)
            ax.set_xlabel('Sites', fontsize=12)
            #ax.set_ylabel('Track')
            plt.setp(ax, xticks=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200], 
                    xticklabels=['0','100','200','300','400','500','600','700','800','900','1000'],  
                    yticks=[0.5, 1.5, 2.5], yticklabels=['1', '2', '3'])

        elif(row==0 and col==3):
            fig5.colorbar(c0, cax=ax)
       
        elif(row==1 and col==0):
            c3 = ax.pcolor(heat_map_b_3[0], linewidths = 0.02, cmap=c_red, vmin=0 , vmax=top2)
            ax.set_title("Segment 1: Kin1 (S)", fontsize=14)
            ax.set_xlabel('Sites', fontsize=12)
            ax.set_ylabel('Track', fontsize=12)
            plt.setp(ax, xticks=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200], 
                    xticklabels=['0','100','200','300','400','500','600','700','800','900','1000'],  
                    yticks=[0.5, 1.5, 2.5], yticklabels=['1', '2', '3'])

        elif(row==1 and col==1):
            c4 = ax.pcolor(heat_map_b_3[1], linewidths = 0.02, cmap=c_red, vmin=0 , vmax=top2)
            ax.set_title("Segment 2: Kin1 (S)", fontsize=14)
            ax.set_xlabel('Sites', fontsize=12)
            #ax.set_ylabel('Track')
            plt.setp(ax, xticks=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200], 
                    xticklabels=['0','100','200','300','400','500','600','700','800','900','1000'],  
                    yticks=[0.5, 1.5, 2.5], yticklabels=['1', '2', '3'])

        elif(row==1 and col==2):
            c5 = ax.pcolor(heat_map_b_3[2], linewidths = 0.02, cmap=c_red, vmin=0 , vmax=top2)
            ax.set_title("Segment 3: Kin1 (S)", fontsize=14)
            ax.set_xlabel('Sites', fontsize=12)
            #ax.set_ylabel('Track')
            plt.setp(ax, xticks=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200], 
                    xticklabels=['0','100','200','300','400','500','600','700','800','900','1000'],  
                    yticks=[0.5, 1.5, 2.5], yticklabels=['1', '2', '3'])

        elif(row==1 and col==3):
            fig5.colorbar(c3, cax=ax)
        
        
fig5.suptitle("\n".join(wrap('Multi-MMLS (Scenario ' + str(scenario) + ') - FULL BLOCK and RELEASE', 100)), fontsize=14, y=1.1)
fig5.tight_layout()
plt.subplots_adjust(wspace = 0.3, hspace = 0.9)
plt.draw()
plt.savefig('Outputs/'+ str(association_rate/2) + ' Scenario ' + str(scenario)+ ' RB Heatmap.png', format='png', dpi=600, bbox_inches = 'tight')
plt.close()

print("Final Graph Done")


# In[ ]:



