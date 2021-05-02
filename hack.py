#!/usr/bin/env python

import os
import sys
import json
import re

config = os.path.join(os.path.expanduser('~'), '.hack.conf')

def exit(msg):
    print msg
    sys.exit(0)

def main():
    argv = sys.argv
    arg_host = sys.argv[1] if len(sys.argv) > 1 else None
    arg_user = sys.argv[2] if len(sys.argv) > 2 else None
    config_content = ''
    with open(config, 'r') as config_file:
        config_content = config_file.read()
    conf = json.loads(config_content)
    if len(conf.keys()) == 0:
        exit("no hosts found")
    if arg_host is not None:
        found = False
        for host in conf:
            if arg_host in host:
                arg_host = host
                found = True
        if not found:
            exit("host %s not found" % arg_host)
    else:
        max_ip_width = 0
        for host, info in conf.items():
            if len(info['ip']) > max_ip_width:
                max_ip_width = len(info['ip'])
        print '%% 3s  %% %ds  %%s' % max_ip_width % ('idx', 'ip', 'users')
        idx = 1
        for host, info in conf.items():
            print '%% 3d  %% %ds  %%s' % max_ip_width % (idx, info['ip'], ' '.join(info['users'] if 'users' in info else []))
            idx += 1
        arg_idx = raw_input('choose host: ')
        if not re.match(r'^\d+$', arg_idx) or int(arg_idx) <= 0 or int(arg_idx) >= idx:
            exit("invalid index")
        else:
            arg_host = conf.keys()[int(arg_idx) - 1]
    info = conf[arg_host]
    print "host: %s ip: %s" % (arg_host, info['ip'])
    if 'users' not in info:
        info['users'] = [os.environ.get('USER')]
    if arg_user is not None:
        if arg_user not in info['users']:
            exit("invalid user for host [%s], avaliable users are [%s]" % (arg_host, ' '.join(info['users'])))
    elif len(info['users']) == 1:
        arg_user = info['users'][0]
    else:
        print "% 3s %s" % ("idx", "user")
        idx = 1
        for user in info['users']:
            print "% 3d %s" % (idx, user)
            idx += 1
        arg_idx = raw_input('choose user: ')
        if not re.match(r'^\d+$', arg_idx) or int(arg_idx) <= 0 or int(arg_idx) >= idx:
            exit("invalid index")
        else:
            arg_user = info['users'][int(arg_idx) - 1]
    port = info['port'] if 'port' in info else '22'
    print "user: %s" % arg_user
    os.system("ssh %s -l %s -p %s" % (info['ip'], arg_user, port))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print
        pass
