import pickle
import uproot
import pandas as pd
def get_dic_raw_sys(ERA, INPUTDIR, region="TR"):
    if region == "TR":
        if "16" in ERA:
            with open(INPUTDIR+'/'+ERA+'pre/nested_dic_df_SR1.pkl', 'rb') as f:
                nested_dic_df = pickle.load(f)
            with open(INPUTDIR+'/'+ERA+'pre/nested_dic_df_TTCR.pkl', 'rb') as f:
                nested_dic_df1 = pickle.load(f)
            with open(INPUTDIR+'/'+ERA+'post/nested_dic_df_SR1.pkl', 'rb') as f:
                nested_dic_df2 = pickle.load(f)
            with open(INPUTDIR+'/'+ERA+'post/nested_dic_df_TTCR.pkl', 'rb') as f:
                nested_dic_df3 = pickle.load(f)
            dic_df_all = [nested_dic_df['raw'], nested_dic_df1['raw'], nested_dic_df2['raw'], nested_dic_df3['raw']]
            dic_df_met_u_all = [nested_dic_df['met_u'], nested_dic_df1['met_u'], nested_dic_df2['met_u'], nested_dic_df3['met_u']]
            dic_df_met_d_all = [nested_dic_df['met_d'], nested_dic_df1['met_d'], nested_dic_df2['met_d'], nested_dic_df3['met_d']]    
            dic_df_met_ue_u_all = [nested_dic_df['met_ue_u'], nested_dic_df1['met_ue_u'], nested_dic_df2['met_ue_u'], nested_dic_df3['met_ue_u']]
            dic_df_met_ue_d_all = [nested_dic_df['met_ue_d'], nested_dic_df1['met_ue_d'], nested_dic_df2['met_ue_d'], nested_dic_df3['met_ue_d']]
        else:
            with open(INPUTDIR+'/'+ERA+'/nested_dic_df_SR1.pkl', 'rb') as f:
                nested_dic_df = pickle.load(f)
            with open(INPUTDIR+'/'+ERA+'/nested_dic_df_TTCR.pkl', 'rb') as f:
                nested_dic_df1 = pickle.load(f)
            dic_df_all = [nested_dic_df['raw'], nested_dic_df1['raw']]
            dic_df_met_u_all = [nested_dic_df['met_u'], nested_dic_df1['met_u']]
            dic_df_met_d_all = [nested_dic_df['met_d'], nested_dic_df1['met_d']]    
            dic_df_met_ue_u_all = [nested_dic_df['met_ue_u'], nested_dic_df1['met_ue_u']]
            dic_df_met_ue_d_all = [nested_dic_df['met_ue_d'], nested_dic_df1['met_ue_d']]

        dic_df, dic_df_met_u, dic_df_met_d, dic_df_met_ue_u, dic_df_met_ue_d = [{} for _ in range(5)]

        for key in dic_df_all[0]:
            list_raw, list_met_u, list_met_d, list_met_ue_u, list_met_ue_d = [[] for _ in range(5)]
            for i in range(len(dic_df_all)):
                try:
                    list_raw.append(dic_df_all[i][key])
                    list_met_u.append(dic_df_met_u_all[i][key])
                    list_met_d.append(dic_df_met_d_all[i][key])            
                    list_met_ue_u.append(dic_df_met_ue_u_all[i][key])
                    list_met_ue_d.append(dic_df_met_ue_d_all[i][key])
                except:
                    print("missing:", key)
            dic_df[key]=pd.concat(list_raw, ignore_index=True)
            dic_df_met_u[key]=pd.concat(list_met_u, ignore_index=True)
            dic_df_met_d[key]=pd.concat(list_met_d, ignore_index=True)
            dic_df_met_ue_u[key]=pd.concat(list_met_ue_u, ignore_index=True)
            dic_df_met_ue_d[key]=pd.concat(list_met_ue_d, ignore_index=True)

        dic_df_all.clear()    
        dic_df_met_u_all.clear()    
        dic_df_met_d_all.clear()    
        dic_df_met_ue_u_all.clear()    
        dic_df_met_ue_d_all.clear() 

        dic_df_raw=dic_df
        dic_nested_shape_sys={}
        dic_nested_shape_sys["met_u"]=dic_df_met_u
        dic_nested_shape_sys["met_d"]=dic_df_met_d    
        dic_nested_shape_sys["met_ue_u"]=dic_df_met_ue_u
        dic_nested_shape_sys["met_ue_d"]=dic_df_met_ue_d 

    elif region == "SR":
        if "16" in ERA:
            with open(INPUTDIR+'/'+ERA+'pre/nested_dic_df_SR1.pkl', 'rb') as f:
                nested_dic_df = pickle.load(f)
            with open(INPUTDIR+'/'+ERA+'post/nested_dic_df_SR1.pkl', 'rb') as f:
                nested_dic_df1 = pickle.load(f)
            dic_df_all = [nested_dic_df['raw'], nested_dic_df1['raw']]
            dic_df_met_u_all = [nested_dic_df['met_u'], nested_dic_df1['met_u']]
            dic_df_met_d_all = [nested_dic_df['met_d'], nested_dic_df1['met_d']]    
            dic_df_met_ue_u_all = [nested_dic_df['met_ue_u'], nested_dic_df1['met_ue_u']]
            dic_df_met_ue_d_all = [nested_dic_df['met_ue_d'], nested_dic_df1['met_ue_d']]
        else:
            with open(INPUTDIR+'/'+ERA+'/nested_dic_df_SR1.pkl', 'rb') as f:
                nested_dic_df = pickle.load(f)   
            dic_df=nested_dic_df['raw']
            dic_df_met_u=nested_dic_df['met_u']
            dic_df_met_d=nested_dic_df['met_d'] 
            dic_df_met_ue_u=nested_dic_df['met_ue_u']
            dic_df_met_ue_d=nested_dic_df['met_ue_d']  

        if "16" in ERA:
            dic_df, dic_df_met_u, dic_df_met_d, dic_df_met_ue_u, dic_df_met_ue_d = [{} for _ in range(5)]

            for key in dic_df_all[0]:
                list_raw, list_met_u, list_met_d, list_met_ue_u, list_met_ue_d = [[] for _ in range(5)]
                for i in range(len(dic_df_all)):
                    try:
                        list_raw.append(dic_df_all[i][key])
                        list_met_u.append(dic_df_met_u_all[i][key])
                        list_met_d.append(dic_df_met_d_all[i][key])            
                        list_met_ue_u.append(dic_df_met_ue_u_all[i][key])
                        list_met_ue_d.append(dic_df_met_ue_d_all[i][key])
                    except:
                        print("missing:", key)
                dic_df[key]=pd.concat(list_raw, ignore_index=True)
                dic_df_met_u[key]=pd.concat(list_met_u, ignore_index=True)
                dic_df_met_d[key]=pd.concat(list_met_d, ignore_index=True)
                dic_df_met_ue_u[key]=pd.concat(list_met_ue_u, ignore_index=True)
                dic_df_met_ue_d[key]=pd.concat(list_met_ue_d, ignore_index=True)

            dic_df_all.clear()    
            dic_df_met_u_all.clear()    
            dic_df_met_d_all.clear()    
            dic_df_met_ue_u_all.clear()    
            dic_df_met_ue_d_all.clear() 

    elif region == "VR":
        if "16" in ERA:
            with open(INPUTDIR+'/'+ERA+'pre/nested_dic_df_TTCR.pkl', 'rb') as f:
                nested_dic_df = pickle.load(f)
            with open(INPUTDIR+'/'+ERA+'post/nested_dic_df_TTCR.pkl', 'rb') as f:
                nested_dic_df1 = pickle.load(f)
            dic_df_all = [nested_dic_df['raw'], nested_dic_df1['raw']]
            dic_df_met_u_all = [nested_dic_df['met_u'], nested_dic_df1['met_u']]
            dic_df_met_d_all = [nested_dic_df['met_d'], nested_dic_df1['met_d']]    
            dic_df_met_ue_u_all = [nested_dic_df['met_ue_u'], nested_dic_df1['met_ue_u']]
            dic_df_met_ue_d_all = [nested_dic_df['met_ue_d'], nested_dic_df1['met_ue_d']]
        else:
            with open(INPUTDIR+'/'+ERA+'/nested_dic_df_TTCR.pkl', 'rb') as f:
                nested_dic_df = pickle.load(f)   
            dic_df=nested_dic_df['raw']
            dic_df_met_u=nested_dic_df['met_u']
            dic_df_met_d=nested_dic_df['met_d'] 
            dic_df_met_ue_u=nested_dic_df['met_ue_u']
            dic_df_met_ue_d=nested_dic_df['met_ue_d']  

        if "16" in ERA:
            dic_df, dic_df_met_u, dic_df_met_d, dic_df_met_ue_u, dic_df_met_ue_d = [{} for _ in range(5)]

            for key in dic_df_all[0]:
                list_raw, list_met_u, list_met_d, list_met_ue_u, list_met_ue_d = [[] for _ in range(5)]
                for i in range(len(dic_df_all)):
                    try:
                        list_raw.append(dic_df_all[i][key])
                        list_met_u.append(dic_df_met_u_all[i][key])
                        list_met_d.append(dic_df_met_d_all[i][key])            
                        list_met_ue_u.append(dic_df_met_ue_u_all[i][key])
                        list_met_ue_d.append(dic_df_met_ue_d_all[i][key])
                    except:
                        print("missing:", key)
                dic_df[key]=pd.concat(list_raw, ignore_index=True)
                dic_df_met_u[key]=pd.concat(list_met_u, ignore_index=True)
                dic_df_met_d[key]=pd.concat(list_met_d, ignore_index=True)
                dic_df_met_ue_u[key]=pd.concat(list_met_ue_u, ignore_index=True)
                dic_df_met_ue_d[key]=pd.concat(list_met_ue_d, ignore_index=True)

            dic_df_all.clear()    
            dic_df_met_u_all.clear()    
            dic_df_met_d_all.clear()    
            dic_df_met_ue_u_all.clear()    
            dic_df_met_ue_d_all.clear() 
    else:
        print("WARNING: check if REGION valid")


    dic_df_raw=dic_df
    dic_nested_shape_sys={}
    dic_nested_shape_sys["met_u"]=dic_df_met_u
    dic_nested_shape_sys["met_d"]=dic_df_met_d    
    dic_nested_shape_sys["met_ue_u"]=dic_df_met_ue_u
    dic_nested_shape_sys["met_ue_d"]=dic_df_met_ue_d 

    return dic_df_raw, dic_nested_shape_sys