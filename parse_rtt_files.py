f = "time2eventABT_ID_RTT_plots.r"
"""
R file produced running: 

python plotRJforward.v3.py literate_mcmc_logs -skipbins 1 -ggplot 0

"""



import numpy as np
import pandas as pd

def parse_r_vec(t, vec_name):
    t = l.split("%s=c(" % vec_name)[1]
    t = t.split(")\n")[0]
    vec = np.array(t.split(',')).astype(float)
    return vec
  
tdwg = []  
b_rate = []
d_rate = []
div_rate = []
max_len = []
times = []
with open(f, 'r') as rtt:
    for l in rtt.readlines():
        b, d, n = [], [], []
        if "main='time2event" in l:
            a = l.split("main='time2event")[1]
            tdwg.append(a.split("_ID_mcmc")[0])
        if 'time=c(' in l:
            times_tmp = parse_r_vec(l, "time")
            if len(times_tmp) > len(times):
                times = times_tmp
            print(np.max(times))
            
        if "birth_rate=c(" in l:
            b = parse_r_vec(l, "birth_rate")
            b_rate.append(b)
            
        if "death_rate=c(" in l:
            d = parse_r_vec(l, "death_rate")
            d_rate.append(d)
        if "net_diversity=c(" in l:    
            n = parse_r_vec(l, "net_diversity")
            div_rate.append(n)
        if np.max([len(b), len(d), len(n)]) > 0:
            max_len.append(np.max([len(b), len(d), len(n)]))
          
          
b_rate_a = np.zeros((len(b_rate), np.max(max_len))) + np.nan 
d_rate_a = np.zeros((len(b_rate), np.max(max_len))) + np.nan 
n_rate_a = np.zeros((len(b_rate), np.max(max_len))) + np.nan 

for i in range(len(b_rate)):
    b_rate_a[i, -len(b_rate[i]):] = b_rate[i]
    d_rate_a[i, -len(d_rate[i]):] = d_rate[i]
    n_rate_a[i, -len(div_rate[i]):] = np.floor(div_rate[i])

b_pd = pd.DataFrame(b_rate_a)    
b_pd.index = tdwg
b_pd.columns =  - (np.arange(np.max(max_len))[::-1] - 2022)
b_pd.to_csv("/Users/dsilvestro/Documents/Projects/Ongoing/Darkspot/Species_description_rates_all.csv", na_rep='NA')

d_pd = pd.DataFrame(d_rate_a)    
d_pd.index = tdwg
d_pd.columns = - (np.arange(np.max(max_len))[::-1] - 2022)
d_pd.to_csv("/Users/dsilvestro/Documents/Projects/Ongoing/Darkspot/Species_sampling_rates_all.csv", na_rep='NA')

div_pd = pd.DataFrame(n_rate_a)    
div_pd.index = tdwg
div_pd.columns = - (np.arange(np.max(max_len))[::-1] - 2022)
div_pd.to_csv("/Users/dsilvestro/Documents/Projects/Ongoing/Darkspot/Species_to_be_sampled_all.csv", na_rep='NA')

