FROM mambaorg/micromamba:latest

COPY env.yml /tmp/env.yml
RUN micromamba create -n phylogen -f /tmp/env.yml -y && \
    micromamba clean --all -y

# install fasturec
RUN git clone https://bitbucket.org/pgor17/fasturec.git /opt/fasturec \
    && cd /opt/fasturec \
    && make

ENV PATH="/opt/fasturec/bin:${PATH}"

SHELL ["micromamba", "run", "-n", "pipeline", "/bin/bash", "-c"]
