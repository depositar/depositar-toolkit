from StringIO import StringIO

from invoke import task

from utils import *


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

@task(help={'config': 'CKAN config file'})
def usermail(c, config):
    users = StringIO()
    c.run('ckanapi action user_list -c {}'.format(config),
         out_stream=users)
    um = UserMail(users.getvalue())
    um.get_list()
