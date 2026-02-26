#!/bin/bash

filbkg=$1 #"hofx_meanbkg_loc6.txt"
filanl=$2 #"hofx_meananl_loc6.txt"

## Read in to determine number of obs first 
nobs=0
while read line; do
  (( nobs = nobs + 1 ))
done < $filbkg
(( nobs = nobs - 1 )) # ignore header line

#set -vx
flag=0
sumsquares="0"
while read line; do
#  echo $line ${line##*/} ${line#*/}
  if [ $flag -eq 0 ]; then # ski[ header
    flag=1
    continue
  fi
  tmp=${line#*/}
  strobs=${tmp%/*}
  strdata=${tmp#*/}
  data=${strdata/[/}
  data=${data/]/}
  data=${data/e+/e}
  obs=${strobs/[/}
  obs=${obs/]/}
  obs=${obs/e+/e}
  sumsquares=$(awk "BEGIN {print $sumsquares + (${obs}-${data})^2}")
done < $filbkg

RMSDbkg=$(awk "BEGIN {print sqrt($sumsquares / $nobs) }")

flag=0
sumsquares=0
while read line; do
  #echo $line ${line##*/}
  if [ $flag -eq 0 ]; then # ski[ header
    flag=1
    continue
  fi
  tmp=${line#*/}
  strobs=${tmp%/*}
  strdata=${tmp#*/}
  data=${strdata/[/}
  data=${data/]/}
  data=${data/e+/e}
  obs=${strobs/[/}
  obs=${obs/]/}
  obs=${obs/e+/e}
  sumsquares=$(awk "BEGIN {print $sumsquares + (${obs}-${data})^2}")
done < $filanl

RMSDanl=$(awk "BEGIN {print sqrt($sumsquares / $nobs) }")

echo "For filbkg=$1 and filanl=$2"
echo "RMSD bkg, anl = ${RMSDbkg} ${RMSDanl}"
echo ""
