#!/bin/sh
#
#
# Script que configura as chaves SSH Raspberry Pi.
# Deve ser executado no diretório contendo a pasta 'env/'


# Copia as chaves SSH do Walle
sudo cp env/ssh/dropbear_ed25519_host_key /etc/dropbear/


# Copia a chave pública SSH do cliente para o root (necessário para usar o Rsync)
sudo mkdir -p /root/.ssh
sudo cp env/ssh/client-ssh.pub /root/.ssh/authorized_keys


# Copia a chave pública SSH do cliente para o usuário
mkdir -p ~/.ssh
cp env/ssh/client-ssh.pub ~/.ssh/authorized_keys
