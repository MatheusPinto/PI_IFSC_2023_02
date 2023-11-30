<a id="module-codigo.atualiza_certificados"></a>

<a id="codigo-atualiza-certificados"></a>

# codigo.atualiza_certificados

Cria os certificados e chaves privadas usadas na comunicação do Wall-e com o usuário.

Atençâo: executar esse script sobrescreverá as chaves anteriores.

<a id="codigo.atualiza_certificados.cria_chave"></a>

### codigo.atualiza_certificados.cria_chave(tipo: [str](https://docs.python.org/3/library/stdtypes.html#str), cert_path: [str](https://docs.python.org/3/library/stdtypes.html#str), key_path: [str](https://docs.python.org/3/library/stdtypes.html#str), duracao='365')

Cria um certificado e chave privada com o OpenSSL.

O tipo de chave é definida pelo parâmetro *tipo*. A duração em dias do
cerificado é definida por *duracao*. Após esse tempo passar, o
certificado deixará de ser válido. O certificado será salvo com nome
*cert_path* e a chave privada será salva com nome *key_path*.

* **Parâmetros:**
  * **tipo** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Tipo de chave que será gerada.
  * **cert_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Arquivo onde será salvo o certificado.
  * **key_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Arquivo onde será salvo a chave privada.
  * **duracao** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)*,* *default="365"*) – Duração do certificado em dias.
