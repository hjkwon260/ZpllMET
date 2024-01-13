import ROOT as rt
import numpy as np
from collections import defaultdict
import math
from array import array

class HistStack(object):    
    """draw stacked histogram"""    
    def __init__(self, dic_df, variable, weight, nbin, xl, xh, xtitle="DNN Score", dic_sys=None):
        self.dic_df = dic_df
        self.variable = variable
        self.weight = weight
        self.nbin = nbin
        self.xl = xl
        self.xh = xh
        self.hist_all={}
        self.merged_hist={}
        self.h_bkg=None
        self.xtitle= xtitle
        self.option = ""
        self.str_sig = ""
        self.yeilds={}
        self.dic_sys=dic_sys       
        self.era=None   
        self.sig_key=None
        self.stat_unc=None

    def get_dic_hist(self):
        for k, df in self.dic_df.items():
            h = rt.TH1D("", "",  self.nbin, self.xl, self.xh)
            h.Sumw2()
            for i, v in enumerate(df[self.variable]): 
                h.Fill(v, df[self.weight].iat[i])
            # overflow
            h.SetBinContent(h.GetNbinsX(),h.GetBinContent(h.GetNbinsX())+h.GetBinContent(h.GetNbinsX()+1))
            self.hist_all[k]=h
        return self.hist_all
    
    def get_merged_hist(self):
        hist_all=self.get_dic_hist()
        for key in hist_all:
            if "top" in key:
                if 'h_tw' in locals():
                    h_tw.Add(hist_all[key])
                else:
                    h_tw=hist_all[key].Clone("")
            if "DY" in key:
                if 'h_dy' in locals():
                    h_dy.Add(hist_all[key])
                else:
                    h_dy=hist_all[key].Clone("")
            if key=="TT" or key=="TTSemi":
            # if key=="TT":
                if 'h_tt' in locals():
                    h_tt.Add(hist_all[key])
                else:
                    h_tt=hist_all[key].Clone("")
            if key=="TThdampUp" or key=="TTSemi":
                if 'h_tthdampup' in locals():
                    h_tthdampup.Add(hist_all[key])
                else:
                    h_tthdampup=hist_all[key].Clone("")
            if key=="TThdampDown" or key=="TTSemi":
                if 'h_tthdampdown' in locals():
                    h_tthdampdown.Add(hist_all[key])
                else:
                    h_tthdampdown=hist_all[key].Clone("")
            if key=="TTUp" or key=="TTSemi":
                if 'h_ttup' in locals():
                    h_ttup.Add(hist_all[key])
                else:
                    h_ttup=hist_all[key].Clone("")                    
            if key=="TTDown" or key=="TTSemi":
                if 'h_ttdown' in locals():
                    h_ttdown.Add(hist_all[key])
                else:
                    h_ttdown=hist_all[key].Clone("")            
            if key=="WZ" or key=="WZQQ":
                if 'h_wz' in locals():
                    h_wz.Add(hist_all[key])
                else:
                    h_wz=hist_all[key].Clone("")
            if key=="TTZ" or key=="WWW" or key=="WWZ" or key=="H" or key=="HWW":
                if 'h_others' in locals():
                    h_others.Add(hist_all[key])
                else:
                    h_others=hist_all[key].Clone("")
        # self.merged_hist['WWW']=hist_all["WWW"].Clone("")   
        # self.merged_hist['WWZ']=hist_all["WWZ"].Clone("")   
        # self.merged_hist['H']=hist_all["H"].Clone("")   
        # self.merged_hist['HWW']=hist_all["HWW"].Clone("")   
        self.merged_hist['Others']=h_others
        # self.merged_hist['TTZ']=hist_all["TTZ"].Clone("")   
        self.merged_hist['ZZ']=hist_all["ZZ"].Clone("")
        self.merged_hist['WZ']=h_wz
        self.merged_hist['WW']=hist_all["WW"].Clone("")
        if 'h_tw' in locals():
            self.merged_hist['TW']=h_tw
        # self.merged_hist['TTSemi']=hist_all["TTSemi"].Clone("")               
        if 'h_tt' in locals():
            self.merged_hist['TT']=h_tt 
        if 'h_tthdampup' in locals():
            self.merged_hist['TThdampUp']=h_tthdampup
        if 'h_tthdampdown' in locals():
            self.merged_hist['TThdampDown']=h_tthdampdown
        if 'h_ttup' in locals():
            self.merged_hist['TTUp']=h_ttup            
        if 'h_ttdown' in locals():
            self.merged_hist['TTDown']=h_ttdown   
        if 'h_dy' in locals():
            self.merged_hist['DY']=h_dy               
        return self.merged_hist
    
    def set_pad(self, loc, xl, yl, xh, yh):
        p = rt.TPad("pad", "", xl, yl, xh, yh)    
        p.SetLeftMargin(0.12)
        p.SetRightMargin(0.05)
        p.SetTicky() 
        p.SetGrid()
        if loc=="top":
            p.SetLogy()
            p.SetBottomMargin(0.01)
        else:
            p.SetTopMargin(0.01)         
            p.SetBottomMargin(0.3)            
        return p
    
    def set_legend(self, xl, yl, xh, yh):
        l = rt.TLegend(xl, yl, xh, yh)
        l.SetBorderSize(0)
        return l
    
    def get_ratio(self, num):
        h = self.hist_all[num].Clone("")
        h.Divide(self.h_bkg)
        if num=="Data":
            h.SetMarkerStyle(8)
            h.GetYaxis().SetRangeUser(0.4, 1.8)
            h.GetYaxis().SetTitle("Data/MC")
        else:
            h.SetLineColor(2)
            h.SetLineWidth(3)
            h.GetYaxis().SetRangeUser(0.0, h.GetMaximum()*1.1)
            h.GetYaxis().SetTitle("S/B")
        h.GetXaxis().SetLabelSize(0.08)
        h.GetYaxis().SetLabelSize(0.07)   
        h.GetXaxis().SetTitleOffset(0.8)       
        h.GetYaxis().SetTitleOffset(0.3)
        h.GetXaxis().SetTitle(self.xtitle)
        h.SetTitleSize(0.15,"y")
        h.SetTitleSize(0.15,"x")          
        return h   
    
    def get_significance(self, sig_key):
        yields=defaultdict(list)
        for nb in range(self.nbin):
            yields["bkg"].append(self.h_bkg.GetBinContent(nb+1))
        #sigs
        for key2 in self.hist_all:
            if "Zp-" in key2:
                for nb in range(self.nbin):
                    yields[key2].append(self.hist_all[key2].GetBinContent(nb+1))  
                    
