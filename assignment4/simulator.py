#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 01:28:08 2019

@author: tanjeremy
"""

'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''
import sys
import queue

input_file = 'input.txt'

class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)

class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum ):
    n = 0
    maxArrival = 0
    totalBurst = 0
    schedule = []
    current_time = 0
    timeInQueue = 0
    
    for process in process_list:
        if n < process.id:
            n = process.id
        if maxArrival < process.arrive_time:
            maxArrival = process.arrive_time
        totalBurst = totalBurst + process.burst_time
    
    n = n + 1
#    print(n)
    
    rem_bt = [0] * n 
    wt = [0] * n 
    timeLastPreEmpt = [0] * n 
    
    runQ = queue.Queue()
    queue1 = queue.Queue()
    
    for process in process_list:
        queue1.put(process)
        
#    print(list(queue1.queue))
#    for elem in list(queue1.queue):
#        print(elem)
        
    queueItem = queue1.get()
    rem_bt[queueItem.id] = queueItem.burst_time
    
    runQ.put(queueItem)
#    print(rem_bt)
#    print(wt)
    firstItem = True
    
    while(runQ.empty()==False or queue1.empty()==False):
        if(firstItem):
            queueItem = runQ.get()
            firstItem=False
            schedule.append((current_time,queueItem.id))

#        print(checkItem.id)
#        print(checkItem.arrive_time)
#        print(checkItem.burst_time)

        current_time = current_time+1
        timeInQueue = timeInQueue+1
#        print("Running ID: " + str(queueItem.id))
#        print("current_time: " + str(current_time))
#        print("total bt: " + str(sum(rem_bt)))
        
        if(queue1.empty()==False):
            checkItem = queue1.queue[0]
            if(checkItem.arrive_time==current_time):
                nextItem = queue1.get()
                rem_bt[nextItem.id] = rem_bt[nextItem.id] + nextItem.burst_time
                timeLastPreEmpt[nextItem.id] = current_time
                runQ.put(nextItem)
#                if(runQ.qsize()>0 and (runQ.queue[0].arrive_time>nextItem.arrive_time or runQ.queue[0].arrive_time==-1)):
#                    tempQ = queue.Queue()
#                    tempQ.put(nextItem)
#                    for elem in list(runQ.queue):
#                        tempQ.put(elem)
#                    runQ=tempQ
#                else:
#                    runQ.put(nextItem)
#                
#                for elem in list(runQ.queue):
#                    print(elem)

#        for elem in list(runQ.queue):
#            print(elem)

        if(rem_bt[queueItem.id]-1>0):
#            print("here")
            rem_bt[queueItem.id] = rem_bt[queueItem.id]-1
        elif(rem_bt[queueItem.id]-1==0):
            rem_bt[queueItem.id] = 0
        
        if(rem_bt[queueItem.id]==0 and runQ.qsize()>0):
            queueItem = runQ.get()
            wt[queueItem.id] = wt[queueItem.id] + current_time-timeLastPreEmpt[queueItem.id]
            schedule.append((current_time,queueItem.id))
            timeInQueue=0
        elif(timeInQueue==time_quantum and rem_bt[queueItem.id]>0):
            timeLastPreEmpt[queueItem.id] = current_time
            runQ.put(Process(queueItem.id,-1,rem_bt[queueItem.id]))
            queueItem = runQ.get()
            wt[queueItem.id] = wt[queueItem.id] + current_time-timeLastPreEmpt[queueItem.id]
            schedule.append((current_time,queueItem.id))
            timeInQueue=0
            
#        if(current_time>10):
#            break
                
#        print(str(timeInQueue)+", "+str(time_quantum))
#        print(current_time)
#        print(rem_bt)
#        print(wt)
        
#        print("queue1 size " + str(queue1.qsize()))
#        print("runQ size " + str(runQ.qsize()))
#        break
            
    return (schedule, sum(wt)/len(process_list))

def SRTF_scheduling(process_list):
    n = 0
    maxArrival = 0
    totalBurst = 0
    schedule = []
    current_time = 0
#    timeInQueue = 0
    
    for process in process_list:
        if n < process.id:
            n = process.id
        if maxArrival < process.arrive_time:
            maxArrival = process.arrive_time
        totalBurst = totalBurst + process.burst_time
    
    n = n + 1
#    print(n)
    
    rem_bt = [0] * n 
    wt = [0] * n 
    timeLastPreEmpt = [0] * n 
    
    runQ = queue.PriorityQueue()
    queue1 = queue.Queue()
    
    for process in process_list:
        queue1.put(process)
        
#    print(list(queue1.queue))
#    for elem in list(queue1.queue):
#        print(elem)
        
    queueItem = queue1.get()
    rem_bt[queueItem.id] = queueItem.burst_time
    
    runQ.put((queueItem.burst_time,str(queueItem.id)))
#    print(rem_bt)
#    print(wt)
    firstItem = True
    
    while(runQ.empty()==False or queue1.empty()==False):
        if(firstItem):
            queueItem = runQ.get()
            queueItem = Process(int(queueItem[1]),-1,queueItem[0])
            firstItem=False
            schedule.append((current_time,queueItem.id))

#        print(checkItem.id)
#        print(checkItem.arrive_time)
#        print(checkItem.burst_time)

        current_time = current_time+1
#        timeInQueue = timeInQueue+1
#        print("Running ID: " + str(queueItem.id))
#        print("current_time: " + str(current_time))
#        print("total bt: " + str(sum(rem_bt)))

        if(rem_bt[queueItem.id]-1>0):
#            print("here")
            rem_bt[queueItem.id] = rem_bt[queueItem.id]-1
        elif(rem_bt[queueItem.id]-1==0):
            rem_bt[queueItem.id] = 0

        if(queue1.empty()==False):
            checkItem = queue1.queue[0]
            if(checkItem.arrive_time==current_time):
                nextItem = queue1.get()
                rem_bt[nextItem.id] = rem_bt[nextItem.id] + nextItem.burst_time
#                runQ.put((rem_bt[nextItem.id],str(nextItem.id)))
                
#                print("compare burst time" + str(rem_bt[nextItem.id]) + "," + str(rem_bt[queueItem.id]))
                if(rem_bt[queueItem.id] != 0 and rem_bt[nextItem.id]<rem_bt[queueItem.id]):
#                    print("take"+str(nextItem.id))
                    runQ.put((rem_bt[queueItem.id],str(queueItem.id)))
                    timeLastPreEmpt[queueItem.id] = current_time
                    queueItem = Process(nextItem.id,-1,rem_bt[nextItem.id])
                    schedule.append((current_time,nextItem.id))
                else:
                    runQ.put((rem_bt[nextItem.id],str(nextItem.id)))
                    timeLastPreEmpt[nextItem.id] = current_time
#                    print(timeLastPreEmpt)
#                if(runQ.qsize()>0 and (runQ.queue[0].arrive_time>nextItem.arrive_time or runQ.queue[0].arrive_time==-1)):
#                    tempQ = queue.Queue()
#                    tempQ.put(nextItem)
#                    for elem in list(runQ.queue):
#                        tempQ.put(elem)
#                    runQ=tempQ
#                else:
#                    runQ.put(nextItem)
                
#                for elem in list(runQ.queue):
#                    print(elem)

        if(rem_bt[queueItem.id]==0 and runQ.empty()==False):
#            for elem in list(runQ.queue):
#                print(elem)
            queueItem = runQ.get()
            queueItem = Process(int(queueItem[1]),-1,queueItem[0])
            wt[queueItem.id] = wt[queueItem.id] + current_time-timeLastPreEmpt[queueItem.id]
#            print("take"+str(queueItem.id))
#            print(str(current_time) + "," + str(queueItem.id))
            schedule.append((current_time,queueItem.id))

#        for elem in list(runQ.queue):
#            print(elem)

#        print(rem_bt)
            


            
#        if(current_time>10):
#            break
                
#        print(str(timeInQueue)+", "+str(time_quantum))
#        print(current_time)
#        print(rem_bt)

#        print(wt)
        
#        print("queue1 size " + str(queue1.qsize()))
#        print("runQ size " + str(runQ.qsize()))
#        break
            
    return (schedule, sum(wt)/len(process_list))

def predict_burst(a, t_n ,T_n):
    return a*t_n + (1 - a)* T_n

def SJF_scheduling(process_list, alpha):
    n = 0
    maxArrival = 0
    totalBurst = 0
    schedule = []
    current_time = 0
#    timeInQueue = 0
    
    for process in process_list:
        if n < process.id:
            n = process.id
        if maxArrival < process.arrive_time:
            maxArrival = process.arrive_time
        totalBurst = totalBurst + process.burst_time
    
    n = n + 1
#    print(n)
    
    rem_bt = [0] * n 
    wt = [0] * n 
    timeLastPreEmpt = [0] * n 
    tp_n = [5] * n 
    
    runQ = queue.PriorityQueue()
    queue1 = queue.Queue()
    
    for process in process_list:
        queue1.put(process)
        
#    print(list(queue1.queue))
#    for elem in list(queue1.queue):
#        print(elem)
        
    queueItem = queue1.get()
    rem_bt[queueItem.id] = queueItem.burst_time
    tp_n[queueItem.id] = queueItem.burst_time + predict_burst(alpha, rem_bt[queueItem.id] ,tp_n[queueItem.id])
    
    runQ.put((tp_n[queueItem.id],str(queueItem.id)))
#    print(rem_bt)
#    print(wt)
    
    print(tp_n)
    
    firstItem = True
    
    while(runQ.empty()==False or queue1.empty()==False):
        if(firstItem):
            queueItem = runQ.get()
            queueItem = Process(int(queueItem[1]),-1,queueItem[0])
            firstItem=False
            schedule.append((current_time,queueItem.id))

#        print(checkItem.id)
#        print(checkItem.arrive_time)
#        print(checkItem.burst_time)

        current_time = current_time+1
#        timeInQueue = timeInQueue+1
#        print("Running ID: " + str(queueItem.id))
#        print("current_time: " + str(current_time))
#        print("total bt: " + str(sum(rem_bt)))

        if(rem_bt[queueItem.id]-1>0):
#            print("here")
            rem_bt[queueItem.id] = rem_bt[queueItem.id]-1
        elif(rem_bt[queueItem.id]-1==0):
            rem_bt[queueItem.id] = 0

        if(queue1.empty()==False):
            checkItem = queue1.queue[0]
            if(checkItem.arrive_time==current_time):
                nextItem = queue1.get()
                rem_bt[nextItem.id] = rem_bt[nextItem.id] + nextItem.burst_time
                tp_n[nextItem.id] = nextItem.burst_time + predict_burst(alpha, rem_bt[nextItem.id] ,tp_n[nextItem.id])
            
                
#                runQ.put((rem_bt[nextItem.id],str(nextItem.id)))
                
#                print("compare burst time" + str(rem_bt[nextItem.id]) + "," + str(rem_bt[queueItem.id]))
#                if(rem_bt[queueItem.id] != 0 and rem_bt[nextItem.id]<rem_bt[queueItem.id]):
#                    print("take"+str(nextItem.id))
#                    runQ.put((rem_bt[queueItem.id],str(queueItem.id)))
#                    timeLastPreEmpt[queueItem.id] = current_time
#                    queueItem = Process(nextItem.id,-1,rem_bt[nextItem.id])
#                    schedule.append((current_time,nextItem.id))
#                else:
                runQ.put((tp_n[nextItem.id],str(nextItem.id)))
                timeLastPreEmpt[nextItem.id] = current_time
#                    print(timeLastPreEmpt)
#                if(runQ.qsize()>0 and (runQ.queue[0].arrive_time>nextItem.arrive_time or runQ.queue[0].arrive_time==-1)):
#                    tempQ = queue.Queue()
#                    tempQ.put(nextItem)
#                    for elem in list(runQ.queue):
#                        tempQ.put(elem)
#                    runQ=tempQ
#                else:
#                    runQ.put(nextItem)
                
                for elem in list(runQ.queue):
                    print(elem)
                print('--')

        if(rem_bt[queueItem.id]==0 and runQ.empty()==False):
#            for elem in list(runQ.queue):
#                print(elem)
            queueItem = runQ.get()
            queueItem = Process(int(queueItem[1]),-1,queueItem[0])
            wt[queueItem.id] = wt[queueItem.id] + current_time-timeLastPreEmpt[queueItem.id]
#            print("take"+str(queueItem.id))
#            print(str(current_time) + "," + str(queueItem.id))
            schedule.append((current_time,queueItem.id))

#        for elem in list(runQ.queue):
#            print(elem)

#        print(rem_bt)
            
        print(tp_n)

            
        if(current_time>40):
            break
                
#        print(str(timeInQueue)+", "+str(time_quantum))
#        print(current_time)
#        print(rem_bt)

#        print(wt)
        
#        print("queue1 size " + str(queue1.qsize()))
#        print("runQ size " + str(runQ.qsize()))
#        break
            
    return (schedule, sum(wt)/len(process_list))

def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result
def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    print ("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
    print ("simulating RR ----")
    RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    main(sys.argv[1:])

#process_list = read_input()
#print ("printing input ----")
#for process in process_list:
#    print (process)
#print ("simulating FCFS ----")
#FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
#write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )
#print ("simulating RR ----")
#RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum = 2)
#write_output('RR.txt', RR_schedule, RR_avg_waiting_time )
#print ("simulating SRTF ----")
#SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
#write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )
#print ("simulating SJF ----")
#SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
#write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )
