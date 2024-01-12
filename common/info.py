import os


self_id = 6466094355
creator = 5273618487
administrators = [345060487, creator]
version = '1.5.0.5'
username = 'rbevbot'
self_name = 'Kuma Eval'

if os.name == 'nt':
    debug_mode = True
    channel = 'local'
else:
    debug_mode = False
    channel = 'cloud'