#         yields = self.get_yields_by_bin() # problem, why?
        s = yields[sig_key]
        b = yields['bkg'] 

        q = []
        for j in range(len(s)):
            if b[j]==0: #temp
                continue
            q_j = 2*((s[j]+b[j])*math.log((s[j]+b[j])/b[j])-s[j])
            q.append(q_j)
        z = np.sqrt(np.array(q)) 
        
        h = rt.TH1D("", "",  self.nbin, self.xl, self.xh)
        for i in range(self.nbin):
            h.Fill(i/self.nbin, z[i])
        h.SetLineWidth(3)
        h.GetYaxis().SetTitle("Z_{A}")
        h.GetXaxis().SetLabelSize(0.08)
        h.GetYaxis().SetLabelSize(0.07)   
        h.GetXaxis().SetTitleOffset(0.8)       
        h.GetYaxis().SetTitleOffset(0.35)
        h.GetXaxis().SetTitle(self.xtitle)
        h.SetTitleSize(0.12,"y")
        h.SetTitleSize(0.15,"x")             
        return h

    def get_str_lumi_channel(self, era):
        if("mm" in era):
            str_channel="#mu#mu"          
        if("ee" in era):
            str_channel="ee"               
        if("em" in era):
            str_channel="e#mu"
        if "16" in era:
            str_lumi="37.33"
        if "16pre" in era:
            str_lumi="19.52" 
        if "16post" in era:
            str_lumi="16.81"                 
        if "17" in era:
            str_lumi="41.48"
        if "18" in era:
            str_lumi="59.83"
        return str_channel, str_lumi

    def get_stat_sys_err(self):
        '''
            dependency: self.h_bkg in draw_hist()
            return: list of TGraphAsymmErrors, legends. 0: stat, 1: stat+s, ...
                sumi(si^2/n^2)/(tot/n)
        '''  
        
        list_graphs = []
        list_legends = []
        
        xl=np.ones(self.nbin)*self.h_bkg.GetBinWidth(1)/2          
        xh=np.ones(self.nbin)*self.h_bkg.GetBinWidth(1)/2            
        
        x_cen, y_cen, stat_unc = ([] for i in range(3))
        for i in range(self.nbin):
            x_cen.append(self.h_bkg.GetXaxis().GetBinCenter(i+1))
            y_cen.append(self.h_bkg.GetBinContent(i+1))
            stat_unc.append(self.h_bkg.GetBinError(i+1))
        gberr = rt.TGraphAsymmErrors(self.nbin, np.array(x_cen), np.array(y_cen), xl, xh, np.array(stat_unc), np.array(stat_unc))
        gberr.SetLineWidth(0)
        gberr.SetLineColor(0)        
        gberr.SetFillColor(14)
        gberr.SetFillStyle(3001) 
        
        self.stat_unc = stat_unc
        stat_unc2 = np.array(stat_unc)*np.array(stat_unc)       
 
        n = np.array(y_cen)
        stat_rel = np.divide(stat_unc2, n*n, out=np.zeros(n.shape, dtype=float), where=n!=0)


        if self.dic_sys:

            totsys_up = np.sqrt(self.dic_sys['sum_up']*self.dic_sys['sum_up'] + stat_unc2)
            totsys_down = np.sqrt(self.dic_sys['sum_down']*self.dic_sys['sum_down'] + stat_unc2)
            
            totsys_up = np.divide(totsys_up, n, out=np.zeros(n.shape, dtype=float), where=n!=0)
            totsys_down = np.divide(totsys_down, n, out=np.zeros(n.shape, dtype=float), where=n!=0)

            sys_comb_up = stat_rel.copy()
            sys_comb_down = stat_rel.copy()

            sys_up = np.divide(sys_comb_up, totsys_up, out=np.zeros(totsys_up.shape, dtype=float), where=totsys_up!=0)
            sys_down = np.divide(sys_comb_down, totsys_down, out=np.zeros(totsys_down.shape, dtype=float), where=totsys_down!=0)

            gerr = rt.TGraphAsymmErrors(self.nbin, np.array(x_cen), np.ones(self.nbin), xl, xh, sys_down, sys_up)
            gerr.SetLineWidth(0)
            gerr.SetLineColor(0)        
            gerr.SetFillColor(14)
            gerr.SetFillStyle(3001)
            list_graphs.append(gerr)
            list_legends.append('MC stat')              
        
            sys_list = [] 
            for s in self.dic_sys:
                print(s)
                if "Down" in s:
                    sys_list.append(s.rstrip("Down"))
            print(sys_list)        
            for i, s in enumerate(sys_list):
                a = self.dic_sys[s+'Up'].copy()
                a = np.divide(a, n*n, out=np.zeros(a.shape, dtype=float), where=n!=0)
                sys_comb_up += a
                sys_up = np.divide(sys_comb_up, totsys_up, out=np.zeros(totsys_up.shape, dtype=float), where=totsys_up!=0)
                b = self.dic_sys[s+'Down'].copy()
                b = np.divide(b, n*n, out=np.zeros(b.shape, dtype=float), where=n!=0)
                sys_comb_down += b
                sys_down = np.divide(sys_comb_down, totsys_down, out=np.zeros(totsys_down.shape, dtype=float), where=totsys_down!=0)
                
                # gerr = rt.TGraphAsymmErrors(self.nbin, np.array(x_cen), np.ones(self.nbin), xl, xh, sys_up, sys_down) # flipped since MC is denominator
                gerr = rt.TGraphAsymmErrors(self.nbin, np.array(x_cen), np.ones(self.nbin), xl, xh, sys_down, sys_up) # changed 1301
                gerr.SetLineWidth(0)
                gerr.SetLineColor(0)        
                gerr.SetFillColor(i+2)
                if i > 7:
                    gerr.SetFillColor(i-7+2)
                gerr.SetFillStyle(3001)
                list_graphs.append(gerr)
                list_legends.append(str(s))     
        else:
            sqrt_stat_rel = np.sqrt(stat_rel)
            gerr = rt.TGraphAsymmErrors(self.nbin, np.array(x_cen), np.ones(self.nbin), xl, xh, sqrt_stat_rel, sqrt_stat_rel)
            gerr.SetLineWidth(0)
            gerr.SetLineColor(0)        
            gerr.SetFillColor(14)
            gerr.SetFillStyle(3001) 
            list_graphs.append(gerr)
            list_legends.append('MC stat')
        return gberr, list_graphs, list_legends
    
    def draw_hist(self, sig_key, era, file_name, blind_from=1):
        c1 = rt.TCanvas("c1","",800,800)
        c1.cd()
        p1 = self.set_pad("top", 0, 0.3, 1, 1)
        p1.Draw()
        p1.cd()           
        l = self.set_legend(0.55, 0.7, 0.68, 0.89)
        l1 = self.set_legend(0.65, 0.7, 0.92, 0.89)
        rt.gStyle.SetOptStat(0)
        rt.gStyle.SetPalette(rt.kRainBow)

        self.era = era
        self.sig_key = sig_key

        # stack bkgs
        hstack=rt.THStack("","")
        h_bkg=rt.TH1D("", "",  self.nbin, self.xl, self.xh)
        dic_merged=self.get_merged_hist()
        # draw in order of bkg_keys
        if "hdampUp" in self.weight:
            bkg_keys = ['Others', 'ZZ', 'WZ', 'WW', 'TW', 'TThdampUp', 'DY']
        elif "hdampDown" in self.weight:
            bkg_keys = ['Others', 'ZZ', 'WZ', 'WW', 'TW', 'TThdampDown', 'DY']
        elif "PSUp" in self.weight:
            bkg_keys = ['Others', 'ZZ', 'WZ', 'WW', 'TW', 'TTUp', 'DY']
        elif "PSDown" in self.weight:
            bkg_keys = ['Others', 'ZZ', 'WZ', 'WW', 'TW', 'TTDown', 'DY'] 
        else:
            bkg_keys = ['Others', 'ZZ', 'WZ', 'DY', 'WW', 'TW', 'TT']
