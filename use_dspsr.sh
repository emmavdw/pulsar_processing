#!/bin/bash

echo -n "Enter SAS ID core observations: "
read sas

sas=$(echo $sas | tr --delete L)


# Iterate over all .h5 files in the specified directory
for fname in "L${sas}/cs/L"*.h5; do
    # Extract obsid from the filename
    obsid=$(basename "$fname" | sed -e "s/_S0_/ /g" | awk '{print $1}')

    # Print extracted obsid
    echo "Processing file: $fname"
    echo "Extracted obsid: $obsid"

    # Run dspsr command
    #dspsr -A -L5 -E /home/wateren/parfiles/0329+54.par -O "$obsid" "$fname"
    dspsr -U 481 -L 10 -A -E /home/wateren/parfiles/0809+74.par -O "$obsid" "$fname"
    
    psrsh -e med /home/wateren/code/median_zap.psh ${obsid}.ar
    pam -e Fp -Fp ${obsid}.med
    pam -e Tp -Tp ${obsid}.med
    pam -e FTp -FTp ${obsid}.Fp
done




