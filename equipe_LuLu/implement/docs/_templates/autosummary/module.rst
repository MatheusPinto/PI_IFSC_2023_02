{{ fullname | escape | underline}}


{# Documentação de um arquivo #}

{% if not modules %}
:code: [{{ name }}.py](../../../../{{ fullname | replace('.','/') }}.py)
{% endif %}

.. automodule:: {{ fullname }}
   :members:
   :private-members:
   :special-members: __init__, __call__
   :show-inheritance:


{# Documentação de uma pasta #}

{% block modules %}
{% if modules %}

:folder: [{{ name }}/](../../../../{{ fullname | replace('.','/') }})

.. rubric:: Modulos

.. autosummary::
   :toctree:
   :recursive:
{% for item in modules %}
   {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}
