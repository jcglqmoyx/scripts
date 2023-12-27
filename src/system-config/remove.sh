TRASH_DIR="/home/hqc/.local/share/Trash/files"
  
for i in $*; do  
    STAMP=`date +%s`  
    fileName=`basename $i`  
    mv $i $TRASH_DIR/$fileName.$STAMP  
done 
