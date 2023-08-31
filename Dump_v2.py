#!/usr/bin/env python
# coding: utf-8

# parent: Preselection_v6

# In[1]:


import os, sys
import numpy as np
import pickle
import uproot
import glob
import pandas as pd
from tqdm import tqdm
import json
import ROOT as rt
import fnmatch

## user define
sys.path.append('.')
sys.path.append('./Utils')
from Plotter import HistStack

from beeps import *


# # Set config

# In[2]:


# ERA="ee17"
# ERA="ee16pre"
# # ERA="mm18"
# ERA="em18"
# # DATE = '20230129_17_eleffmva'
# DATE = '20230301_18'
# # DATE = '20230130_18_dyhighworctight'
# # INPUTDIR = "/eos/user/h/hkwon/Run2/20230130_18_dyhighworctight/mm/"
# INPUTDIR = "/eos/user/h/hkwon/Run2/20230301_18/em/"
import sys
ERA = sys.argv[1]
DATE = sys.argv[2]
INPUTDIR = sys.argv[3]

DUMP_PKL = False
DUMP_SIDEBAND_MET_PKL = False
DUMP_SIDEBAND_MASS_PKL = False
DUMP_SIDEBAND_PT_PKL = False
DUMP_DIVIDED_BY_BTAG = True
# DRAW_SR = True
# RUN_SIDEBAND_MET = False
# RUN_SIDEBAND_MASS = False
# RUN_SIDEBAND_PT = False
# RUN_BTAG = True
# EXPORT_VARIABLE = False

# # for dev
# ERA = "em18"
# DATE = "20230819lep_18"
# INPUTDIR = "/eos/user/h/hkwon/Run2/"+DATE+"/em/"


# # Get input

# In[3]:


lumi_all={
    "ee16pre":19520,
    "ee16post":16810,
    "ee17":41480,
    "ee18":59830,
    "mm16pre":19520,
    "mm16post":16810,
    "mm17":41480,
    "mm18":59830,    
#     "mm18":14000,    
    "em16pre":19520,
    "em16post":16810,
    "em17":41480,
    "em18":59830     
}

data_evts = {
    "ee16pre":652566543,
    "ee16post":287977113,
    "ee17":460041183,
    "ee18":1326465857,
    "mm16pre":458655573,
    "mm16post":327037312,
    "mm17":739073837,
#     "mm18":944842550,  #949352777 
    "mm18":949352777,  #949352777 
    "em16pre":1111222116,
    "em16post":615014425,
    "em17":1199115020,
#     "em18":2271308407   #2281001366  
    "em18":2281001366   #2281001366  
}

lumi=lumi_all[ERA]
print(ERA, lumi)

channel = ERA.replace("16pre", "")
channel = channel.replace("16post", "")
channel = channel.replace("17", "")
channel = channel.replace("18", "")

def get_df(root_file_name, unneccesary_columns):
    f = uproot.open(root_file_name)
    df = uproot.open(root_file_name)["Events_"+channel].arrays(library="pd")
    df_met_u = uproot.open(root_file_name)["Events_"+channel+"_met_u"].arrays(library="pd")
    df_met_d = uproot.open(root_file_name)["Events_"+channel+"_met_d"].arrays(library="pd")     
    df_met_jer_u = uproot.open(root_file_name)["Events_"+channel+"_met_jer_u"].arrays(library="pd")
    df_met_jer_d = uproot.open(root_file_name)["Events_"+channel+"_met_jer_d"].arrays(library="pd")    
    df_met_ue_u = uproot.open(root_file_name)["Events_"+channel+"_met_ue_u"].arrays(library="pd")
    df_met_ue_d = uproot.open(root_file_name)["Events_"+channel+"_met_ue_d"].arrays(library="pd") 
    df_scale_u = uproot.open(root_file_name)["Events_"+channel+"_scale_u"].arrays(library="pd")
    df_scale_d = uproot.open(root_file_name)["Events_"+channel+"_scale_d"].arrays(library="pd")
    info = uproot.open(root_file_name)["Info_"+channel].arrays(library="pd")
