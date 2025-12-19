FROM mambaorg/micromamba:latest

COPY env.yml /tmp/env.yml
RUN micromamba create -n phylogen -f /tmp/env.yml -y && \
    micromamba clean --all -y

RUN micromamba install -n phylogen -y git make gcc_linux-64 gxx_linux-64 \
    && micromamba clean --all -y

# install fasturec
RUN git clone https://bitbucket.org/pgor17/fasturec.git /opt/fasturec \
    && cd /opt/fasturec \
    && make

ENV PATH="/opt/fasturec/bin:${PATH}"

SHELL ["micromamba", "run", "-n", "phylogen", "/bin/bash", "-c"]
