'''
Plots sgRNA ranks vs. read fraction of each sgRNA in library. Also calculates the AUC.
Author: Mudra Hegde
Email: mhegde@broadinstitute.org
'''
import pandas as pd
import os, argparse, csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from matplotlib import rc

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputfile',
        type=str,
        help='File with raw sequencing reads')
    parser.add_argument('--thr',
        type=int, 
        default = 0.9,
        help='Fraction of cumulative reads threshold;0.0-1.0')
    parser.add_argument('--outputfolder',
        type=str,
        help='Outputfolder')
    return parser

if __name__ == '__main__':
    rc('pdf', fonttype=42)
    args = get_parser().parse_args()
    outputfolder = args.outputfolder
    print 'Creating output folder...'
    os.system('mkdir '+outputfolder)    
    inputfile = args.inputfile
    input_df = pd.read_table(inputfile)
    colnames = list(input_df.columns)
    outputfile = outputfolder+'/aucs.txt'
    thr = args.thr
    print 'Generating plots and calculating AUCs...'
    with open(outputfile,'w') as o:
        w = csv.writer(o,delimiter='\t')
        w.writerow((['Sample','AUC','Library representation at '+str(thr*100)+'% cumuative reads(in %)']))
        for i,c in enumerate(colnames[2:]):
            row = [c]
            col_sum = float(sum(input_df.ix[:,c]))
            input_df['read_frac'] = [x/col_sum for x in input_df.ix[:,c]]
            input_df = input_df.sort_values(by='read_frac',ascending=False)
            input_df['Cumulative_sum'] = np.cumsum(input_df.read_frac)
            input_df['x-axis'] = [x/float(len(input_df)) for x in range(0,len(input_df))]
            fig1,ax1 = plt.subplots()
            x_axis = list(input_df['x-axis'])
            y_axis = list(input_df.Cumulative_sum)
            p = ax1.plot(x_axis,y_axis,linewidth=1)
            ax1.set_xlim(0.0,1.0)
            ax1.set_ylim(0.0,1.0)
            auc = metrics.auc(x_axis,y_axis)
            row.append(auc)
            frac_sg = round(list(input_df.ix[input_df.Cumulative_sum >= thr,'x-axis'])[0]*100,2)
            row.append(frac_sg)
            w.writerow((row))
            ax1.text(0.6,0.2,'AUC = '+str(round(auc,2)),fontsize=14,fontweight='bold')
            ax1.tick_params(axis='both',labelsize=14,)
            ax1.set_xlabel('sgRNAs ranked by abundance',fontsize=14,fontweight='bold')
            ax1.set_ylabel('Fraction of total represented',fontsize=14,fontweight='bold')
            ax1.set_title(c,fontsize=14,fontweight='bold')
            fig1.savefig(outputfolder+'/'+c+'.pdf',format='pdf')
            plt.close(fig1)