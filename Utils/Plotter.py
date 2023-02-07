import ROOT as rt
import numpy as np
from collections import defaultdict
import math
from array import array

class HistStack(object):    
    """draw stacked histogram"""
    def __init__(self, dic_df, variable, weight, nbin, xl, xh, xtitle="DNN Score"):
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
            if key=="DY":
                    h_dy=hist_all[key].Clone("")
            if key=="TT" or key=="TTSemi":
                if 'h_tt' in locals():
                    h_tt.Add(hist_all[key])
                else:
                    h_tt=hist_all[key].Clone("")
        self.merged_hist['TTZ']=hist_all["TTZ"].Clone("")   
        self.merged_hist['ZZ']=hist_all["ZZ"].Clone("")
        self.merged_hist['WZ']=hist_all["WZ"].Clone("")
        self.merged_hist['WW']=hist_all["WW"].Clone("")
        if 'h_tw' in locals():
            self.merged_hist['TW']=h_tw
        if 'h_tt' in locals():
            self.merged_hist['TT']=h_tt 
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
            h.GetYaxis().SetRangeUser(0.6, 1.4)
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
    
    def get_str_lumi_channel(self, era):
        if("mm" in era):
            str_channel="#mu#mu"          
        if("ee" in era):
            str_channel="ee"               
        if("em" in era):
            str_channel="e#mu"
        if "16pre" in era:
            str_lumi="19.52" 
        if "16post" in era:
            str_lumi="16.81"                 
        if "17" in era:
            str_lumi="41.48"
        if "18" in era:
            str_lumi="59.83"
        return str_channel, str_lumi

    def get_stat_err(self):
        # dependency: self.h_bkg in draw_hist()
        x_cen,y_cen,stat_u,stat_d,stat_u_ratio,stat_d_ratio=([] for i in range(6))
        
        for i in range(self.nbin):
            x_cen.append(self.h_bkg.GetXaxis().GetBinCenter(i+1))
            y_cen.append(self.h_bkg.GetBinContent(i+1))
            stat_u.append(self.h_bkg.GetBinError(i+1))
            stat_d.append(self.h_bkg.GetBinError(i+1))
            if self.h_bkg.GetBinContent(i+1)!=0:
                stat_u_ratio.append(self.h_bkg.GetBinError(i+1)/self.h_bkg.GetBinContent(i+1))
                stat_d_ratio.append(self.h_bkg.GetBinError(i+1)/self.h_bkg.GetBinContent(i+1))
            else:
                stat_u_ratio.append(0)
                stat_d_ratio.append(0)                
        xl=np.ones(self.nbin)*self.h_bkg.GetBinWidth(1)/2          
        xh=np.ones(self.nbin)*self.h_bkg.GetBinWidth(1)/2                  
        gberr = rt.TGraphAsymmErrors(self.nbin, np.array(x_cen), np.array(y_cen), xl, xh, np.array(stat_u), np.array(stat_d))
        gberr_ratio = rt.TGraphAsymmErrors(self.nbin, np.array(x_cen), np.ones(self.nbin), xl, xh, np.array(stat_u_ratio), np.array(stat_d_ratio))
        gberr.SetLineWidth(0)
        gberr.SetLineColor(0)        
        gberr.SetFillColor(14)
        gberr.SetFillStyle(3001) 
        gberr_ratio.SetLineWidth(0)
        gberr_ratio.SetLineColor(0)        
        gberr_ratio.SetFillColor(14)
        gberr_ratio.SetFillStyle(3001)       
        return gberr, gberr_ratio
    
    def draw_hist(self, sig_key, era, file_name, is_dnn=False):
        c1 = rt.TCanvas("c1","",800,800)
        c1.cd()
        p1 = self.set_pad("top", 0, 0.3, 1, 1)
        p1.Draw()
        p1.cd()           
        l = self.set_legend(0.55, 0.7, 0.68, 0.89)
        l1 = self.set_legend(0.65, 0.7, 0.92, 0.89)
        rt.gStyle.SetOptStat(0)
        rt.gStyle.SetPalette(rt.kRainBow)

        # stack bkgs
        hstack=rt.THStack("","")
        h_bkg=rt.TH1D("", "",  self.nbin, self.xl, self.xh)
        dic_merged=self.get_merged_hist()
        for key in dic_merged:
            hstack.Add(dic_merged[key])
            h_bkg.Add(dic_merged[key])

        self.h_bkg = h_bkg        
        hstack.Draw("pfc hist")
        hstack.SetMaximum(hstack.GetMaximum()*5000) # cannot use SetRangeUser 
        if is_dnn:
            hstack.SetMinimum(self.hist_all["Zp-2500_CH-345"].GetMaximum()*0.01)
        else:
            hstack.SetMinimum(self.hist_all["Zp-3700_CH-1095"].GetMaximum()*0.01)        
        hstack.GetYaxis().SetTitle("Events")
        hstack.GetXaxis().SetTitle("DNN score")
        hstack.GetYaxis().SetTitleSize(0.06)
        hstack.GetYaxis().SetTitleOffset(0.6)   

        for keyr in reversed(dic_merged):
            l.AddEntry(dic_merged[keyr], keyr, "f")
            
        # draw data
        h_data=self.hist_all["Data"].Clone("")
        if is_dnn: # blind
            for i in range(self.nbin):
                # blind threshold: 0.25
                if i > self.nbin/4:
                    h_data.SetBinContent(i+1, 1e15)
        h_data.Draw("same EP")
        h_data.SetMarkerStyle(8)
        
        gberr, gberr_ratio=self.get_stat_err()
        gberr.Draw("E2 same")    
        
        # draw sig
        if is_dnn:
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
        
        if is_dnn:
            h_ratio = self.get_ratio(sig_key)
        else:    
            h_ratio = self.get_ratio("Data")
        
        h_ratio.Draw()        
        gberr_ratio.Draw("E2 same")
        
        l2 = self.set_legend(0.75, 0.9, 0.92, 0.99)
        l2.AddEntry(gberr_ratio, "MC stat. err.", "f")
        l2.Draw()      
        c1.SaveAs(file_name+"_"+self.variable+".pdf")
        if not is_dnn:
            c1.SaveAs(file_name+"_"+self.variable+".png")
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
        list_yeild=[]
        for key in self.yeilds:
            if key!="Data":
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
    
    def get_yeilds_table(self, ):
        with open('yields_table_'+self.str_sig+'.txt', 'a') as yf:
            #bkgs
            dic_merged=self.get_merged_hist()
            yf.write(r"\begin{landscape}"+"\n")
            div=2
            nbin=16
            for i in range(div):
                binning="DNN score bin & "
                ntab="|c|"            
                for nb in range(int(nbin/div)):
