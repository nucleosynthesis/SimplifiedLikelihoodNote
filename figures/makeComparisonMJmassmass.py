import ROOT 
import array 

ROOT.gROOT.SetBatch(1)

ncontours = 20;

stops   = array.array('d',[0.0 ,  0.25,  0.5 , .75     , 1.0   ])
blue    = array.array('d',[0.  ,  0.  ,  1.0  , 0       , 0.00 ])
green   = array.array('d',[0.  ,  0.0 ,  1.0  , 0.5    , 1.00 ])
red     = array.array('d',[1.  ,  0.5 ,  1.0 , 0.0     ,  0 ])

npoints = 5;
ROOT.TColor.CreateGradientColorTable(npoints, stops, red, green, blue, ncontours);
ROOT.gStyle.SetNumberContours(ncontours);

def DIVIDE(h1,h2):
  
  for i in range(1,h1.GetNbinsX()+1):
    for j in range(1,h1.GetNbinsX()+1):
      x = h1.GetXaxis().GetBinCenter(i)
      y = h1.GetYaxis().GetBinCenter(j)
      c = h1.GetBinContent(i,j)

      rat = 1 

      if h2.GetXaxis().GetXmin() > x or h2.GetXaxis().GetXmax() < x : rat = 1
      elif h2.GetYaxis().GetXmin() > y or h2.GetYaxis().GetXmax() < y : rat = 1
      else: 
        d = h2.Interpolate(x,y)
        if d == 0: rat = 1 
        else: rat = c/d 

      h1.SetBinContent(i,j,rat)
  

def makeNice2DPlot(slname,lname, title):

  can = ROOT.TCanvas("c","c",800,800)

  can.SetLeftMargin(0.15)
  can.SetRightMargin(0.165)
  can.SetBottomMargin(0.12)
  can.SetTicky()
  can.SetTickx()

  slfile = ROOT.TFile.Open(slname)
  lfile = ROOT.TFile.Open(lname)

  scan_sl_obs = slfile.Get("observed_scan")
  scan_fl_obs = lfile.Get("hobs2")
  scan_fl_exp = lfile.Get("hexp2")
  
  DIVIDE(scan_sl_obs,scan_fl_obs)
  scan_sl_obs.SetMaximum(1.95)
  scan_sl_obs.SetMinimum(-0.05)

  scan_fl_obs.SetContour(2)
  scan_fl_obs.SetContourLevel(1,1)
  scan_fl_exp.SetContour(2)
  scan_fl_exp.SetContourLevel(1,1)
  
  cont_sl_obs = slfile.Get("observed_contour")
  cont_sl_exp = slfile.Get("expected_contour")

  scan_sl_obs.GetXaxis().SetTitle("#it{m}_{MED} [GeV]");
  scan_sl_obs.GetYaxis().SetTitle("#it{m}_{DM} [GeV]");
  scan_sl_obs.GetZaxis().SetTitle("#it{#mu}_{up}^{95%} (#it{L_{S}}) / #it{#mu}_{up}^{95%}  (#it{L}) ");
  scan_sl_obs.GetZaxis().SetTitleOffset(1.6);
  scan_sl_obs.GetZaxis().SetTitleSize(0.03);
  scan_sl_obs.GetYaxis().SetTitleOffset(1.4);
  scan_sl_obs.GetXaxis().SetNdivisions(105)
  scan_sl_obs.SetTitle("");

  cont_sl_obs.SetLineColor(ROOT.kAzure+1)
  cont_sl_exp.SetLineColor(ROOT.kMagenta+1)
  cont_sl_exp.SetLineStyle(1)
  
  scan_fl_obs.SetLineColor(ROOT.kBlack)
  scan_fl_exp.SetLineColor(ROOT.kBlack)
  scan_fl_exp.SetLineStyle(2)

  scan_sl_obs.Draw("colz")
  palette = scan_sl_obs.GetListOfFunctions().FindObject("palette");
  palette.SetY2NDC(0.9);
  palette.SetY1NDC(0.12);
  palette.SetX1NDC(0.86);
  palette.SetX2NDC(0.88);

  cont_sl_obs.Draw("l")
  cont_sl_exp.Draw("l")
  scan_fl_obs.Draw("cont3same")
  scan_fl_exp.Draw("cont3same")

  lat = ROOT.TLatex(); lat.SetNDC()
  lat.SetTextFont(42)
  lat.SetTextSize(0.03)
  lat.SetTextAlign(32)
  lat.DrawLatex(0.85,0.94,title)

  leg = ROOT.TLegend(0.2,0.6,0.6,0.84)
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  leg.AddEntry(scan_fl_obs,"Full likelihood (observed)","L")
  leg.AddEntry(scan_fl_exp,"Full likelihood (expected)","L")
  leg.AddEntry(cont_sl_obs,"Simplified likelihood (observed)","L")
  leg.AddEntry(cont_sl_exp,"Simplified likelihood (expected)","L")
  leg.Draw()
  can.SaveAs("compare_mj_limits_%s.png"%slname.strip(".root"))


