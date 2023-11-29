#!/bin/sh


# Remove os antigos arquivos
rm -r _autosummary 2> /dev/null


# Cria
make clean markdown