#             bkg_keys = ['Others', 'ZZ', 'WZ', 'WW', 'TW', 'TT', 'DY']
            # bkg_keys = ['WWW', 'WWZ', 'H', 'HWW', 'TTZ', 'ZZ', 'WZ', 'WW', 'TW', 'TT', 'DY']
            # bkg_keys = ['TTZ', 'ZZ', 'WZ', 'WW', 'TW', 'TTSemi', 'TT', 'DY'] #temp
        for key in bkg_keys:
            hstack.Add(dic_merged[key])
            h_bkg.Add(dic_merged[key])

        self.h_bkg = h_bkg        
        hstack.Draw("pfc hist")
        hstack.SetMaximum(hstack.GetMaximum()*5000) # cannot use SetRangeUser 
#         if is_dnn:
#             hstack.SetMinimum(self.hist_all["Zp-2500_CH-345"].GetMaximum()*0.01)
#         else:
        hstack.SetMinimum(self.hist_all["Zp-3700_CH-1095"].GetMaximum()*0.01)        
        hstack.GetYaxis().SetTitle("Events")
        hstack.GetXaxis().SetTitle("DNN score")
        hstack.GetYaxis().SetTitleSize(0.06)
        hstack.GetYaxis().SetTitleOffset(0.6)   

        for keyr in reversed(bkg_keys):
            l.AddEntry(dic_merged[keyr], keyr, "f")
            
        # draw data
        h_data=self.hist_all["Data"].Clone("")
        if blind_from!=1: # blind
            if blind_from < 0:
                for i in range(self.nbin):
                    threshold = self.nbin*math.fabs(blind_from)
                    if i+1 < threshold:
                        h_data.SetBinContent(i+1, 1e15)                
            else:    
                for i in range(self.nbin):
                    threshold = self.nbin*blind_from
                    if i+1 > threshold:
                        h_data.SetBinContent(i+1, 1e15)
        h_data.Draw("same EP")
        h_data.SetMarkerStyle(8)
        
        gberr, list_graphs, list_legends = self.get_stat_sys_err()
        gberr.Draw("E2 same")    
        
        # draw sig
