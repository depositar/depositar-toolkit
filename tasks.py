import io

from invoke import task

from utils import *


@task(help={'config': 'CKAN config file', 'datasets': 'datasets csv',
            'resources': 'resources csv','files': 'file folder'})
def load(c, config, datasets=None, resources=None, files=None):
    l = Load(c)
    if datasets:
        d = l.dataset(open(datasets))
        c.run('ckanapi load datasets --create-only -c {}'.format(config),
              in_stream=io.StringIO(d))
    if resources:
        l.resource(open(resources), files)

@task(help={'config': 'CKAN config file', 'user': 'site adm user'})
def usermail(c, config, user='default'):
    users = io.StringIO()
    c.run('ckanapi action user_list -c {} -u {}'.format(config, user),
         out_stream=users)
    um = UserMail(users.getvalue())
    um.get_list()
