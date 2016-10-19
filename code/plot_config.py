import ROOT as r
directory  = "shapes_prefit"
directorys = "shapes_prefit"

signals = {
 	   "Signal":[
               ["$CAT/signal"
		] ,r.kRed+1,0]
	  }

key_order = ["W(#rightarrow#it{l#nu})+jets","Z(#rightarrow#it{#nu#nu})+jets"]

backgrounds = { 
		"W(#rightarrow#it{l#nu})+jets":      [["$CAT/wjets"], 		r.kAzure-2, 0]
		,"Z(#rightarrow#it{#nu#nu})+jets":    [["$CAT/zjets"],		r.kOrange, 0]
	      }