def makeNice1DPlot(slname,lname, title):
  can = ROOT.TCanvas("c","c",800,800)

  can.SetLeftMargin(0.15)
  can.SetRightMargin(0.15)
  can.SetBottomMargin(0.12)
  can.SetTicky()
  can.SetTickx()

  slfile = ROOT.TFile.Open(slname)
  lfile = ROOT.TFile.Open(lname)

  cont_sl_obs = slfile.Get("observedLimit")
  cont_sl_exp = slfile.Get("expectedLimit")
  cont_fl_obs = lfile.Get("obs")
  cont_fl_exp = lfile.Get("exp")

  cont_sl_obs.GetXaxis().SetTitle("#it{m}_{MED} [GeV]");
  cont_sl_obs.GetYaxis().SetTitle("#it{#mu}_{up}^{95%} ");
  cont_sl_obs.GetYaxis().SetTitleOffset(1.2);
  cont_sl_obs.SetTitle("");

  cont_sl_obs.SetLineColor(ROOT.kAzure+1)
  cont_sl_exp.SetLineColor(ROOT.kAzure+1)
  cont_sl_exp.SetLineStyle(2)
  cont_fl_obs.SetLineColor(ROOT.kBlack)
  cont_fl_exp.SetLineColor(ROOT.kBlack)
  cont_fl_exp.SetLineStyle(2)
   
  cont_sl_obs.Draw("al")
  cont_sl_exp.Draw("l")
  cont_fl_obs.Draw("l")
  cont_fl_exp.Draw("l")


  lat = ROOT.TLatex(); lat.SetNDC()
  lat.SetTextFont(42)
  lat.SetTextSize(0.03)
  lat.SetTextAlign(32)
  lat.DrawLatex(0.835,0.94,title)

  leg = ROOT.TLegend(0.2,0.6,0.6,0.84)
  leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  leg.AddEntry(cont_fl_obs,"Full likelihood (observed)","L")
  leg.AddEntry(cont_fl_exp,"Full likelihood (expected)","L")
  leg.AddEntry(cont_sl_obs,"Simplified likelihood (observed)","L")
  leg.AddEntry(cont_sl_exp,"Simplified likelihood (expected)","L")
  leg.Draw()
  can.SaveAs("compare_mj_limits_%s.pdf"%slname.strip(".root"))

def makeNiceScan(slname,title):
  can = ROOT.TCanvas("c","c",800,800)

  can.SetLeftMargin(0.15)
  can.SetRightMargin(0.15)
  can.SetBottomMargin(0.12)
  can.SetTicky()
  can.SetTickx()

  slfile = ROOT.TFile.Open(slname)

  cont_sl_obs = slfile.Get("observed_simp_likelihood_full_covariance")
  cont_sl_exp = slfile.Get("expected_simp_likelihood_full_covariance")
  cont_sl_obs_nc = slfile.Get("observed_simp_likelihood_no_corr")
  cont_sl_exp_nc = slfile.Get("expected_simp_likelihood_no_corr")
  cont_fl_obs = slfile.Get("observed_full_likelihood")
  cont_fl_exp = slfile.Get("expected_full_likelihood")

  cont_sl_obs.GetXaxis().SetTitle("#it{#mu}");
  cont_sl_obs.GetYaxis().SetTitle("#it{q(#mu)} ");
  cont_sl_obs.GetYaxis().SetTitleOffset(1.2);
  cont_sl_obs.SetTitle("");

  cont_sl_obs.SetLineColor(ROOT.kAzure+1)
  cont_sl_exp.SetLineColor(ROOT.kAzure+1)
  cont_sl_exp.SetLineStyle(2)
  cont_fl_obs.SetLineColor(ROOT.kBlack)
  cont_fl_exp.SetLineColor(ROOT.kBlack)
  cont_fl_exp.SetLineStyle(2)

  cont_sl_obs_nc.SetLineColor(ROOT.kRed)
  cont_sl_exp_nc.SetLineColor(ROOT.kRed)
  cont_sl_exp_nc.SetLineStyle(2)

  cont_sl_obs.GetYaxis().SetRangeUser(0,10)   
  cont_sl_obs.GetXaxis().SetRangeUser(-4,3)   
  cont_sl_obs.Draw("al")
  cont_sl_exp.Draw("l")
  cont_fl_obs.Draw("l")
  cont_fl_exp.Draw("l")

  cont_sl_obs_nc.Draw("l")
  cont_sl_exp_nc.Draw("l")

  lat = ROOT.TLatex(); lat.SetNDC()
  lat.SetTextFont(42)
  lat.SetTextSize(0.025)
  lat.SetTextAlign(32)
  lat.DrawLatex(0.835,0.94,title)

  leg = ROOT.TLegend(0.2,0.6,0.6,0.84)
  #leg.SetFillStyle(0)
  leg.SetBorderSize(0)
  leg.AddEntry(cont_fl_obs,"Full likelihood (observed)","L")
  leg.AddEntry(cont_fl_exp,"Full likelihood (expected)","L")
  leg.AddEntry(cont_sl_obs,"Simplified likelihood (observed)","L")
  leg.AddEntry(cont_sl_exp,"Simplified likelihood (expected)","L")
  leg.AddEntry(cont_sl_obs_nc,"Simplified likelihood (observed, no corr.)","L")
  leg.AddEntry(cont_sl_exp_nc,"Simplified likelihood (expected, no corr.)","L")
  leg.Draw()
  can.SaveAs("compare_mj_likelihoods.pdf")


makeNice2DPlot("scan_combined_vector.root","vector_g025.root","Vector mediator, #it{g}_{SM}=0.25, #it{g}_{DM}=1")
makeNice2DPlot("scan_combined_axial.root","axial_g025.root","Axial mediator, #it{g}_{SM}=0.25, #it{g}_{DM}=1")

makeNice1DPlot("brazilian_combo_scalar.root","limit_1D_scalar.root","Scalar mediator, #it{g}_{q}=0.25, #it{g}_{DM}=1, #it{m}_{DM}=10 GeV")
makeNice1DPlot("brazilian_combo_pseudoscalar.root","limit_1D_ps.root","Pseudoscalar mediator, #it{g}_{q}=0.25, #it{g}_{DM}=1, #it{m}_{DM}=10 GeV")


makeNiceScan("likelihoodComparison.root","Vector mediator, #it{g}_{q}=0.25, #it{g}_{DM}=1, #it{m}_{MED}=1.8 TeV, #it{m}_{DM}=1 GeV")
