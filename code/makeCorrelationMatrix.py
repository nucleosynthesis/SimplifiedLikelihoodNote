import ROOT
fi = ROOT.TFile.Open("mlfit.root")
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
catmap = {"htsearch":""};

for cat in ["htsearch"]: 

  bkg = fi.Get("shapes_prefit/%s/total_background"%(cat))
  cov = fi.Get("shapes_prefit/%s/total_covar"%(cat))
  nbins = bkg.GetNbinsX()
  cor = cov.Clone()
  cor.SetTitle("")
  cor.SetName("correlation")
  cor.GetXaxis().SetTitle("Search region")
  cor.GetYaxis().SetTitle("Search region")

  for b in range(1,nbins+1): 
    etmin = bkg.GetBinLowEdge(b);
    etmax = bkg.GetBinLowEdge(b+1);

    cor.GetXaxis().SetBinLabel(b,"%d"%(b))
    cor.GetYaxis().SetBinLabel(b,"%d"%(b))
    cor.GetXaxis().SetLabelSize(0.05)
    cor.GetYaxis().SetLabelSize(0.05)
    #cor.GetXaxis().LabelsOption("v"); 


    for c in range(1,nbins+1):

      bwB = bkg.GetBinWidth(b)
      bwC = bkg.GetBinWidth(c)

      EBC = cov.GetBinContent(b,c)
      print " Covariance = ", EBC,
      EB  = cov.GetBinContent(b,b)
      EC  = cov.GetBinContent(c,c)

      sigb = EB**0.5
      sigc = EC**0.5

      cor.SetBinContent(b,c,EBC)
      print " Correlation = ", EBC/(sigb*sigc)

  can = ROOT.TCanvas("c","c",1800,1800)
  can.SetGridy()
  can.SetGridx()
  can.SetLeftMargin(0.12)
  can.SetRightMargin(0.05)
  can.SetBottomMargin(0.12)
  ROOT.gStyle.SetPaintTextFormat(".1f");

  #if cat=="monojet": cor.SetMarkerSize(0.8)
  cor.SetMarkerSize(1.2)
  cor.Draw("TEXT")
  lat2 = ROOT.TLatex()
  lat2.SetNDC()
  lat2.SetTextFont(42)
  lat2.SetTextSize(0.04)
  lat2.DrawLatex(0.12,0.92,"Covariance") 
  #lat2.DrawLatex(0.69,0.92,"19.7 fb^{-1} (8 TeV)") 
  
  lat2.SetTextSize(0.025)
  lat2.DrawLatex(0.01,0.92,catmap[cat]) 

  can.SaveAs("%s_covariance.png"%cat)
  can.SaveAs("%s_covariance.pdf"%cat)

