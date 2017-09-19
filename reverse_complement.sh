 #!/bin/bash
DNA=$1
RC=""
for  ((i=0;i<=${#DNA};i++)); 
do
    if [ "${DNA:$i:1}" == "G" ]; then
       RC="C$RC"
    elif [ "${DNA:$i:1}" == "C" ]; then
       RC="G$RC"
    elif [ "${DNA:$i:1}" == "A" ]; then
       RC="T$RC"
    elif [ "${DNA:$i:1}" == "T" ]; then
       RC="A$RC"
    fi
done
echo "$RC"