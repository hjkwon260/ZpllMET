FROM gitlab-registry.cern.ch/linuxsupport/rpmci/builder-al9:latest # 08.09.23

LABEL maintainer="Hyejin Kwon <hj.kwon@cern.ch>"

RUN dnf install -y root python3-root root-notebook python3-pip R python3-devel
RUN pip3 install numpy uproot pandas tqdm
RUN pip3 install uproot pandas tqdm jupyterlab tensorflow scikit-learn seaborn rpy2
