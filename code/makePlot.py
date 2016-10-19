isPrelim=False
import sys

import ROOT as r 
r.gStyle.SetOptStat(0)

fi = r.TFile.Open("mlfit.root")
fiSig = r.TFile.Open("mlfit_Signal1.root")
di = fi 
diSig = fiSig

import plot_config 

r.gROOT.SetBatch(1)

#r.gROOT.ProcessLine(".L plotMonoV.C")
#from ROOT import getDataMV
#from ROOT import getDataMJ

def makePlot(cat,typ,minimum,maximum,name,label):

 config = "plot_config"
 print "Run Config", config
 x = __import__(config)

 can = r.TCanvas("c_%d"%typ,"c_%d"%typ,800,800)
 procs=[]

 # first run through signals, backgrounds and data to check if we need to replace things
 for sl in x.signals.keys():
  for si,s in enumerate(x.signals[sl][0]):
   snew  =  s.replace("$CAT",cat)
   x.signals[sl][0][si] = snew; 

 for b in x.backgrounds.keys():
  for i in range(len(x.backgrounds[b][0])):
   x.backgrounds[b][0][i]=x.backgrounds[b][0][i].replace("$CAT",cat)


 legentries = []
 lat = r.TLatex(); lat.SetNDC()
 lat.SetTextFont(42)
 lat.SetTextSize(0.05)

 pad1 = r.TPad("p1","p1",0,0.28,1,1); pad1.SetBottomMargin(0.01); pad1.SetCanvas(can); pad1.Draw(); pad1.cd()

 totalbackground = di.Get(x.directory+"/%s/total_background"%cat) 
 totalbackground.SetTitle("")
 totalbackground.GetYaxis().SetTitle("Number of events")
 totalbackground.GetYaxis().SetTitleOffset(0.8)
 totalbackground.GetYaxis().SetTitleSize(0.06)
 totalbackground.GetYaxis().SetLabelSize(0.05)
 totalbackground.GetXaxis().SetTitle("")
 totalbackground.GetXaxis().SetLabelSize(0)
 totalbackground.GetYaxis().SetTickLength(0.015)


 totalbackground.SetMinimum(minimum)
 totalbackground.SetMaximum(maximum)

 ratio = r.TGraphAsymmErrors(); ratio.SetName("ratio_data");
 #if typ==0 : getDataMV(totalbackground,ratio)
 #if typ==1 : getDataMJ(totalbackground,ratio)
 data = di.Get(x.directory+"/%s/data"%cat)

 for n in range(0,data.GetN()-1): 
    XX=data.GetX()[n]
    y=data.GetY()[n]
    yh=data.GetErrorYhigh(n)
    yl=data.GetErrorYlow(n)
    bc = totalbackground.GetBinContent(n+1)
    bw = totalbackground.GetBinWidth(n+1)
    y=y/bc
    yh=yh/bc
    yl=yl/bc
    ratio.SetPoint(n,XX,y)
    ratio.SetPointError(n,bw/2,bw/2,yl,yh)


 data.SetTitle("data")
 data.GetXaxis().SetLabelSize(0)
 data.GetYaxis().SetTickLength(0.03)

 thstack = r.THStack("bkg_%s"%cat,"backgroundstack")
 thstack.SetTitle("")
 totalbkg = 0; totalc=0

 leg = r.TLegend(0.5,0.46,0.86,0.87); leg.SetFillColor(0); leg.SetTextFont(42)

 leg.SetBorderSize(0)
 leg.AddEntry(data,"Data","PEL")

 for bkgtype_i,bkg in enumerate(x.key_order):
  nullhist = 0; nullc = 0

  for thist in x.backgrounds[bkg][0]:
    print "trying...",x.directory+"/"+thist, "from",di.GetName()
    tmp = di.Get(x.directory+"/"+thist)
    tmp.SetLineColor(1)

    if len(x.backgrounds[bkg])>3:  # last one is a scale-factor, from fit?
       tmp.Scale(x.backgrounds[bkg][3])

    if nullc == 0 : 	
        print "Starting ", tmp.GetName(), tmp.Integral("")
    	nullhist = tmp.Clone()

    else:
        #print "  ... Adding ", tmp.GetName(), tmp.Integral("")
    	nullhist.Add(tmp)
    nullc+=1


  nullhist.SetLineWidth(2)
  nullhist.SetFillColor(x.backgrounds[bkg][1])
  nullhist.SetFillStyle(1001)
  x.backgrounds[bkg][2]=nullhist.Clone()
  x.backgrounds[bkg][2].SetName("background_%d"%bkgtype_i)
  thstack.Add(x.backgrounds[bkg][2])
  legentries.append([x.backgrounds[bkg][2].Clone(),bkg,"F"])

  totalc+=1


 legentries.reverse()
 for le in legentries: leg.AddEntry(le[0],le[1],le[2])
 
 allsignal = 0
 for b in range(1,totalbackground.GetNbinsX()+1):
   totalbackground.GetXaxis().SetBinLabel(b,"%d"%b)
 totalbackground.Draw("hist")
 for sig_i,sig_t in enumerate(x.signals.keys()):
  totalsignal = 0
  for sig_s_i,sig in enumerate(x.signals[sig_t][0]):
   print "Getting signal %s"%x.directorys+"/"+sig
   tmp = diSig.Get(x.directorys+"/"+sig)
   if sig_s_i==0: totalsignal = tmp.Clone()
   else: totalsignal.Add(tmp)

  totalsignal.SetLineColor(x.signals[sig_t][1])
  totalsignal.SetLineStyle(1)
  totalsignal.SetLineWidth(4)

  if len(x.signals[sig_t])>3:  # last one is a scale-factor
       totalsignal.Scale(x.signals[sig_t][3])

  x.signals[sig_t][2]=totalsignal.Clone()
  legentries.append(x.signals[sig_t][2].Clone())
  leg.AddEntry(legentries[-1],sig_t,"L")

  print "	Nevents ", sig_t, totalsignal.Integral("width")
   #procs.append([tmp.GetName(),tmp.Integral("width")])

  thstack.Draw("histFsame")
  for sig in x.signals.keys(): 
 	x.signals[sig][2].Draw("samehist")

 data.SetMarkerColor(r.kBlack)
 data.SetLineColor(1)
 data.SetLineWidth(2)
 data.SetMarkerSize(1.2)
 data.SetMarkerStyle(20)
 ratio.SetMarkerColor(r.kBlack)
 ratio.SetLineColor(1)
 ratio.SetLineWidth(2)
 ratio.SetMarkerSize(1.2)
 ratio.SetMarkerStyle(20)
 totalbackground.SetFillStyle(3005)
 totalbackground.SetFillColor(1)
 totalbackground.Draw("sameE2")
 data.Draw("samePE")

 leg.Draw()

 pad1.SetLogy()
 pad1.SetTicky()
 pad1.SetTickx()
 pad1.RedrawAxis()

 lat2 = r.TLatex()
 lat2.SetNDC()
 lat2.SetTextFont(42)
 lat2.SetTextSize(0.066)
 #if isPrelim:  lat2.DrawLatex(0.14,0.8,"#bf{CMS} #it{Preliminary}") 
 lat2.DrawLatex(0.14,0.8,"Toy experiment") 
 if cat : lat.DrawLatex(0.14,0.74,label) 
 #lat.DrawLatex(0.67,0.92,"2.3 fb^{-1} (13 TeV)") 
 pad1.RedrawAxis()

 can.cd()
 pad2 = r.TPad("p2","p2",0,0.064,1,0.28)
 pad2.SetTopMargin(0.02)
 pad2.SetBottomMargin(0.23)
 pad2.SetCanvas(can)
 pad2.Draw()
 pad2.cd()

 ratioErr = totalbackground.Clone(); ratioErr.SetName("raterr_elsey");
 for b in range(ratioErr.GetNbinsX()):
 	bw = ratioErr.GetBinContent(b+1);
 	ratioErr.SetBinContent(b+1,1);
	print ratioErr.GetBinError(b+1)
 	ratioErr.SetBinError(b+1,ratioErr.GetBinError(b+1)/bw);
 
 	
 ratioErr.SetFillStyle(3005);
 ratioErr.SetFillColor(1);

 ratioErr.GetYaxis().SetNdivisions(5)
 ratioErr.GetYaxis().SetLabelSize(0.15)
 ratioErr.GetYaxis().SetTitleSize(0.18)
 ratioErr.GetXaxis().SetTitleSize(0.14)
 ratioErr.GetXaxis().SetLabelSize(0.24)
 ratioErr.GetXaxis().SetTitle("")
 ratioErr.SetMaximum(3.9)
 ratioErr.SetMinimum(0.02)

 ratioErr.GetYaxis().SetTitle("Data/Bkg.")
 ratioErr.GetYaxis().SetTitleOffset(0.25)
 ratioErr.GetXaxis().SetTitleOffset(1.4)
 ratioErr.Draw()
 ratioErr.Draw("sameE2")
 line = r.TLine(ratioErr.GetXaxis().GetXmin(),1,ratioErr.GetXaxis().GetXmax(),1)
 line.SetLineColor(1)
 line.SetLineWidth(2)
 line.SetLineStyle(2)
 line.Draw()
 ratio.Draw("samePE")

 pad2.SetGridy()
 pad2.SetTicky()
 pad2.SetTickx()
 pad2.RedrawAxis()
  
 can.cd() 
 lat.SetTextSize(0.055)
 lat.DrawLatex(0.6,0.02,"Search region")
 can.SaveAs("%s.pdf"%name)
 can.SaveAs("%s.C"%name)

#makePlot("VH_had_hinv_13TeV_datacard_SR_monoV",0,0.00005,10000,"plot_monov","V(jj)-tagged")
#makePlot("ggH_hinv_13TeV_datacard_SR_monoJ",1,0.002,100000,"plot_monoj","Monojet-tagged")

#makePlot("VH_had_hinv_13TeV_datacard_SR_monoV",0,0.00005,10000,"plot_monov","V(jj)")
makePlot("htsearch",1,0.011,100000,"plot_dummy","")