#         if is_dnn:
        if 'score' in self.variable:
            sig_keys = [sig_key]
        else:
            sig_keys = ["Zp-2500_CH-345", "Zp-3700_CH-345", "Zp-3700_CH-1095"]

        for i, sig in enumerate(sig_keys):
            self.hist_all[sig].Draw("same hist")
            self.hist_all[sig].SetLineColor(2+i)
            self.hist_all[sig].SetLineWidth(3)
            str_sig=sig.replace("_narrow", "")
            str_sig=str_sig.replace("Zp-", "m(Z')=")
            str_sig=str_sig.replace("_CH-", ", m(#chi^{#pm})=")  
            l1.AddEntry(self.hist_all[sig], str_sig, "l")
        l.Draw()
        l1.AddEntry(h_data, "data", "p")
        l1.Draw()
        
        str_channel, str_lumi = self.get_str_lumi_channel(era)
        latex1=rt.TLatex()
        latex1.DrawLatexNDC(0.71, 0.92, "#font[42]{#scale[0.8]{"+str_lumi+" fb^{-1}(13 TeV)}}");
        latex1.DrawLatexNDC(0.13, 0.92, "#font[62]{CMS}#font[42]{#it{#scale[0.8]{ Preliminary}}}");
        latex1.DrawLatexNDC(0.15,0.85, "#scale[0.8]{#font[42]{"+str_channel+" channel}}") 
                
        # draw Data/MC
        c1.cd()
        p2 = self.set_pad("bottom", 0, 0, 1, 0.3)
        p2.Draw()
        p2.cd()  
        
        h_ratio = self.get_ratio("Data")
        
        if "score" in self.variable:
            h_ratio1 = self.get_significance(sig_key)        

        l2 = self.set_legend(0.75, 0.9, 0.92, 0.99)

