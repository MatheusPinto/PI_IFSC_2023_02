{{ fullname | escape | underline}}

.. automodule:: {{ fullname }}
   :members:
   :private-members:
   :special-members: __init__, __call__
   :show-inheritance:


{% block modules %}
{% if modules %}
.. rubric:: Modules

.. autosummary::
   :toctree:
   :recursive:
{% for item in modules %}
   {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}
