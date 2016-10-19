in order to produce the same data as the figure, you need to run with:
'''bash
combine -M MaxLikelihoodFit -t 1 --expectSignal 0 -s 10 signal_region_simple.txt --saveShapes --saveWithUnc --saveOverall --freezeNuisances zjetsScale --setPhysicsModelParameters zjetsScale=5 (--preFitValue 0)
'''
where --preFitValue 0 is included to make the covariance and not included for the signal


