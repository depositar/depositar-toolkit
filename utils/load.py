# -*- coding: UTF-8 -*-

import os
import re
import json
import urllib2
from collections import OrderedDict

import unicodecsv as csv
from ckanapi import RemoteCKAN


class Load:
    def __init__(self, config):
        self.c = config
        self.registry = RemoteCKAN(config.api_url, apikey=config.api_key)
        self.schema = json.loads(
                urllib2.urlopen('https://github.com/depositar/' + \
                'ckanext-data-depositario/raw/master/ckanext/' + \
                'data_depositario/scheming.json').read())

    def dataset(self, metadata):
        out_rows = OrderedDict()
        reader = csv.DictReader(metadata)
        fields = self.schema['dataset_fields']
        license_list = self.registry.action.license_list()
        for row in reader:
            name = row[u'資料集編號']
            out_row = out_rows.get(name,
                    {'name': name, 'owner_org':self.c.owner_proj, 'keywords': []})
            for k, v in row.iteritems():
                if not v: continue
                for f in fields:
                    if f.get('label')['zh_TW'] == k:
                        # data_type, temp_res
                        if f.get('choices'):
                            for c in f['choices']:
                                if c['label']['zh_TW'] == v:
                                    v = c['value']
                        # license_id
                        if f['field_name'] == 'license_id':
                            for l in license_list:
                                if l['title_zh'] == v:
                                    v = l['id']
                        if f.get('multiple'):
                            # language
                            if f['field_name'] == 'language':
                                v = re.search(r'\((\w+)\)', v).group(1)
                            out_row[f['field_name']] = out_row[f['field_name']] + [v] \
                                if type(out_row.get(f['field_name'])) is list else [v]
                        else:
                            out_row[f['field_name']] = v
            out_rows[name] = out_row
        return '\n'.join([json.dumps(v) for k, v in out_rows.iteritems()])

    def resource(self, metadata, files):
        reader = csv.DictReader(metadata)
        fields = self.schema['resource_fields']
        for r_i, row in enumerate(reader, start=1):
            out_row = {'package_id': row[u'資料集編號']}
            loc = row[u'網址/檔案名稱']
            if not loc:
                print "#%d: Missing url or file. Skip." % r_i
                continue
            if loc[0:7] == 'http://' or loc[0:8] == 'https://':
                # url
                out_row['url'] = loc
            elif files:
                # file
                try:
                    out_row['upload'] = open(os.path.join(files, loc), 'rb')
                except IOError:
                    print "#%d: Missing file, skip" % r_i
                    continue
            for k, v in row.iteritems():
                if not v: continue
                for f in fields:
                    if f.get('label')['zh_TW'] == k:
                        # encoding
                        if f.get('choices'):
                            for c in f['choices']:
                                if c['label']['zh_TW'] == v:
                                    v = c['value']
                        out_row[f['field_name']] = v
            self.registry.action.resource_create(**out_row)
