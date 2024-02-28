import math
import os, sys
sys.path.append('./Utils')
from Plotter import HistStack
import numpy as np


def get_sys_list():
    # return ["scale", "puweight", "effrecoSF", "effSF", "topSF", "met", "metjer", "metue", "hdamp", "PS", "btagSF", "jes", "jer"]
    return ["scale", "puweight", "effrecoSF", "l1prefiring", "effSF", "topSF", "met", "metjer", "metue", "trigSF", "hdamp", "PS", "btagSF", "jes", "jer"]
	# return ["met", "metjer", "metue", "jes", "jer"]
    
def get_dic_sys(model_mass, ERA, dic_df_raw, dic_nested_shape_sys, sys_list, variable, r, region, threshold, file_prefix, file_str):
    """
        draw histograms with sys variations, return sys uncertainty dic
    """
    dic_sys = {}
    dic_sys_sqr = {}
    # nominal weight plot
    # file_prefix = "Outputs/DNN/"+REGION
    hist=HistStack(dic_df_raw, variable, 'weight', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/norm_"+file_str)     
    dic_yields = hist.get_yields_by_bin()
    bkg_norm = dic_yields['bkg']
    if "score" in variable:
	    hist.create_root_file(file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
	    hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
    
    for s in sys_list:
        if "met" in s or "scale" in s or "jes" in s or "jer" in s or "btag" in s: # fill later
            continue
        # up
        hist=HistStack(dic_df_raw, variable, 'weight'+s+'Up', r[0], r[1], r[2], r[3])            
        c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systUp_"+s+file_str, blind_from=threshold)     
        dic_yields = hist.get_yields_by_bin()
        sysUp = dic_yields['bkg']
        dic_sys[s+'Up'] = np.array(sysUp) - np.array(bkg_norm)
        if "score" in variable:
        	hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
        # down
        hist=HistStack(dic_df_raw, variable, 'weight'+s+'Down', r[0], r[1], r[2], r[3])            
        c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systDown_"+s+file_str, blind_from=threshold)     
        dic_yields = hist.get_yields_by_bin()
        sysDown = dic_yields['bkg']
        dic_sys[s+'Down'] = np.array(sysDown) - np.array(bkg_norm)
        if "score" in variable:
        	hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)

    # btag
    btag_sys = ['btagSFbc', 'btagSFbc_correlated', 'btagSFlight', 'btagSFlight_correlated']
    for bsys in btag_sys:
        # up
        hist=HistStack(dic_df_raw, variable, 'weight'+bsys+'Up', r[0], r[1], r[2], r[3])            
        c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systUp_"+bsys+file_str, blind_from=threshold)     
        dic_yields = hist.get_yields_by_bin()
        sysUp = dic_yields['bkg']
        dic_sys[bsys+'Up'] = np.array(sysUp) - np.array(bkg_norm)
        if "score" in variable:
            hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
        # down
        hist=HistStack(dic_df_raw, variable, 'weight'+bsys+'Down', r[0], r[1], r[2], r[3])            
        c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systDown_"+bsys+file_str, blind_from=threshold)     
        dic_yields = hist.get_yields_by_bin()
        sysDown = dic_yields['bkg']
        dic_sys[bsys+'Down'] = np.array(sysDown) - np.array(bkg_norm)
        if "score" in variable:
            hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)    

    # shape sys
    hist=HistStack(dic_nested_shape_sys['met_u'], variable, 'weightmetUp', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systUp_met"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['metUp'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
    	hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
    hist=HistStack(dic_nested_shape_sys['met_d'], variable, 'weightmetDown', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systDown_met"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['metDown'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
    	hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)

    hist=HistStack(dic_nested_shape_sys['jes_u'], variable, 'weightJECUp', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systUp_jes"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['jesUp'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
        hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
    hist=HistStack(dic_nested_shape_sys['jes_d'], variable, 'weightJECDown', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systDown_jes"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['jesDown'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
        hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)

    hist=HistStack(dic_nested_shape_sys['jer_u'], variable, 'weightJERUp', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systUp_jer"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['jerUp'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
        hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
    hist=HistStack(dic_nested_shape_sys['jer_d'], variable, 'weightJERDown', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systDown_jer"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['jerDown'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
        hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)

    hist=HistStack(dic_nested_shape_sys['met_jer_u'], variable, 'weightmetjerUp', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systUp_metjer"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['metjerUp'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
        hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
    hist=HistStack(dic_nested_shape_sys['met_jer_d'], variable, 'weightmetjerDown', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systDown_metjer"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['metjerDown'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
        hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
        
    hist=HistStack(dic_nested_shape_sys['met_ue_u'], variable, 'weightmetueUp', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systUp_metue"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['metueUp'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
    	hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
    hist=HistStack(dic_nested_shape_sys['met_ue_d'], variable, 'weightmetueDown', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systDown_metue"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['metueDown'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
    	hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
    hist=HistStack(dic_nested_shape_sys['scale_u'], variable, 'weightscaleUp', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systUp_scale"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['scaleUp'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
        hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)
    hist=HistStack(dic_nested_shape_sys['scale_d'], variable, 'weightscaleDown', r[0], r[1], r[2], r[3])            
    c1=hist.draw_hist(model_mass, ERA, file_name=file_prefix+"/sys/systDown_scale"+file_str, blind_from=threshold)     
    dic_yields = hist.get_yields_by_bin()
    sysUp = dic_yields['bkg']
    dic_sys['scaleDown'] = np.array(sysUp) - np.array(bkg_norm)
    if "score" in variable:
        hist.export_hist(model_mass, file_name=file_prefix+"/root_files/shape_v1_"+file_str+model_mass)

    # si^2
    sys_list_new = sys_list + btag_sys
    sys_list_new.remove('btagSF')
    for s in sys_list_new:
        # by source
        sqrUp = [x*x if x>0 else -x*x for x in dic_sys[s+'Up']]
        sqrUp_up = [x if x>0 else 0 for x in sqrUp]
        sqrUp_down = [x if x<0 else 0 for x in sqrUp]
        sqrDown = [x*x if x>0 else -x*x for x in dic_sys[s+'Down']]
        sqrDown_up = [x if x>0 else 0 for x in sqrDown]
        sqrDown_down = [x if x<0 else 0 for x in sqrDown]
        
        sqr_up = np.array(sqrUp_up) + np.array(sqrDown_up)
        sqr_down = np.array(sqrUp_down) + np.array(sqrDown_down)
        
        dic_sys_sqr[s+'Up'] = sqr_up
        dic_sys_sqr[s+'Down'] = np.fabs(sqr_down) #store absolute
        
    print(dic_sys)
    print(dic_sys_sqr)
    # sqrt(sumi si^2)
    for i, s in enumerate(sys_list_new):
        if i==0:
            sum_up = dic_sys_sqr[s+'Up'].copy() # be carefull not to use shallow copy
            sum_down = dic_sys_sqr[s+'Down'].copy()
        else:
            sum_up += dic_sys_sqr[s+'Up']
            sum_down += dic_sys_sqr[s+'Down']

    dic_sys_sqr['sum_up'] = np.sqrt(sum_up)
#     print(sum_up)
#     print(sum_down)
    dic_sys_sqr['sum_down'] = np.sqrt(sum_down)
    print(dic_sys_sqr)
            
    return dic_sys_sqr