FROM public.ecr.aws/bitnami/python:3.8

RUN apt-get update

RUN apt-get install --no-install-recommends -y curl unzip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

RUN mkdir $HOME/.npm && chmod 777 $HOME/.npm/ && chmod 777 $HOME/

USER $USER
