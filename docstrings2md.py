# pylint: skip-file
# for details see https://stackoverflow.com/questions/36237477/python-docstrings-to-github-readme-md
# further details in https://blog.matteoferla.com/2019/11/convert-python-docstrings-to-github.html

import re
import shutil
import os
import subprocess

# ## Settings
MODULE_NAME = 'event_superschema'
AUTHOR_NAME = 'Ronald Landheer-Cieslak'
OUTPUT_FILENAME = 'event_superschema.md'

# ## Apidoc call
arguments = ['-o',
            'Sphinx-docs',
            MODULE_NAME,
            'sphinx-apidoc',
            '--full',
            '-A',
            f"'${AUTHOR_NAME}'",
            '--module-first',
            '--ext-githubpages',
            ]
proc = subprocess.run(["sphinx-apidoc", *arguments], capture_output=True)
if r := proc.stderr:
    raise RuntimeError(r.decode())
print(proc.stdout.decode())

# ## tweak configuration

with open('Sphinx-docs/conf.py') as fh:
    conf_codeblock = fh.read()
conf_codeblock = conf_codeblock.replace('# import os', 'import os')\
                               .replace('# import sys', 'import sys\nsys.path.insert(0, os.path.abspath("../"))')\
                               .replace("'sphinx.ext.autodoc',", "'sphinx.ext.autodoc','sphinx_autodoc_typehints','sphinx_markdown_builder',")
conf_codeblock += '''
def skip(app, what, name, obj, would_skip, options):
    if name in ( '__init__',):
        return False
    return would_skip
def setup(app):
    app.connect('autodoc-skip-member', skip)
'''

with open('Sphinx-docs/conf.py', 'w') as fh:
    fh.write(conf_codeblock)

# ## Make

os.chdir('Sphinx-docs')
os.system('make markdown')
os.chdir('..')

# ## Consolidate Markdown

folder = 'Sphinx-docs/_build/markdown'

def clean_markdown(markdown):
    markdown = re.sub(r'\n+    \* ', '\n * ', markdown)
    markdown = re.sub(r'\n+\* ', '\n* ', markdown)
    return markdown.replace('    *', '*')\
                   .replace('>>> ', '')

with open(os.path.join(folder, MODULE_NAME+'.md')) as fh:
    markdown = clean_markdown(fh.read())
for filename in os.listdir(folder):
    if filename == MODULE_NAME+'.md':
        continue
    if MODULE_NAME not in filename:
        continue
    with open(os.path.join(folder, filename)) as fh:
        markdown += clean_markdown(fh.read())

with open(OUTPUT_FILENAME, 'w') as fh:
    fh.write(markdown)

# ## Removing Sphynx folder
shutil.rmtree('Sphinx-docs')
