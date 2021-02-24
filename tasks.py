from StringIO import StringIO

from invoke import task

from utils.load import *


@task(help={'config': 'CKAN config file', 'datasets': 'datasets csv',
            'resources': 'resources csv','files': 'file folder'})
def load(c, config, datasets=None, resources=None, files=None):
    l = Load(c)
    if datasets:
        d = l.dataset(open(datasets))
        c.run('ckanapi load datasets --create-only -c {}'.format(config),
              in_stream=StringIO(d))
    if resources:
        l.resource(open(resources), files)
