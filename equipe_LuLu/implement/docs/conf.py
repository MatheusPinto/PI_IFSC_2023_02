# Informações do projeto
project = 'Lixeira móvel com Wall-e'
copyright = '2023, Lucas de Amorim Vasco & Lucas Martins Wollinger'
author = 'Lucas de Amorim Vasco & Lucas Martins Wollinger'
release = '0.0.1'


# COnfigurações gerais
import os
import sys

sys.path.insert(0, os.path.abspath('../'))

sys.path.insert(0, os.path.abspath('../codigo/'))
sys.path.insert(0, os.path.abspath('../codigo/teste'))

sys.path.insert(0, os.path.abspath('../codigo/controlador'))
sys.path.insert(0, os.path.abspath('../codigo/controlador/teste'))

sys.path.insert(0, os.path.abspath('../codigo/movimento'))
sys.path.insert(0, os.path.abspath('../codigo/movimento/fake_RPi'))
sys.path.insert(0, os.path.abspath('../codigo/movimento/teste'))

sys.path.insert(0, os.path.abspath('../codigo/interface'))
sys.path.insert(0, os.path.abspath('../codigo/interface/teste'))

sys.path.insert(0, os.path.abspath('../codigo/segmentacao'))
sys.path.insert(0, os.path.abspath('../codigo/segmentacao/datasets'))
sys.path.insert(0, os.path.abspath('../codigo/segmentacao/teste'))

sys.path.insert(0, os.path.abspath('../codigo/identificacao'))
sys.path.insert(0, os.path.abspath('../codigo/identificacao/teste'))


# Extensões
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.ifconfig',
        'sphinx.ext.napoleon',
        'sphinx.ext.githubpages',
        'sphinx.ext.intersphinx',
        'sphinx_markdown_builder'
        ]

autosummary_generate = True
autosummary_imported_members = True

markdown_anchor_sections = True
markdown_anchor_signatures = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '*.md']

language = 'pt_BR'

intersphinx_mapping = {
        'cv2' : ('http://docs.opencv.org/2.4/', None),
        'cv' : ('http://docs.opencv.org/2.4/', None),
        'numpy': ('http://docs.scipy.org/doc/numpy/', None),
        'np': ('http://docs.scipy.org/doc/numpy/', None),
        'python': ('https://docs.python.org/3', None),
        'PySide6': ('https://doc.qt.io/qtforpython/', None)
        }