#         if not "score" in self.variable or blind_from==1: 
        h_ratio.Draw()
        # sys
        if self.dic_sys:
            for i in reversed(range(len(list_graphs)-1)):
                gr = list_graphs[i+1].Clone("")
                gr.Draw("E2 same")
                l2.AddEntry(list_graphs[i+1], list_legends[i+1], "f")                

            # stat
            list_graphs[0].Draw("E2 same")
            l2.AddEntry(list_graphs[0], list_legends[0], "f")
        
        if blind_from!=1: # blind
            if blind_from < 0:
                for i in range(self.nbin):
                    threshold = self.nbin*math.fabs(blind_from)
                    if i+1 < threshold:
                        h_ratio.SetBinContent(i+1, 1e15) 
            else:         
                for i in range(self.nbin):
                    threshold = self.nbin*blind_from
                    if i+1 > threshold:
                        h_ratio.SetBinContent(i+1, 1e15) 
#         if "score" in self.variable and blind_from!=1:
#             h_ratio.Draw("same hist")
#             h_ratio.SetLineWidth(2)
#         else:
        h_ratio.Draw("same")

#         if not "score" in self.variable or blind_from==1:        
        l2.Draw()      
        c1.SaveAs(file_name+"_"+self.variable+"breakdown.pdf")
#         if not is_dnn:
#             c1.SaveAs(file_name+"_"+self.variable+".png")

        c1.cd()
#         p2.Clear()
        p2 = self.set_pad("bottom", 0, 0, 1, 0.3)
        p2.Draw()
        p2.cd()
#         h_ratio.Draw()
        l3 = self.set_legend(0.75, 0.9, 0.92, 0.99)
        
#         if not "score" in self.variable or blind_from==1: 
        h_ratio.Draw()
        # sys
        if self.dic_sys:
            for i in reversed(range(len(list_graphs)-1)):
                gr = list_graphs[i+1].Clone("")
                gr.Draw("E2 same")                
                gr.SetFillColor(3)
            l3.AddEntry(list_graphs[2], "tot. sys.", "f")
        # stat
        list_graphs[0].Draw("E2 same")
        l3.AddEntry(list_graphs[0], list_legends[0], "f")
        
        if blind_from!=1: # blind
            if blind_from < 0:
                for i in range(self.nbin):
                    threshold = self.nbin*math.fabs(blind_from)
                    if i+1 < threshold:
                        h_ratio.SetBinContent(i+1, 1e15)        
            else:         
                for i in range(self.nbin):
                    threshold = self.nbin*blind_from
                    if i+1 > threshold:
                        h_ratio.SetBinContent(i+1, 1e15)        
#         if "score" in self.variable and blind_from!=1:
#             h_ratio.Draw("same hist")
#             h_ratio.SetLineWidth(2)
#         else:
        h_ratio.Draw("same")        

