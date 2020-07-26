import time;

import datetime 


def get_period(x):
    results=  list();
    t = time.perf_counter()
    for i in range(x):
        results.append(i);
    return  (time.perf_counter() - t) * (10000000)
        

def sample(rate):
    values  = list();
    secs  =  1;
    period  =  1/rate;
    while(True):
        secs  =  secs  -  period
        values.append(secs);
        if(secs <= 0):
            break;
        time.sleep(period);
        
    return values;
interval  =  get_period(100);
print("Time per sample : {0}µS".format(interval));
print("sample rate : {0}sS".format(interval/ 100000000));       