#                     print(i*int(nbin/2))
                    ntab+="c|"
                    binning+=str(round(dic_merged["TT"].GetBinLowEdge(i*int(nbin/div)+nb+1+4),2))+"-"+str(round(dic_merged["TT"].GetBinLowEdge(i*int(nbin/div)+nb+2+4),2))
                    if nb==int(nbin/div)-1:
                        binning+=" \\\\ \hline"
                    else:
                        binning+=" & "
                
                yf.write(r"\begin{table}[htbp]"+"\n")
                yf.write(r"\centering"+"\n")
                yf.write(r"\caption{Background samples used in the analysis.}"+"\n")
                yf.write(r"\label{tab:bkg_samples}"+"\n")                        
                yf.write(r"\begin{tabular}{"+ntab+r"} \hline"+"\n")
                yf.write(binning+"\n")
                for key in reversed(dic_merged):
                    yeilds=key+" & "
                    for nb in range(int(nbin/div)):
#                         yeilds+=str(round(dic_merged[key].GetBinContent(i*int(nbin/div)+nb+1+4),1))+"$\pm$"+str(round(dic_merged[key].GetBinError(i*int(nbin/div)+nb+1+4),1))
                        yeilds+=str(round(dic_merged[key].GetBinContent(i*int(nbin/div)+nb+1+4),2))
                        if nb==int(nbin/div)-1:
                            yeilds+=" \\\\ "
                        else:
                            yeilds+=" & "
                    yf.write(yeilds)
                #bkg sum
                yf.write("\hline\n")
                yeilds="Total Bkgs & "
                for nb in range(int(nbin/div)):