#         if not "score" in self.variable or blind_from==1:                       
        l3.Draw("same")
        c1.SaveAs(file_name+"_"+self.variable+".pdf") 
        
        if "score" in self.variable:
            c1.cd()
    #         p2.Clear()
            p2 = self.set_pad("bottom", 0, 0, 1, 0.3)
            p2.Draw()
            p2.cd()
            h_ratio1.Draw("same hist")
            h_ratio1.SetLineWidth(2)
            c1.SaveAs(file_name+"_sign_"+self.variable+".pdf")
        return c1     

    def get_yeilds(self):
        yeilds={}
        #bkgs
        dic_merged=self.merged_hist #dependency: draw_hist()
        for key in dic_merged:
            yeilds[key]=dic_merged[key].Integral(0,self.nbin) # nbin=nth+overflow
        #sigs, Data
        for key2 in self.hist_all:
            if "Zp-2500_CH-345" in key2:
                yeilds[key2]=self.hist_all[key2].Integral(0,self.nbin)  
            if key2=="Data":
                yeilds[key2]=self.hist_all[key2].Integral(0,self.nbin) 
        self.yeilds=yeilds
        return yeilds
    
    def get_yields_by_bin(self):
        yields=defaultdict(list)
        #bkgs
        dic_merged=self.get_merged_hist()
        for key in dic_merged:
            for nb in range(self.nbin):
                yields[key].append(dic_merged[key].GetBinContent(nb+1))  
        for nb in range(self.nbin):
            yields["bkg"].append(self.h_bkg.GetBinContent(nb+1))
        #sigs
        for key2 in self.hist_all:
            if "Zp-" in key2:
                for nb in range(self.nbin):
                    yields[key2].append(self.hist_all[key2].GetBinContent(nb+1))        
        return yields
        
    
    def draw_pie(self, file_name):
        """
            depandancy: get_yields()
        """
        list_yeild=[]
        for key in self.yeilds:
            if key!="Data" and not "Up" in key and not "Down" in key:
                list_yeild.append(self.yeilds[key])

        arr_yeilds = array('f', list_yeild)
        arr_colors = array('i', [1,207,208,209,225,226,227,2,3])
        nvals=len(arr_yeilds)
        print(arr_yeilds)
        cpie=rt.TCanvas("cpie","et",700,700)
        cpie.cd()
        p1=rt.TPad("pad","",0,0.3,0.5,1)
        p1.Draw()
        p1.cd()        
        pie=rt.TPie("pie","Yeilds",nvals,arr_yeilds,arr_colors)
        pie.Draw()
        print("test")
        
        i=0
        for key in self.yeilds:
            if key!="Data":
                pie.SetEntryLabel(i, key)
                i+=1
        pie.SetRadius(.2)

        latex=rt.TLatex()
        latex.DrawLatexNDC( 0.2,0.82, "# Data: "+str(self.yeilds["Data"]))
        latex.DrawLatexNDC( 0.2,0.77, "# Total bkg: "+str(round( (sum(list_yeild)-list_yeild[-1]),2 )))
        soverb=float("{:.5f}".format(list_yeild[-1]/math.sqrt(sum(list_yeild))))
        latex.DrawLatexNDC( 0.2,0.2, "s/#sqrt{b}: "+str(soverb))
        latex.DrawLatexNDC( 0.2,0.17, "TTUp: "+str(round(self.yeilds["TTUp"],2)))
        latex.DrawLatexNDC( 0.2,0.14, "TTDown: "+str(round(self.yeilds["TTDown"],2)))
        latex.DrawLatexNDC( 0.2,0.11, "TThdampUp: "+str(round(self.yeilds["TThdampUp"],2)))
        latex.DrawLatexNDC( 0.2,0.08, "TThdampDown: "+str( round(self.yeilds["TThdampDown"],2)))
        cpie.Draw()
    
        cpie.cd()
        p2=rt.TPad("pad","",0.5,0,1,1)
        p2.Draw()
        p2.cd()    
        #customize legend
        l=rt.TLegend(0.1,0.1,0.9,0.89)
        for j in range(len(list_yeild)):
            l.AddEntry(pie.GetSlice(j), pie.GetSlice(j).GetTitle()+" ("+str(round(list_yeild[j],2))+"), "+str(round( 100*(list_yeild[j]/sum(list_yeild)),2 ))+"%", "f")
        l.Draw()    
        cpie.SaveAs(file_name+"yeilds"+self.variable+"_"+self.option+'.pdf')
        cpie.SaveAs(file_name+"yeilds"+self.variable+"_"+self.option+'.png')    

    def draw_pie_lastbin(self, file_name):
        """
            depandancy: get_yields_by_bin()
        """
        list_yeild=[]
        list_keys=[]
        yields = self.get_yields_by_bin()
        for key in yields:
            if key!="Data" and not "Up" in key and not "Down" in key and not "Zp" in key and not "bkg" in key:
                list_yeild.append(yields[key][19])
                list_keys.append(key)
        
        
        arr_yeilds = array('f', list_yeild)
        arr_colors = array('i', [1,207,208,209,225,226,227,2,3])
        nvals=len(arr_yeilds)
        print(arr_yeilds)
        cpie=rt.TCanvas("cpie","et",700,700)
        cpie.cd()
        p1=rt.TPad("pad","",0,0.3,0.5,1)
        p1.Draw()
        p1.cd()        
        pie=rt.TPie("pie","Yeilds",nvals,arr_yeilds,arr_colors)
        pie.Draw()
        print("test")
        
        i=0
        for key in list_keys:
            if key!="Data":
                pie.SetEntryLabel(i, key)
                i+=1
        pie.SetRadius(.2)

        latex=rt.TLatex()
        latex.DrawLatexNDC( 0.2,0.82, "# Data: "+str(yields["Data"]))
        latex.DrawLatexNDC( 0.2,0.77, "# Total bkg: "+str(yields["bkg"][-1]))
