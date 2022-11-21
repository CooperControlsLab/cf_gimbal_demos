import yaml

x={'cf':{
    'address' : 'radio://0/100/2M/E7E7E7E702',
    'params':{
        'pid_rate':{
            'roll_kp'       : 0,
            'roll_ki'       : 0,
            'roll_kd'       : 0,
            'pitch_kp'      : 0,
            'pitch_ki'      : 0,
            'pitch_kd'      : 0,
            'yaw_kp'        : 0,
            'yaw_ki'        : 0,
            'yaw_kd'        : 0,
            'rateFiltEn'    : 0,
            'omxFiltCut'    : 0,
            'omyFiltCut'    : 0,
            'omzFiltCut'    : 0,
        },
        'pid_attitude':{
            'roll_kp'       : 0,
            'roll_ki'       : 0,
            'roll_kd'       : 0,
            'pitch_kp'      : 0,
            'pitch_ki'      : 0,
            'pitch_kd'      : 0,
            'yaw_kp'        : 0,
            'yaw_ki'        : 0,
            'yaw_kd'        : 0,
            'yawMaxDelta'   : 0,
            'attFiltEn'     : 0,
            'attFiltCut'    : 0,
        }
    }}}

key_sequence = ['cf','params']
searches = ['pid_rate', 'pid_attitude']


def get_param_strings(d, strip_keys, param_class_keys):
    temp = d
    keys = []
    # Strip dictionary down to search keys only left
    for k in strip_keys:
        if temp[k] is not None:
            temp = temp[k]
    
    # Get list of keys in search keys
    param_strings = []
    for s in param_class_keys:
        if temp[s] is not None:
            name0 = s
            keys = list(temp[s])
            for k in keys:
                param_strings.append(str(name0) + '.' + str(k))
    return param_strings
        # make list of strings of full parameter names
    
strings = get_param_strings(x, key_sequence, searches)
print(strings)
print(type(x['cf']['address']))
# d = yaml.dump(x, open('dump.yaml','w'), default_flow_style=False, sort_keys=False)