#                     yeilds+=str(round(self.h_bkg.GetBinContent(i*int(nbin/div)+nb+1+4),1))+"$\pm$"+str(round(self.h_bkg.GetBinError(i*int(nbin/div)+nb+1+4),1))
                    yeilds+=str(round(self.h_bkg.GetBinContent(i*int(nbin/div)+nb+1+4),2))
                    if nb==int(nbin/div)-1:
                        yeilds+=" \\\\ "
                    else:
                        yeilds+=" & "
                yf.write(yeilds+"\n")
                #sigs
                yf.write("\hline\n")
                for key2 in self.hist_all:
                    if "Zp-" in key2:
                        yeilds=self.str_sig+" & "
                        for nb in range(int(nbin/div)):
#                             yeilds+=str(round(self.hist_all[key2].GetBinContent(i*int(nbin/div)+nb+1+4),1))+"$\pm$"+str(round(self.hist_all[key2].GetBinError(i*int(nbin/div)+nb+1+4),1))
                            yeilds+=str(round(self.hist_all[key2].GetBinContent(i*int(nbin/div)+nb+1+4),2))
                            if nb==int(nbin/div)-1:
                                yeilds+=" \\\\ \hline"
                            else:
                                yeilds+=" & "
                        yf.write(yeilds+"\n")
                yf.write(r"\end{tabular}"+"\n")
                yf.write(r"\end{table}"+"\n")
            yf.write(r"\end{landscape}"+"\n")
            
    def get_yeilds_table_syst(self, sys_tot_u, sys_tot_d, channel):
        with open('./Outputs/'+channel+'/yields_table_width_syst_'+self.str_sig+'.txt', 'a') as yf:
            #bkgs
            dic_merged=self.get_merged_hist()
            div=4
            nbin=16
            yf.write(r"\begin{table}[htbp]"+"\n")
            yf.write(r"\centering"+"\n")
            yf.write(r"\caption{Background samples used in the analysis.}"+"\n")
            yf.write(r"\label{tab:bkg_samples}"+"\n") 
            for i in range(div):
                binning="DNN score bin & "
                ntab="|c|"            
                for nb in range(int(nbin/div)):
#                     print(i*int(nbin/2))
                    ntab+="c|"
                    binning+=str(round(dic_merged["TT"].GetBinLowEdge(i*int(nbin/div)+nb+1+4),2))+"-"+str(round(dic_merged["TT"].GetBinLowEdge(i*int(nbin/div)+nb+2+4),2))
                    if nb==int(nbin/div)-1:
                        binning+=" \\\\ \hline"
                    else:
                        binning+=" & "
                                       
                yf.write(r"\begin{tabular}{"+ntab+r"} \hline"+"\n")
                yf.write(binning+"\n")
                for key in reversed(dic_merged):
                    yeilds=key+" & "
                    for nb in range(int(nbin/div)):
                        yeilds+="$"+str(int(dic_merged[key].GetBinContent(i*int(nbin/div)+nb+1+4)))+"\pm"+str(int(rt.sqrt(dic_merged[key].GetBinContent(i*int(nbin/div)+nb+1+4))))+"^{+"+str(int(sys_tot_u[key][i*int(nbin/div)+nb+4]))+"}_{-"+str(int(sys_tot_d[key][i*int(nbin/div)+nb+4]))+"}$"
#                         yeilds+=str(round(dic_merged[key].GetBinContent(i*int(nbin/div)+nb+1+4),2))
                        if nb==int(nbin/div)-1:
                            yeilds+=" \\\\ "
                        else:
                            yeilds+=" & "
                    yf.write(yeilds)
                #bkg sum
                yf.write("\hline\n")
                yeilds="Total Bkgs & "
                for nb in range(int(nbin/div)):
