
# get the file directory
INSTALL_DIR=$(dirname $0)
cd $INSTALL_DIR

# adding lib dir to PYHTONPATH
export PYTHONPATH=$INSTALL_DIR/lib/:$PYTHONPATH

#python Duskr/Duskrcli.py
#python Duskr/XmpSettingLister.py
#python Duskr/ExivCRawRequester.py
python Duskr/XmpFileDescriptor.py
