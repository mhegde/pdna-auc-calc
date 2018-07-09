# AUC calculation for pDNA -- Library distribution
<b>This script plots the sgRNA ranks vs. their read fractions. It also calculates and displays the AUC </b>  
<b>Author</b>: Mudra Hegde  
<b>Email</b>: mhegde@broadinstitute.org  
<b>Version: 1.0 </b>  

<b>Required packages</b>
1. pandas
2. numpy
3. matplotlib
4. scikit-learn

<b>Inputs</b>
1. <b>Input file</b>: .txt file with raw read counts.
2. <b>Column</b>: Column number of column with read counts to be plotted.
3. <b>Title</b>: Title for final plot.
4. <b>Output file</b>

<b>To run this script, type the following on the terminal:</b>
python calc_read_frac_v1.0.py --input-file \<Path to input file\> --column \<Column number\> --title \<Plot title\> --outputfile \<Path to outputfile\>