#     return sum(info["sumweight"]), df.drop(unneccesary_columns, axis=1), df_met_u.drop(unneccesary_columns, axis=1), df_met_d.drop(unneccesary_columns, axis=1), df_scale_u.drop(unneccesary_columns, axis=1), df_scale_d.drop(unneccesary_columns, axis=1)
    return sum(info["sumweight"]), df.drop(unneccesary_columns, axis=1), df_met_u.drop(unneccesary_columns, axis=1), df_met_d.drop(unneccesary_columns, axis=1), df_met_jer_u.drop(unneccesary_columns, axis=1), df_met_jer_d.drop(unneccesary_columns, axis=1), df_met_ue_u.drop(unneccesary_columns, axis=1), df_met_ue_d.drop(unneccesary_columns, axis=1), df_scale_u.drop(unneccesary_columns, axis=1), df_scale_d.drop(unneccesary_columns, axis=1)

unneccesary_columns = []
dic_input = {
    "ee16pre": "/eos/user/h/hkwon/Run2/"+DATE+"_16pre/ee/",
    "mm16pre": "/eos/user/h/hkwon/Run2/"+DATE+"_16pre/mm/",
    "em16pre": "/eos/user/h/hkwon/Run2/"+DATE+"_16pre/em/",
    "ee16post": "/eos/user/h/hkwon/Run2/"+DATE+"_16post/ee/",
    "mm16post": "/eos/user/h/hkwon/Run2/"+DATE+"_16post/mm/",
    "em16post": "/eos/user/h/hkwon/Run2/"+DATE+"_16post/em/",
    "ee17": "/eos/user/h/hkwon/Run2/"+DATE+"_17/ee/",
    "mm17": "/eos/user/h/hkwon/Run2/"+DATE+"_17/mm/",
    "em17": "/eos/user/h/hkwon/Run2/"+DATE+"_17/em/",
    "ee18": "/eos/user/h/hkwon/Run2/"+DATE+"_18/ee/",
    "mm18": "/eos/user/h/hkwon/Run2/"+DATE+"_18/mm/",    
    "em18": "/eos/user/h/hkwon/Run2/"+DATE+"_18/em/"        
#     "em18": "/eos/user/h/hkwon/Run2/20221120_18/em/"        
}
# input_dir = dic_input[ERA]
input_dir = INPUTDIR
f = []
for (dirpath, dirnames, filenames) in os.walk(input_dir):
    f.extend(filenames)
    break

dic_tup={}
for file in tqdm(f):
    # file naming: flatNtuple_Preselect_WZ1.root, flatNtuple_Preselect_Zp-3700_CH-1345.root
    if not "flatNtuple" in file:
        continue
#     if channel=="mm" and (fnmatch.fnmatch(file, '*E*Run*') or fnmatch.fnmatch(file, '*M*RunB*') or fnmatch.fnmatch(file, '*M*RunC*') or fnmatch.fnmatch(file, '*M*RunD*')): #temp
#     if channel=="mm" and fnmatch.fnmatch(file, '*E*Run*'): #temp
#         continue
#     if channel=="ee" and fnmatch.fnmatch(file, '*M*Run*'):
#         continue
#     if channel=="em" and fnmatch.fnmatch(file, '*E*Run*'):
#         continue 
    if "Run" in file and not "hadd" in file:
        continue
    if "TT" in file and not "hadd" in file:
        continue
    if "DY" in file and not "hadd" in file and not "To" in file:
        continue  
    if "TW" in file and not "hadd" in file:
        continue         
    if "WW" in file and not "hadd" in file:
        continue  
    if "WZ" in file and not "hadd" in file:
        continue      
    if "ZZ" in file and not "hadd" in file:
        continue      
    if "Htt" in file and not "hadd" in file:
        continue  
        
    if "Zp" in file:
        sample=file.split('_')[2]+"_"+file.split('_')[3]
    else:
        print(file)
        sample=file.split('_')[2]
    sample=sample.rstrip('.root')
    try:
        print(sample)
        dic_tup[sample]=get_df(input_dir+file, unneccesary_columns)   
    except:
        print(sample)
        beep()        
        if "Run" in sample: # check file corrupt
            raise    
