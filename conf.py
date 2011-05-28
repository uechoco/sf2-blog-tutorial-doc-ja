import sys, os
from sphinx.highlighting import lexers
from pygments.lexers.web import PhpLexer
from pygments.lexers.text import YamlLexer

sys.path.append(os.path.abspath('_exts'))

extensions = []
master_doc = 'index'
highlight_language = 'php'

project = u'Symfony2 Blog Tutorial'
copyright = u'2011 Japan Symfony Users Group'

version = '0'
release = '0.0.0'

lexers['php'] = PhpLexer(startinline=True)
lexers['yml'] = YamlLexer()