#                     yeilds+=str(round(self.h_bkg.GetBinContent(i*int(nbin/div)+nb+1+4),1))+"$\pm$"+str(round(self.h_bkg.GetBinError(i*int(nbin/div)+nb+1+4),1))
                    yeilds+="$"+str(int(self.h_bkg.GetBinContent(i*int(nbin/div)+nb+1+4)))+"\pm"+str(int(rt.sqrt(self.h_bkg.GetBinContent(i*int(nbin/div)+nb+1+4))))+"^{+"+str(int(sys_tot_u["bkg"][i*int(nbin/div)+nb+4]))+"}_{-"+str(int(sys_tot_d["bkg"][i*int(nbin/div)+nb+4]))+"}$"
                    if nb==int(nbin/div)-1:
                        yeilds+=" \\\\ "
                    else:
                        yeilds+=" & "
                yf.write(yeilds+"\n")
                #sigs
                yf.write("\hline\n")
                for key2 in self.hist_all:
                    if "Zp-" in key2:
                        yeilds="$"+self.str_sig.replace("#", "\\")+"$ & "
                        for nb in range(int(nbin/div)):
#                             yeilds+=str(round(self.hist_all[key2].GetBinContent(i*int(nbin/div)+nb+1+4),1))+"$\pm$"+str(round(self.hist_all[key2].GetBinError(i*int(nbin/div)+nb+1+4),1))
                            yeilds+="$"+str(int(self.hist_all[key2].GetBinContent(i*int(nbin/div)+nb+1+4)))+"\pm"+str(int(rt.sqrt(self.hist_all[key2].GetBinContent(i*int(nbin/div)+nb+1+4))))+"^{+"+str(int(sys_tot_u[key2][i*int(nbin/div)+nb+4]))+"}_{-"+str(int(sys_tot_d[key2][i*int(nbin/div)+nb+4]))+"}$"
                            if nb==int(nbin/div)-1:
                                yeilds+=" \\\\ \hline"
                            else:
                                yeilds+=" & "
                        yf.write(yeilds+"\n")
                yf.write(r"\end{tabular}"+"\n")
            yf.write(r"\end{table}"+"\n")
            
    def create_root_file(self, sig_key, nclass, channel):
        f = rt.TFile("./Outputs/"+channel+"/shape_"+sig_key+"_"+str(nclass)+".root","RECREATE")
        subdir = f.mkdir("signal_region");
        subdir.cd()
        self.hist_all["Data"].SetName("data_obs")
        self.hist_all["Data"].SetTitle("data_obs")
        self.hist_all["Data"].Write("data_obs",rt.TObject.kWriteDelete)
#         self.h_bkg.SetName("data_obs")
#         self.h_bkg.SetTitle("data_obs")
#         self.h_bkg.Write("data_obs",rt.TObject.kWriteDelete)        
        f.Close()  
    def export_hist(self, sig_key, nclass, channel):
        str_sys = self.option
        str_sys = str_sys.replace("weight", "")
        if str_sys!="":
            str_sys = "_"+str_sys
        f = rt.TFile("./Outputs/"+channel+"/shape_"+sig_key+"_"+str(nclass)+".root","UPDATE") 
        f.cd("signal_region")
        self.hist_all[sig_key].SetName("zp"+str_sys)
        self.hist_all[sig_key].SetTitle("zp"+str_sys)
        self.hist_all[sig_key].Write("zp"+str_sys,rt.TObject.kWriteDelete)
        self.merged_hist["TT"].SetName("ttbar"+str_sys)
        self.merged_hist["TT"].SetTitle("ttbar"+str_sys)
        self.merged_hist["TT"].Write("ttbar"+str_sys,rt.TObject.kWriteDelete)
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
        self.merged_hist["TTZ"].SetName("ttz"+str_sys)
        self.merged_hist["TTZ"].SetTitle("ttz"+str_sys)
        self.merged_hist["TTZ"].Write("ttz"+str_sys,rt.TObject.kWriteDelete) 