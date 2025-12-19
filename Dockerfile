FROM mambaorg/micromamba:latest

COPY env.yml /tmp/env.yml
RUN micromamba create -n phylogen -f /tmp/env.yml -y && \
    micromamba clean --all -y

# install build tools: git, make, standard compilers
RUN micromamba install -n phylogen -y git make "cxx-compiler" && \\
    micromamba clean --all -y

SHELL ["micromamba", "run", "-n", "phylogen", "/bin/bash", "-c"]

# install fasturec
RUN git clone https://bitbucket.org/pgor17/fasturec.git /home/micromamba/fasturec \
    && cd /home/micromamba/fasturec \
    && make

ENV PATH="/home/micromamba/fasturec/bin:${PATH}"