#         soverb=float("{:.5f}".format(list_yeild[-1]/math.sqrt(sum(list_yeild))))
#         latex.DrawLatexNDC( 0.2,0.2, "s/#sqrt{b}: "+str(soverb))
        cpie.Draw()
    
        cpie.cd()
        p2=rt.TPad("pad","",0.5,0,1,1)
        p2.Draw()
        p2.cd()    
        #customize legend
        l=rt.TLegend(0.1,0.1,0.9,0.89)
        for j in range(len(list_yeild)):
            l.AddEntry(pie.GetSlice(j), pie.GetSlice(j).GetTitle()+" ("+str(round(list_yeild[j],2))+"), "+str(round( 100*(list_yeild[j]/sum(list_yeild)),2 ))+"%", "f")
        l.Draw()    
        cpie.SaveAs(file_name+"lastbin_yeilds"+self.variable+"_"+self.option+'.pdf')
        cpie.SaveAs(file_name+"lastbin_yeilds"+self.variable+"_"+self.option+'.png')         
        
        
    def export_yields_table(self, file_name):
        """
            depandancy: get_yields_by_bin()
        """
        with open(file_name+'.txt', 'w') as yf:
            yields = self.get_yields_by_bin()
            
            yf.write(r"\begin{table}[htbp]"+"\n")
            yf.write(r"\centering"+"\n")
            yf.write(r"\caption{caption}"+"\n")
            yf.write(r"\label{tab:label}"+"\n")
            yf.write(r"\begin{tabular}{|c|c|c|c|c|} \hline"+"\n")
            yf.write(r"DNN score bin & bin 16 & bin 17 & bin18 & bin 19 \\ \hline"+"\n")
#             print(yields)
# TT & $0\pm0^{+0}_{-0}$ & $20\pm4^{+14}_{-22}$ & $703\pm26^{+325}_{-257}$ & $1274\pm35^{+588}_{-463}$ \\ DY & $0\pm0^{+0}_{-0}$ & $0\pm0^{+0}_{-0}$ & $112\pm10^{+39}_{-39}$ & $338\pm18^{+42}_{-42}$ \\ TW & $0\pm0^{+0}_{-0}$ & $0\pm0^{+0}_{-0}$ & $203\pm14^{+57}_{-66}$ & $480\pm21^{+133}_{-156}$ \\ VV & $0\pm0^{+0}_{-0}$ & $10\pm3^{+4}_{-7}$ & $533\pm23^{+31}_{-56}$ & $943\pm30^{+39}_{-43}$ \\ \hline            
            nbin = 4
            processes = ['TT', 'TW', 'WW', 'DY', 'bkg', self.sig_key]
            yields_str = ''
            for p in processes: # yields for last 4 bins