# dic_tup


# In[4]:


beep_ok()


# In[5]:


# for key in dic_tup:
#     print(key)


# In[6]:


# get x-sec
dic_xsec={}
with open('config/CrossSection.json') as json_file:
    data = json.load(json_file)
    dic_xsec=data
print(dic_xsec)


# In[7]:


merged_dic_df={}
for key in dic_tup:       
    merged_dic_df[key]=dic_tup[key]


# In[8]:


# # free memory 
# dic_tup.clear()


# In[9]:


totalinput = """
######################################################
####   Total input number of events (sumweight)   ####
######################################################
"""

print(totalinput)

# merged_dic_df["Zp-2500"]=dic_tup["Zp-2500"][0], dic_tup["Zp-2500"][1] 
hadded = ["Data", "TT", "TTSemi", "TTUp", "TTDown", "TThdampUp", "TThdampDown", "top", "antitop", "WW", "WZ", "WZQQ", "DY", "TTZ", "ZZ", "H", "HWW", "WWW", "WWZ"]
for p in hadded:
    print(p, ":", merged_dic_df[p][0])


# In[10]:


out_dir = DATE+"/Presel/DUMP/"+ERA


# In[11]:


os.system("mkdir -p "+out_dir)
with open(out_dir+'/Nevents.txt', 'w') as f:
    f.write(totalinput)


# In[12]:


print("expected:", data_evts[ERA], ", while: ", merged_dic_df['Data'][0])

# try:
#    if data_evts[ERA]!=sum(Data_nevts):
#        raise ValueError('Data events missing!')
# except (ValueError, IndexError):
#    beep()
#    print("expected:", data_evts[ERA], ", while: ", sum(Data_nevts)) 
#    raise


# In[13]:


# # temp!!
for key in merged_dic_df:
    df = merged_dic_df[key][1]
    df_met_u = merged_dic_df[key][2]
    df_met_d = merged_dic_df[key][3]    
    df_met_ue_u = merged_dic_df[key][4]
    df_met_ue_d = merged_dic_df[key][5]
    df_scale_u = merged_dic_df[key][6]
    df_scale_d = merged_dic_df[key][7]
#     print(df[df.isin([np.inf, -np.inf]).any(1)])
    if df.isnull().values.any():
        print("Warning, nan in",key)
        i = df[df.isin([np.nan, np.inf, -np.inf]).any(1)].index
        print(i)
        df_new = df.drop(i)
        df_met_u_new = df_met_u.drop(i)
        df_met_d_new = df_met_d.drop(i)        
        df_met_ue_u_new = df_met_ue_u
        df_met_ue_d_new = df_met_ue_d        
        df_scale_u_new = df_scale_u
        df_scale_d_new = df_scale_d
#         print(df_new.isnull().values.any())
        #workaround for tuple assignment
#         merged_dic_df[key] = merged_dic_df[key][0], df_new, df_met_u_new, df_met_d_new, df_scale_u, df_scale_d
        merged_dic_df[key] = merged_dic_df[key][0], df_new, df_met_u_new, df_met_d_new, df_met_ue_u_new, df_met_ue_d_new, df_scale_u_new, df_scale_d_new
        


# In[14]:


# sys = ["puweight_pre", "l1prefiring_pre", 'effSF_pre', 'topSF_pre', 'genweight_pre', 'trigSF_pre']
sys = ["puweight_pre", "l1prefiring_pre", 'effSF_pre', 'effrecoSF_pre', 'topSF_pre', 'genweight_pre', 'trigSF_pre', 'btagSF_pre']
# sys = ["puweight_pre", "l1prefiring_pre", 'effSF_pre', 'topSF_pre', 'genweight_pre']
eventweights = """
####################################################
####       event weights (normalization)        ####
####################################################
"""

