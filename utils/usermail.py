import csv
import sys
import json


class UserMail:
    def __init__(self, users):
        self.users = users

    def get_list(self):
        l = _parse(json.loads(self.users))
        dw = csv.DictWriter(sys.stdout,
                            fieldnames=['display_name', 'email'],
                            delimiter=',',
                            quoting=csv.QUOTE_ALL)
        dw.writeheader()
        for entry in l:
            dw.writerow(entry)

def _parse(s):
    return [{ k: entry[k] for k in ['display_name', 'email'] } \
            for entry in s if entry['state'] == 'active']
