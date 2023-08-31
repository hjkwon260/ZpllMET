thisdir=/cvmfs/sft.cern.ch/lcg/views/LCG_103swan/x86_64-centos7-gcc11-opt/
echo ${thisdir}

#---then ROOT
if [ -x $thisdir/bin/root ]; then
    if [ -x $thisdir/bin/python ]; then
        PYTHON_INCLUDE_PATH=$(dirname $(dirname $(readlink $thisdir/bin/python)))/include/$(\ls $(dirname $(dirname $(readlink $thisdir/bin/python)))/include)
    fi
    ROOTSYS=$(dirname $(dirname $(readlink $thisdir/bin/root))); export ROOTSYS
    if [ -z "${ROOT_INCLUDE_PATH}" ]; then
        ROOT_INCLUDE_PATH=${thisdir}/include:$PYTHON_INCLUDE_PATH; export ROOT_INCLUDE_PATH
    else
        ROOT_INCLUDE_PATH=${thisdir}/include:$PYTHON_INCLUDE_PATH:$ROOT_INCLUDE_PATH; export ROOT_INCLUDE_PATH
    fi
    if [ -d $thisdir/targets/x86_64-linux/include ]; then
        ROOT_INCLUDE_PATH=${thisdir}/targets/x86_64-linux/include:$ROOT_INCLUDE_PATH; export ROOT_INCLUDE_PATH
    fi
    if [ -z "${JUPYTER_PATH}" ]; then
        JUPYTER_PATH=${thisdir}/etc/notebook; export JUPYTER_PATH
    else
        JUPYTER_PATH=${thisdir}/etc/notebook:$JUPYTER_PATH; export JUPYTER_PATH
    fi
    export CPPYY_BACKEND_LIBRARY=$ROOTSYS/lib/libcppyy_backend${PYTHON_VERSION/./_}
    export CLING_STANDARD_PCH=none
fi