#                 yields_str += p+' & $'+str(round(yields[p][16],2))+'\pm'+str(round(self.stat_unc[16],2))+'^{+'+str(round(self.dic_sys['sum_up'][16],2))+'}_{-'+str(round(self.dic_sys['sum_down'][16],2))+'}$'+' & '+str(round(yields[p][17],2))+' & '+str(round(yields[p][18],2))+' & '+str(round(yields[p][19],2))+' \\\\ \n'
                yields_str += p
                for i in range(nbin):
                    yields_str += ' & $'+str(round(yields[p][i+16],2))+'\pm'+str(round(self.stat_unc[i+16],2))+'^{+'+str(round(self.dic_sys['sum_up'][i+16],2))+'}_{-'+str(round(self.dic_sys['sum_down'][i+16],2))+'}$'
                yields_str += ' \\\\ \n'
                
            yf.write(yields_str)
            yf.write(r"\hline"+"\n")
            yf.write(r"\end{tabular}"+"\n")
            yf.write(r"\end{table}"+"\n")
        

    def create_root_file(self, file_name):
        f = rt.TFile(file_name+"_v1.root","RECREATE")
        subdir = f.mkdir("signal_region");
        subdir.cd()
        self.hist_all["Data"].SetName("data_obs")
        self.hist_all["Data"].SetTitle("data_obs")
        self.hist_all["Data"].Write("data_obs",rt.TObject.kWriteDelete)     
        f.Close()  

    def export_hist(self, sig_key, file_name):
        str_sys = self.weight
        str_sys = str_sys.replace("weight", "")
        if str_sys!="":
            str_sys = "_"+str_sys
        f = rt.TFile(file_name+"_v1.root","UPDATE") 
        f.cd("signal_region")

        if "hdampUp" in str_sys:
            TTkey = "TThdampUp"
        elif "hdampDown" in str_sys:
            TTkey = "TThdampDown"
        elif "PSUp" in str_sys:
            TTkey = "TTUp"  
        elif "PSDown" in str_sys:
            TTkey = "TTDown"
        else:
            TTkey = "TT"
        if "PS" in str_sys:
            str_sys = str_sys.replace("PS", "UE")
        if "effSF" in str_sys:
            str_sys = str_sys.replace("effSF", "ll_eff")
        if "trigSF" in str_sys:
            str_sys = str_sys.replace("trigSF", "trig_eff")
        if "topSF" in str_sys:
            str_sys = str_sys.replace("topSF", "toppt")
        if "scale" in str_sys and "e" in self.era:
            self.hist_all["Data"].SetName("data"+str_sys)
            self.hist_all["Data"].SetTitle("data"+str_sys)
            self.hist_all["Data"].Write("data"+str_sys,rt.TObject.kWriteDelete) 

        year = self.era.replace("mm", "")
        year = year.replace("ee", "")
        year = year.replace("em", "")
        if ("btagSFbc" in str_sys or "btagSFlight" in str_sys) and not "correlated" in str_sys:
            str_sys = str_sys.replace("Up", year+"Up")
            str_sys = str_sys.replace("Down", year+"Down")
        self.hist_all[sig_key].SetName("zp"+str_sys)
        self.hist_all[sig_key].SetTitle("zp"+str_sys)
        self.hist_all[sig_key].Write("zp"+str_sys,rt.TObject.kWriteDelete)            
        self.merged_hist[TTkey].SetName("ttbar"+str_sys)
        self.merged_hist[TTkey].SetTitle("ttbar"+str_sys)
        self.merged_hist[TTkey].Write("ttbar"+str_sys,rt.TObject.kWriteDelete)
        self.merged_hist["DY"].SetName("dy"+str_sys)
        self.merged_hist["DY"].SetTitle("dy"+str_sys)
        self.merged_hist["DY"].Write("dy"+str_sys,rt.TObject.kWriteDelete)
        self.merged_hist["WW"].SetName("ww"+str_sys)
        self.merged_hist["WW"].SetTitle("ww"+str_sys)
        self.merged_hist["WW"].Write("ww"+str_sys,rt.TObject.kWriteDelete)
        self.merged_hist["WZ"].SetName("wz"+str_sys)
        self.merged_hist["WZ"].SetTitle("wz"+str_sys)
        self.merged_hist["WZ"].Write("wz"+str_sys,rt.TObject.kWriteDelete)
        self.merged_hist["TW"].SetName("singletop"+str_sys)
        self.merged_hist["TW"].SetTitle("singletop"+str_sys)
        self.merged_hist["TW"].Write("singletop"+str_sys,rt.TObject.kWriteDelete) 
        self.merged_hist["ZZ"].SetName("zz"+str_sys)
        self.merged_hist["ZZ"].SetTitle("zz"+str_sys)
        self.merged_hist["ZZ"].Write("zz"+str_sys,rt.TObject.kWriteDelete)
        # self.merged_hist["TTZ"].SetName("ttz"+str_sys)
        # self.merged_hist["TTZ"].SetTitle("ttz"+str_sys)
        # self.merged_hist["TTZ"].Write("ttz"+str_sys,rt.TObject.kWriteDelete) 
        self.h_bkg.SetName("total_bkg"+str_sys)
        self.h_bkg.SetTitle("total_bkg"+str_sys)
        self.h_bkg.Write("total_bkg"+str_sys,rt.TObject.kWriteDelete)