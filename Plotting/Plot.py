#!/usr/bin/env python
"""
Thomas:
"""

########################################
# Imports
########################################

import os
import argparse
import pickle

import sys
sys.path.append('src')
from SlicePlot import SlicePlot

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = kError;")
ROOT.gStyle.SetOptStat(0)


########################################
# Main
########################################

def Plot():

    ########################################
    # Command line options
    ########################################

    parser = argparse.ArgumentParser()
    parser.add_argument( '--plotdir', type=str, help='Overwrites the default plot directory and uses this one' )
    parser.add_argument( 'picklefiles', metavar='N', type=str, nargs='+', help='Give a list of fitted pickle files to plot')
    parser.add_argument( '--compare', action='store_true', help='Compare the two given pickle files')
    parser.add_argument( '--override', action='store_true', help='Overrrides certain plot options (set in Plot.py)')
    args = parser.parse_args()    


    ########################################
    # PLOTTING PROCEDURE
    ########################################    

    if not args.compare:

        for pickle_fn in args.picklefiles:

            if not os.path.isfile( pickle_fn ):
                print 'Error: Can not make plots because {0} does not exist'.format( pickle_fn )
                continue

            with open( pickle_fn, 'rb' ) as pickle_fp:
                sliceplot = pickle.load( pickle_fp )


            if args.override:
                sliceplot.sliceplot_y_min = 0.99
                sliceplot.sliceplot_y_max = 1.01

                if os.path.basename(pickle_fn) == 'electronEE_GENPT-0000-0100.pickle':
                    print '    Setting sigma range to larger values'
                    sliceplot.sliceplotsigma_y_min   = 0.0
                    sliceplot.sliceplotsigma_y_max   = 0.25



            if args.plotdir:
                sliceplot.plotdir = args.plotdir

            if not os.path.isdir( sliceplot.plotdir ): os.makedirs( sliceplot.plotdir )

            sliceplot.MakePlots_standard()


    # Compare two fits
    elif args.compare:

        if not len(args.picklefiles)==2:
            print 'Only 2 picklefiles can be compared at a time!'
            return

        picklefile1 = args.picklefiles[0]
        picklefile2 = args.picklefiles[1]

        with open( picklefile1, 'rb' ) as pickle_fp:
            sliceplot1 = pickle.load( pickle_fp )
        with open( picklefile2, 'rb' ) as pickle_fp:
            sliceplot2 = pickle.load( pickle_fp )

        sliceplot1.MakePlots_comparison( sliceplot2 )



########################################
# Functions
########################################


########################################
# End of Main
########################################
if __name__ == "__main__":
    Plot()