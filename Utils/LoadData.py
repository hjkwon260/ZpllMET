import pickle
import uproot
import pandas as pd

def get_concat(dic_df_all, dic_df_met_u_all, dic_df_met_d_all, dic_df_met_jer_u_all, dic_df_met_jer_d_all, dic_df_jes_u_all, dic_df_jes_d_all, dic_df_jer_u_all, dic_df_jer_d_all, dic_df_met_ue_u_all, dic_df_met_ue_d_all, dic_df_scale_u_all, dic_df_scale_d_all):
    dic_df, dic_df_met_u, dic_df_met_d, dic_df_met_jer_u, dic_df_met_jer_d, dic_df_jes_u, dic_df_jes_d, dic_df_jer_u, dic_df_jer_d, dic_df_met_ue_u, dic_df_met_ue_d, dic_df_scale_u, dic_df_scale_d = [{} for _ in range(13)]

    for key in dic_df_all[0]:
        list_raw, list_met_u, list_met_d, list_met_jer_u, list_met_jer_d, list_jes_u, list_jes_d, list_jer_u, list_jer_d, list_met_ue_u, list_met_ue_d, list_scale_u, list_scale_d = [[] for _ in range(13)]
        for i in range(len(dic_df_all)):
            try:
                list_raw.append(dic_df_all[i][key])
                list_met_u.append(dic_df_met_u_all[i][key])
                list_met_d.append(dic_df_met_d_all[i][key])                 
                list_met_jer_u.append(dic_df_met_jer_u_all[i][key])
                list_met_jer_d.append(dic_df_met_jer_d_all[i][key])
                list_jes_u.append(dic_df_jes_u_all[i][key])
                list_jes_d.append(dic_df_jes_d_all[i][key]) 
                list_jer_u.append(dic_df_jer_u_all[i][key])
                list_jer_d.append(dic_df_jer_d_all[i][key])             
                list_met_ue_u.append(dic_df_met_ue_u_all[i][key])
                list_met_ue_d.append(dic_df_met_ue_d_all[i][key])
                list_scale_u.append(dic_df_scale_u_all[i][key])
                list_scale_d.append(dic_df_scale_d_all[i][key])                    
            except:
                print("missing:", key)
        dic_df[key]=pd.concat(list_raw, ignore_index=True)
        dic_df_met_u[key]=pd.concat(list_met_u, ignore_index=True)
        dic_df_met_d[key]=pd.concat(list_met_d, ignore_index=True)        
        dic_df_met_jer_u[key]=pd.concat(list_met_jer_u, ignore_index=True)
        dic_df_met_jer_d[key]=pd.concat(list_met_jer_d, ignore_index=True)        
        dic_df_jes_u[key]=pd.concat(list_jes_u, ignore_index=True)
        dic_df_jes_d[key]=pd.concat(list_jes_d, ignore_index=True)        
        dic_df_jer_u[key]=pd.concat(list_jer_u, ignore_index=True)
        dic_df_jer_d[key]=pd.concat(list_jer_d, ignore_index=True)
        dic_df_met_ue_u[key]=pd.concat(list_met_ue_u, ignore_index=True)
        dic_df_met_ue_d[key]=pd.concat(list_met_ue_d, ignore_index=True)
        dic_df_scale_u[key]=pd.concat(list_scale_u, ignore_index=True)
        dic_df_scale_d[key]=pd.concat(list_scale_d, ignore_index=True)
    dic_df_all.clear()    
    dic_df_met_u_all.clear()    
    dic_df_met_d_all.clear()       
    dic_df_met_jer_u_all.clear()    
    dic_df_met_jer_d_all.clear()       
    dic_df_jes_u_all.clear()    
    dic_df_jes_d_all.clear()       
    dic_df_jer_u_all.clear()    
    dic_df_jer_d_all.clear()    
    dic_df_met_ue_u_all.clear()    
    dic_df_met_ue_d_all.clear() 
    dic_df_scale_u_all.clear()    
    dic_df_scale_d_all.clear() 

    dic_df_raw=dic_df
    dic_nested_shape_sys={}
    dic_nested_shape_sys["met_u"]=dic_df_met_u
    dic_nested_shape_sys["met_d"]=dic_df_met_d    
    dic_nested_shape_sys["met_ue_u"]=dic_df_met_ue_u
    dic_nested_shape_sys["met_ue_d"]=dic_df_met_ue_d 
    dic_nested_shape_sys["met_jer_u"]=dic_df_met_jer_u
    dic_nested_shape_sys["met_jer_d"]=dic_df_met_jer_d            
    dic_nested_shape_sys["jes_u"]=dic_df_jes_u
    dic_nested_shape_sys["jes_d"]=dic_df_jes_d             
    dic_nested_shape_sys["jer_u"]=dic_df_jer_u
    dic_nested_shape_sys["jer_d"]=dic_df_jer_d
    dic_nested_shape_sys["scale_u"]=dic_df_scale_u
    dic_nested_shape_sys["scale_d"]=dic_df_scale_d 

    return dic_df_raw, dic_nested_shape_sys