def get_dic_with_weight(merged_dic_df):
    dic_df={}
    dic_df_met_u={}
    dic_df_met_d={}    
    dic_df_met_jer_u={}
    dic_df_met_jer_d={}
    dic_df_met_ue_u={}
    dic_df_met_ue_d={}
    dic_df_scale_u={}
    dic_df_scale_d={}
    for key, vs in merged_dic_df.items():
        print(key) 
        if vs[0]==0:
            print("missing: ", key, "!, continue without it")
            continue
        if "Data" in key:
            norm=1
        else:
            if fnmatch.fnmatch(key, '*DY*To*'):
                key = key[:len(key)-1]
            norm=lumi*dic_xsec[key]/vs[0]
        print(key, ":", norm)
        global eventweights
        eventweights+=key+":"+str(norm)+"\n"
#         print(eventweights)
        dic_df[key]=vs[1]
        dic_df_met_u[key] = vs[2]
        dic_df_met_d[key] = vs[3]        
        dic_df_met_jer_u[key] = vs[3]
        dic_df_met_jer_d[key] = vs[4]
        dic_df_met_ue_u[key] = vs[5]
        dic_df_met_ue_d[key] = vs[6]
        dic_df_scale_u[key] = vs[7]
        dic_df_scale_d[key]=vs[8]
        dic_df[key]["weight"] = vs[1]["genweight_pre"]*norm
#         dic_df[key]["lumifilter"] = np.ones(vs[1]["genweight_pre"].shape[0])
        a = np.ones(vs[1]["genweight_pre"].shape[0])
        a[int(vs[1]["genweight_pre"].shape[0]*1/3):] = 0
        if key=="Data":
            a = np.zeros(vs[1]["genweight_pre"].shape[0])
#         print(a)
        dic_df_met_u[key]["weightmetUp"] = vs[1]["genweight_pre"]*norm
        dic_df_met_d[key]["weightmetDown"] = vs[1]["genweight_pre"]*norm        
        dic_df_met_jer_u[key]["weightmetjerUp"] = vs[1]["genweight_pre"]*norm
        dic_df_met_jer_d[key]["weightmetjerDown"] = vs[1]["genweight_pre"]*norm
        dic_df_met_ue_u[key]["weightmetueUp"] = vs[1]["genweight_pre"]*norm
        dic_df_met_ue_d[key]["weightmetueDown"] = vs[1]["genweight_pre"]*norm
        dic_df_scale_u[key]["weightscaleUp"] = vs[1]["genweight_pre"]*norm
        dic_df_scale_d[key]["weightscaleDown"] = vs[1]["genweight_pre"]*norm
