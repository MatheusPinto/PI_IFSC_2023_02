#!/bin/sh
#
#
# Atualiza os certificados e chaves utilizados pelo SSH e Rsync
#
# Atenção: as credenciais antigas são excluídas. Cuidado ao usar esse script.


WALLE_PRIVATE_KEY_PATH='env/ssh/dropbear_ed25519_host_key'
WALLE_PUBLIC_KEY_PATH='env/ssh/walle-ssh.pub'
CLIENT_PRIVATE_KEY_PATH='env/ssh/client_ecdsa_key'
CLIENT_PUBLIC_KEY_PATH='env/ssh/client-ssh.pub'


# Cria o diretório onde estará a chave privada
mkdir -p $(dirname "$WALLE_PRIVATE_KEY_PATH")

if [ -f "$WALLE_PRIVATE_KEY_PATH" ]; then
	rm "$WALLE_PRIVATE_KEY_PATH"
fi

if [ -f "$CLIENT_PRIVATE_KEY_PATH" ]; then
	rm "$CLIENT_PRIVATE_KEY_PATH"
fi

# Chave do Wall-e
dropbearkey -t ed25519 -s 256 -f "$WALLE_PRIVATE_KEY_PATH"
dropbearkey -y -f "$WALLE_PRIVATE_KEY_PATH" > "$WALLE_PUBLIC_KEY_PATH"

# Chave do cliente
dropbearkey -t ed25519 -s 256 -f "$CLIENT_PRIVATE_KEY_PATH"
dropbearkey -y -f "$CLIENT_PRIVATE_KEY_PATH" > "$CLIENT_PUBLIC_KEY_PATH"
