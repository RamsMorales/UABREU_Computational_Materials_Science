# $PWD/.venv/bin/python

import re
import numpy as np

time_data = "times.txt"
times = []
with open(time_data,"r") as file:
    for line in file:
        #print(line)
        m = float(re.search(r"\d",line).group(0))
       # print(m.group(0))
        sec = float(re.search(r"\d{1,}\.\d{1,}",line).group(0))
        #print(sec.group(0))
        job_time = m * 60 + sec
        times.append(job_time)

count_above_4 = len([x for x in times if x > (4 * 60)]) 
count_above_5 = len([x for x in times if x > (5 * 60)])
print(f"Proportion of jobs over 4 min {count_above_4 / len(times)*100}")
print(f"Proportion of jobs over 5 min {count_above_5 / len(times)*100}")
print(f"Average real time is {np.mean(times)/60} minutes")
print(f"Standard Deviation of real time is {np.std(times)} seconds")