#         dic_df_met_u[key]["hemveto"] = vs[1]["hemveto"]
#         dic_df_met_d[key]["hemveto"] = vs[1]["hemveto"]       
#         dic_df_met_jer_u[key]["hemveto"] = vs[1]["hemveto"]
#         dic_df_met_jer_d[key]["hemveto"] = vs[1]["hemveto"]
#         dic_df_met_ue_u[key]["hemveto"] = vs[1]["hemveto"]
#         dic_df_met_ue_d[key]["hemveto"] = vs[1]["hemveto"]
#         dic_df_scale_u[key]["hemveto"] = vs[1]["hemveto"]
#         dic_df_scale_d[key]["hemveto"] = vs[1]["hemveto"]
        dic_df[key]["hemfilter"] = a + vs[1]["hemveto"]
        dic_df_met_u[key]["hemfilter"] = a + vs[1]["hemveto"]
        dic_df_met_d[key]["hemfilter"] = a + vs[1]["hemveto"]    
        dic_df_met_jer_u[key]["hemfilter"] = a + vs[1]["hemveto"]
        dic_df_met_jer_d[key]["hemfilter"] = a + vs[1]["hemveto"]
        dic_df_met_ue_u[key]["hemfilter"] = a + vs[1]["hemveto"]
        dic_df_met_ue_d[key]["hemfilter"] = a + vs[1]["hemveto"]
        dic_df_scale_u[key]["hemfilter"] = a + vs[1]["hemveto"]
        dic_df_scale_d[key]["hemfilter"] = a + vs[1]["hemveto"]
        dic_df[key]["wopu"] = vs[1]["genweight_pre"]*norm
        dic_df[key]["wol1"] = vs[1]["genweight_pre"]*norm
        dic_df[key]["woeff"] = vs[1]["genweight_pre"]*norm
        dic_df[key]["wotop"] = vs[1]["genweight_pre"]*norm       
        dic_df[key]["wobsf"] = vs[1]["genweight_pre"]*norm       
      
        for s in sys:
            if s=="genweight_pre":
                continue
            dic_df[key]["weight"] *= vs[1][s]
            dic_df_met_u[key]["weightmetUp"] *= vs[1][s]
            dic_df_met_d[key]["weightmetDown"] *= vs[1][s]            
            dic_df_met_jer_u[key]["weightmetjerUp"] *= vs[1][s]
            dic_df_met_jer_d[key]["weightmetjerDown"] *= vs[1][s]            
            dic_df_met_ue_u[key]["weightmetueUp"] *= vs[1][s]
            dic_df_met_ue_d[key]["weightmetueDown"] *= vs[1][s]            
            dic_df_scale_u[key]["weightscaleUp"] *= vs[1][s]
            dic_df_scale_d[key]["weightscaleDown"] *= vs[1][s]       

            # n-1 correction
            if s!="puweight_pre":
                dic_df[key]["wopu"] *= vs[1][s]
            if s!="l1prefiring_pre":
                dic_df[key]["wol1"] *= vs[1][s]
            if s!="effSF_pre":
                dic_df[key]["woeff"] *= vs[1][s]
#             if s!="topSF_pre":
            if not "top" in s:
                dic_df[key]["wotop"] *= vs[1][s]
            if s!="btagSF_pre":
                dic_df[key]["wobsf"] *= vs[1][s]

        dic_df[key]["weighthdampUp"] = dic_df[key]["weight"].copy(deep=True)
        dic_df[key]["weighthdampDown"] = dic_df[key]["weight"].copy(deep=True)
        dic_df[key]["weightPSUp"] = dic_df[key]["weight"].copy(deep=True)
        dic_df[key]["weightPSDown"] = dic_df[key]["weight"].copy(deep=True)            
        dic_df[key]["weightJECUp"] = dic_df[key]["weight"].copy(deep=True)/vs[1]["btagSF_pre"]*vs[1]["btagSF_jes_u_pre"]            
        dic_df[key]["weightJECDown"] = dic_df[key]["weight"].copy(deep=True)/vs[1]["btagSF_pre"]*vs[1]["btagSF_jes_d_pre"]         
        dic_df[key]["weightJERUp"] = dic_df[key]["weight"].copy(deep=True)/vs[1]["btagSF_pre"]*vs[1]["btagSF_jer_u_pre"]            
        dic_df[key]["weightJERDown"] = dic_df[key]["weight"].copy(deep=True)/vs[1]["btagSF_pre"]*vs[1]["btagSF_jer_d_pre"]                      
            
        # up, down    
        for s1 in sys:
            #if "top" in s1 or "eff" in s1:
#             if "btag" in s1:
#                 continue
            s_u = s1.replace("_", "_u_")
            s_d = s1.replace("_", "_d_")
            if s1=="genweight_pre":
                dic_df[key]["weight"+s_u.replace('_u_pre', 'Up')] = dic_df[key]["weight"].copy(deep=True)*np.fabs(dic_df[key][s_u])
                dic_df[key]["weight"+s_d.replace('_d_pre', 'Down')] = dic_df[key]["weight"].copy(deep=True)*np.fabs(dic_df[key][s_d])
            else:
                dic_df[key]["weight"+s_u.replace('_u_pre', 'Up')] = dic_df[key]["weight"].copy(deep=True)/dic_df[key][s1]*dic_df[key][s_u]
                dic_df[key]["weight"+s_d.replace('_d_pre', 'Down')] = dic_df[key]["weight"].copy(deep=True)/dic_df[key][s1]*dic_df[key][s_d]             