def get_files(files):
    list_nestec_dic = []
    for f in files:
        with open(INPUTDIR+'/'+f, 'rb') as f:
            nested_dic_df = pickle.load(f)
            list_nestec_dic.append(nested_dic_df)
    return list_nestec_dic

def get_list_dic(INPUTDIR, ERA, region):
    if region == "TR":
        region_list = ["SR1", "TTCR"]
    elif region == "SR":
        region_list = ["SR1"]
    elif region == "VR":
        region_list = ["TTCR"]
    elif region == "PTSB":
        region_list = ["PTSB"]
    elif region == "MASSSB":
        region_list = ["MASSSB"]
    elif region == "METSB":
        region_list = ["METSB", "SR1"] #temp    
    elif region == "MASSnoMETSB":
        region_list = ["MASSnoMETSB"]
    else:
        print("WARNING: check if REGION valid")
    list_nested_dic_df = []
    for region in region_list:
        if not "16" in ERA:
            with open(INPUTDIR+'/'+ERA+'/nested_dic_df_'+region+'.pkl', 'rb') as f:
                nested_dic_df = pickle.load(f)
                list_nested_dic_df.append(nested_dic_df)           
        else:
            with open(INPUTDIR+'/'+ERA+'pre/nested_dic_df_'+region+'.pkl', 'rb') as f:
                nested_dic_df = pickle.load(f)
                list_nested_dic_df.append(nested_dic_df) 
            with open(INPUTDIR+'/'+ERA+'post/nested_dic_df_'+region+'.pkl', 'rb') as f:
                nested_dic_df = pickle.load(f)
                list_nested_dic_df.append(nested_dic_df) 
    return list_nested_dic_df

def get_dic_raw_sys(ERA, INPUTDIR, region="TR"):
    # if region == "TR":
    #     if "16" in ERA: 
    #         files = [ERA+'pre/nested_dic_df_SR1.pkl', ERA+'pre/nested_dic_df_TTCR.pkl', ERA+'post/nested_dic_df_SR1.pkl', ERA+'post/nested_dic_df_TTCR.pkl']   
    #     else:
    #         files = [ERA+'/nested_dic_df_SR1.pkl', ERA+'/nested_dic_df_TTCR.pkl']

    # list_nestec_dic = get_files(files)

    # list_sys_key = ['raw', 'met_u', 'met_d', 'met_ue_u', 'met_ue_d', 'met_jer_u', 'met_jer_d', 'jes_u', 'jes_d', 'jer_u', 'jer_d', 'scale_u', 'scale_d']

    list_nested_dic_df = get_list_dic(INPUTDIR, ERA, region)
    # unroll
    dic_df_all = [nested_dic['raw'] for nested_dic in list_nested_dic_df]
    dic_df_met_u_all = [nested_dic['met_u'] for nested_dic in list_nested_dic_df]
    dic_df_met_d_all = [nested_dic['met_d'] for nested_dic in list_nested_dic_df]
    dic_df_met_jer_u_all = [nested_dic['met_jer_u'] for nested_dic in list_nested_dic_df]
    dic_df_met_jer_d_all = [nested_dic['met_jer_d'] for nested_dic in list_nested_dic_df]
    dic_df_jes_u_all = [nested_dic['jes_u'] for nested_dic in list_nested_dic_df]
    dic_df_jes_d_all = [nested_dic['jes_d'] for nested_dic in list_nested_dic_df]
    dic_df_jer_u_all = [nested_dic['jer_u'] for nested_dic in list_nested_dic_df]
    dic_df_jer_d_all = [nested_dic['jer_d'] for nested_dic in list_nested_dic_df]
    dic_df_met_ue_u_all = [nested_dic['met_ue_u'] for nested_dic in list_nested_dic_df]
    dic_df_met_ue_d_all = [nested_dic['met_ue_d'] for nested_dic in list_nested_dic_df]
    dic_df_scale_u_all = [nested_dic['scale_u'] for nested_dic in list_nested_dic_df]
    dic_df_scale_d_all = [nested_dic['scale_d'] for nested_dic in list_nested_dic_df]

    dic_df_raw, dic_nested_shape_sys = get_concat(dic_df_all, dic_df_met_u_all, dic_df_met_d_all, dic_df_met_jer_u_all, dic_df_met_jer_d_all, dic_df_jes_u_all, dic_df_jes_d_all, dic_df_jer_u_all, dic_df_jer_d_all, dic_df_met_ue_u_all, dic_df_met_ue_d_all, dic_df_scale_u_all, dic_df_scale_d_all)

    return dic_df_raw, dic_nested_shape_sys