FROM ghcr.io/youngminkchoi/cadre-jedi-edu-base:v2 
# FROM jcsda/docker-clang-mpich-dev:edu - for old JEDI build (will not work with LPF tutorial)

#NOTE python used by Container is /opt/view/bin/python3, so need to install with that version
RUN /opt/view/bin/python3 -m pip install jupyter -U && /opt/view/bin/python3 -m pip install jupyterlab
RUN /opt/view/bin/python3 -m pip install bash_kernel && /opt/view/bin/python3 -m bash_kernel.install
RUN /opt/view/bin/python3 -m pip install -U matplotlib
RUN /opt/view/bin/python3 -m pip show numpy
RUN /opt/view/bin/python3 -m pip install netCDF4

COPY --chmod=755 start /srv
#RUN chmod +x /srv/start

EXPOSE 8888
USER nonroot
WORKDIR /home/nonroot
ENV SHELL=/bin/bash
ENTRYPOINT ["/srv/start"]
#ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
