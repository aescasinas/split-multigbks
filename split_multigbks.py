import os
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Split a multi-gbk file to separate files.')
parser.add_argument('input_dir', type=str, help='Input directory containing multi-gbk files i.e. DeepBGC output file (.bgc.gbk)')
args = parser.parse_args()

# a directory containing multiple multi-gbk files.
multigbk_dir = args.input_dir

# make a directory called output in the same level of the input directory
os.mkdir(f'{multigbk_dir}/../output')
output_dir = f'{multigbk_dir}/../output' # variable for the output directory

# list of filenames in the input directory
input_files = os.listdir(multigbk_dir)

# iterate through the gbk files in the input directory
for gbk in input_files:

    # get the strain name and make a subdirectory inside the output directory
    strain_name = gbk.split('.')[0]
    print(f'Processing {strain_name}')
    os.mkdir(f'{output_dir}/{strain_name}')

    # read each line of the multigbk file
    with open(f'{multigbk_dir}/{gbk}', 'r') as multigbk_file:
        lines = multigbk_file.readlines()

    count = 1
    for line in lines:
        if "LOCUS" in line:
            fname = f'{strain_name}_region{count}_{line.split()[2]}.gbk' # name of individual separated gbk file
            subprocess.call(f'touch {output_dir}/{strain_name}/{fname}'.split()) # create a gbk file inside the "output/fname" directory
            with open(f'{output_dir}/{strain_name}/{fname}', 'a') as out_file:
                out_file.write(line)
            count += 1
        else:
            with open(f'{output_dir}/{strain_name}/{fname}', 'a') as out_file:
                out_file.write(line)
