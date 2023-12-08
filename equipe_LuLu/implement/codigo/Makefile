all: atualiza-certificados atualiza-ssh


# Inclusão das configurações básicas
include env/conf


# Parâmetros
PASTAS_PARA_SINCRONIZAR = env interface raspberry movimento cliente.py walle.py fake_RPi.py


atualiza-certificados:
	python3 atualiza_certificados.py

atualiza-ssh:
	./atualiza_ssh.sh

ssh:
	dbclient -i ./env/ssh/client_ecdsa_key $(USUARIO)@$(IP)

rsync:
	rsync -a --delete --delete-excluded --exclude-from=rsync-exclude-patterns.txt -e 'dbclient -i ./env/ssh/client_ecdsa_key root@'$(IP) $(PASTAS_PARA_SINCRONIZAR) $(USUARIO)@::code
