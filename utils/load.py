# -*- coding: UTF-8 -*-

import os
import re
import csv
import json
import yaml
import urllib
from collections import OrderedDict

from ckanapi import RemoteCKAN


class Load:
    def __init__(self, config):
        self.c = config
        self.registry = RemoteCKAN(config.api_url, apikey=config.api_key)
        with urllib.request.urlopen('https://raw.githubusercontent.com/depositar/' + \
                                    'ckanext-data-depositario/master/ckanext/' + \
                                    'data_depositario/schemas/dataset.yaml') as url:
            self.schema = yaml.safe_load(url.read())

    def dataset(self, metadata):
        out_rows = OrderedDict()
        reader = csv.DictReader(metadata)
        fields = self.schema['dataset_fields']
        license_list = self.registry.action.license_list()
        theme_list = self.registry.action.group_list(all_fields=True)
        for row in reader:
            name = row[u'資料集編號']
            out_row = out_rows.get(name,
                    {'name': name, 'owner_org':self.c.owner_proj, 'keywords': []})
            # theme
            theme = row.get(u'主題')
            if theme:
                for t in theme_list:
                    if t['title'] == theme:
                        theme = {'name': t['name']}
                out_row['groups'] = out_row['groups'] + [theme] \
                    if type(out_row.get('groups')) is list else [theme]
            for k, v in row.items():
                if not v: continue
                for f in fields:
                    if f.get('label')['zh_Hant_TW'] == k:
                        # data_type, temp_res
                        if f.get('choices'):
                            for c in f['choices']:
                                if c['label']['zh_Hant_TW'] == v:
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
        return '\n'.join([json.dumps(v) for k, v in out_rows.items()])

    def resource(self, metadata, files):
        reader = csv.DictReader(metadata)
        fields = self.schema['resource_fields']
        for r_i, row in enumerate(reader, start=1):
            out_row = {'package_id': row[u'資料集編號']}
            loc = row[u'網址/檔案名稱']
            if not loc:
                print("#%d: Missing url or file. Skip." % r_i)
                continue
            if loc[0:7] == 'http://' or loc[0:8] == 'https://':
                # url
                out_row['url'] = loc
            elif files:
                # file
                try:
                    out_row['upload'] = open(os.path.join(files, loc), 'rb')
                except IOError:
                    print("#%d: Missing file, skip" % r_i)
                    continue
            for k, v in row.items():
                if not v: continue
                for f in fields:
                    if f.get('label')['zh_Hant_TW'] == k:
                        # encoding
                        if f.get('choices'):
                            for c in f['choices']:
                                if c['label']['zh_Hant_TW'] == v:
                                    v = c['value']
                        out_row[f['field_name']] = v
            self.registry.action.resource_create(**out_row)