#     return dic_df, dic_df_met_u, dic_df_met_d, dic_df_scale_u, dic_df_scale_d
    return dic_df, dic_df_met_u, dic_df_met_d, dic_df_met_jer_u, dic_df_met_jer_d, dic_df_met_ue_u, dic_df_met_ue_d, dic_df_scale_u, dic_df_scale_d

# dic_df, dic_df_met_u, dic_df_met_d, dic_df_scale_u, dic_df_scale_d = get_dic_with_weight(merged_dic_df)
dic_df, dic_df_met_u, dic_df_met_d, dic_df_met_jer_u, dic_df_met_jer_d, dic_df_met_ue_u, dic_df_met_ue_d, dic_df_scale_u, dic_df_scale_d = get_dic_with_weight(merged_dic_df)


# In[15]:


with open(out_dir+'/Nevents.txt', 'a') as f:
    f.write(eventweights)


# # Preselection

# In[16]:


dic_df_list = [dic_df, dic_df_met_u, dic_df_met_d, dic_df_met_jer_u, dic_df_met_jer_d, dic_df_met_ue_u, dic_df_met_ue_d, dic_df_scale_u, dic_df_scale_d]
dic_key_list = ['raw', 'met_u', 'met_d', 'met_jer_u', 'met_jer_d', 'met_ue_u', 'met_ue_d', 'scale_u', 'scale_d']


# In[17]:


def get_nested_dic(dic_df_list, dic_key_list, query_str):
    weihtedevents = """
    #############################################################
    ####   unweighted (weighted) #events after preselection  ####
    #############################################################
    """

    nested_dic_df={}

    for i, dic in enumerate(dic_df_list):
        dic_tmp = {}
        for key in dic:
#             query_str_new = query_str
#             if "18" in ERA and key=='Data':
#                 query_str_new += " and hemveto==1"
#             if "18" in ERA and key!='Data':
#                 query_str_new += " and hemfilter>0"
            dic_tmp[key]=dic[key].query(query_str)
            unweighted_nevt = dic_tmp[key].shape[0]
            if dic_key_list[i]=='raw':
                print(key, dic_key_list[i], ":", unweighted_nevt, "(", sum(dic_tmp[key]["weight"]), ")")  
                weihtedevents+=key+":"+str(unweighted_nevt)+"("+str(sum(dic_tmp[key]["weight"]))+")\n"
            else:
                print(key, dic_key_list[i], ":", dic_tmp[key].shape[0])
        #     print(key, ":", unweighted_nevt, "(", unweighted_nevt*lumi*dic_xsec[key]/merged_dic_df[key][0], ")")
        nested_dic_df[dic_key_list[i]]=dic_tmp
    
    return nested_dic_df, weihtedevents


# In[18]:


# query_str="mass_pre>100 and pt_lead_pre>80 and pt_trail_pre>40 and PuppiMET_pre>100"

# nested_dic_df, weihtedevents = get_nested_dic(dic_df_list, dic_key_list, query_str)


# In[19]:


# with open(out_dir+'/Nevents.txt', 'a') as f:
#     f.write(weihtedevents)


# In[20]:


# if DUMP_PKL or "16" in ERA:
#     print("Dump pickle")
#     with open(out_dir+"/"+"nested_dic_df.pkl", "wb") as f:
#         pickle.dump(nested_dic_df, f)


# # b tag selection

# In[21]:


if DUMP_DIVIDED_BY_BTAG:

    base_line = "mass_pre>100 and pt_lead_pre>80 and pt_trail_pre>40 and PuppiMET_pre>100"
    
    if "18" in ERA:
        base_line += " and hemfilter>0"
#     query_str="mass_pre>100 and pt_lead_pre>80 and pt_trail_pre>40 and PuppiMET_pre>100 and njet_pre==1" #temp!
    query_str=base_line+" and nbjetflav_pre==0" #temp!
#     query_str=base_line #temp!

    nested_dic_df, weihtedevents = get_nested_dic(dic_df_list, dic_key_list, query_str)
    # nbjet_jec
    dic_tmp = {}
    selected_columns = ['PuppiMET_pre', 'PuppiMET_phi_pre', 'mass_pre', 'pt_lead_pre', 'pt_trail_pre', 'U_pre',
       'JZB_pre', 'dPhill_pre', 'dPhilMET_pre', 'MT_pre', 'MT2_pre', 'Zpt_pre',
       'dRll_pre', 'dPhillMET_pre', 'eta_lead_pre', 'eta_trail_pre',
       'njet_pre', 'nbjetflav_pre', 'nbjetflav_jesup_pre', 'weightJECUp', 'hemfilter']    
    for key in dic_df:  
        dic_tmp[key]=dic_df[key][selected_columns].query(base_line+" and nbjetflav_jesup_pre==0")
        unweighted_nevt = dic_tmp[key].shape[0]
    nested_dic_df['jes_u'] = dic_tmp
    # nbjet_jec
    dic_tmp = {}
    selected_columns = ['PuppiMET_pre', 'PuppiMET_phi_pre', 'mass_pre', 'pt_lead_pre', 'pt_trail_pre', 'U_pre',
       'JZB_pre', 'dPhill_pre', 'dPhilMET_pre', 'MT_pre', 'MT2_pre', 'Zpt_pre',
       'dRll_pre', 'dPhillMET_pre', 'eta_lead_pre', 'eta_trail_pre',
       'njet_pre', 'nbjetflav_pre', 'nbjetflav_jesdown_pre', 'weightJECDown', 'hemfilter']    
    for key in dic_df:  
        dic_tmp[key]=dic_df[key][selected_columns].query(base_line+" and nbjetflav_jesdown_pre==0")
        unweighted_nevt = dic_tmp[key].shape[0]    
    nested_dic_df['jes_d'] = dic_tmp
    # nbjet_jer
    dic_tmp = {}
    selected_columns = ['PuppiMET_pre', 'PuppiMET_phi_pre', 'mass_pre', 'pt_lead_pre', 'pt_trail_pre', 'U_pre',
       'JZB_pre', 'dPhill_pre', 'dPhilMET_pre', 'MT_pre', 'MT2_pre', 'Zpt_pre',
       'dRll_pre', 'dPhillMET_pre', 'eta_lead_pre', 'eta_trail_pre',
       'njet_pre', 'nbjetflav_pre', 'nbjetflav_jerup_pre', 'weightJERUp', 'hemfilter']    
    for key in dic_df:  
        dic_tmp[key]=dic_df[key][selected_columns].query(base_line+" and nbjetflav_jerup_pre==0")
        unweighted_nevt = dic_tmp[key].shape[0]
    nested_dic_df['jer_u'] = dic_tmp
    # nbjet_jer
    dic_tmp = {}
    selected_columns = ['PuppiMET_pre', 'PuppiMET_phi_pre', 'mass_pre', 'pt_lead_pre', 'pt_trail_pre', 'U_pre',
       'JZB_pre', 'dPhill_pre', 'dPhilMET_pre', 'MT_pre', 'MT2_pre', 'Zpt_pre',
       'dRll_pre', 'dPhillMET_pre', 'eta_lead_pre', 'eta_trail_pre',
       'njet_pre', 'nbjetflav_pre', 'nbjetflav_jerdown_pre', 'weightJERDown', 'hemfilter']    
    for key in dic_df:  
        dic_tmp[key]=dic_df[key][selected_columns].query(base_line+" and nbjetflav_jerdown_pre==0")
        unweighted_nevt = dic_tmp[key].shape[0]    
    nested_dic_df['jer_d'] = dic_tmp    
    with open(out_dir+"/"+"nested_dic_df_SR1.pkl", "wb") as f:
        pickle.dump(nested_dic_df, f) 
        
    nested_dic_df.clear()
    
    ####################################################
    query_str=base_line+" and nbjetflav_pre>0" #temp!

    nested_dic_df, weihtedevents = get_nested_dic(dic_df_list, dic_key_list, query_str)
    
    # nbjet_jec
    dic_tmp = {}
    selected_columns = ['PuppiMET_pre', 'PuppiMET_phi_pre', 'mass_pre', 'pt_lead_pre', 'pt_trail_pre', 'U_pre',
       'JZB_pre', 'dPhill_pre', 'dPhilMET_pre', 'MT_pre', 'MT2_pre', 'Zpt_pre',
       'dRll_pre', 'dPhillMET_pre', 'eta_lead_pre', 'eta_trail_pre',
       'njet_pre', 'nbjetflav_pre', 'nbjetflav_jesup_pre', 'weightJECUp', 'hemfilter']    
    for key in dic_df:  
        dic_tmp[key]=dic_df[key][selected_columns].query(base_line+" and nbjetflav_jesup_pre>0")
        unweighted_nevt = dic_tmp[key].shape[0]
    nested_dic_df['jes_u'] = dic_tmp
    # nbjet_jec
    dic_tmp = {}
    selected_columns = ['PuppiMET_pre', 'PuppiMET_phi_pre', 'mass_pre', 'pt_lead_pre', 'pt_trail_pre', 'U_pre',
       'JZB_pre', 'dPhill_pre', 'dPhilMET_pre', 'MT_pre', 'MT2_pre', 'Zpt_pre',
       'dRll_pre', 'dPhillMET_pre', 'eta_lead_pre', 'eta_trail_pre',
       'njet_pre', 'nbjetflav_pre', 'nbjetflav_jesdown_pre', 'weightJECDown', 'hemfilter']    
    for key in dic_df:  
        dic_tmp[key]=dic_df[key][selected_columns].query(base_line+" and nbjetflav_jesdown_pre>0")
        unweighted_nevt = dic_tmp[key].shape[0]    
    nested_dic_df['jes_d'] = dic_tmp
    # nbjet_jer
    dic_tmp = {}
    selected_columns = ['PuppiMET_pre', 'PuppiMET_phi_pre', 'mass_pre', 'pt_lead_pre', 'pt_trail_pre', 'U_pre',
       'JZB_pre', 'dPhill_pre', 'dPhilMET_pre', 'MT_pre', 'MT2_pre', 'Zpt_pre',
       'dRll_pre', 'dPhillMET_pre', 'eta_lead_pre', 'eta_trail_pre',
       'njet_pre', 'nbjetflav_pre', 'nbjetflav_jerup_pre', 'weightJERUp', 'hemfilter']    
    for key in dic_df:  
        dic_tmp[key]=dic_df[key][selected_columns].query(base_line+" and nbjetflav_jerup_pre>0")
        unweighted_nevt = dic_tmp[key].shape[0]
    nested_dic_df['jer_u'] = dic_tmp
    # nbjet_jer
    dic_tmp = {}
    selected_columns = ['PuppiMET_pre', 'PuppiMET_phi_pre', 'mass_pre', 'pt_lead_pre', 'pt_trail_pre', 'U_pre',
       'JZB_pre', 'dPhill_pre', 'dPhilMET_pre', 'MT_pre', 'MT2_pre', 'Zpt_pre',
       'dRll_pre', 'dPhillMET_pre', 'eta_lead_pre', 'eta_trail_pre',
       'njet_pre', 'nbjetflav_pre', 'nbjetflav_jerdown_pre', 'weightJERDown', 'hemfilter']    
    for key in dic_df:  
        dic_tmp[key]=dic_df[key][selected_columns].query(base_line+" and nbjetflav_jerdown_pre>0")
        unweighted_nevt = dic_tmp[key].shape[0]    
    nested_dic_df['jer_d'] = dic_tmp 
    
    with open(out_dir+"/"+"nested_dic_df_TTCR.pkl", "wb") as f:
        pickle.dump(nested_dic_df, f) 
        
    nested_dic_df.clear()    


# In[ ]:




