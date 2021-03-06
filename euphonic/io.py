import copy
import json
import os
import numpy as np
from pint import Quantity
from euphonic import ureg


def _to_json_dict(dictionary):
    """
    Convert all keys in an output dictionary to a JSON serialisable
    format
    """
    for key, val in dictionary.items():
        if isinstance(val, np.ndarray):
            if val.dtype == np.complex128:
                val = val.view(np.float64).reshape(val.shape + (2,))
            dictionary[key] = val.tolist()
        elif isinstance(val, dict):
            dictionary[key] = _to_json_dict(val)
    return dictionary


def _from_json_dict(dictionary, type_dict={}):
    """
    For a dictionary read from a JSON file, convert all list key values
    to that specified in type_dict. If not specified in type_dict, just
    uses the default conversion provided by np.array(list)
    """
    for key, val in dictionary.items():
        if isinstance(val, list):
            if key in type_dict:
                if type_dict[key] == tuple:
                    dictionary[key] = [tuple(x) for x in val]
                elif type_dict[key] == np.complex128:
                    dictionary[key] = np.array(
                        val, dtype=np.float64).view(np.complex128).squeeze()
                else:
                    dictionary[key] = np.array(val, dtype=type_dict[key])
            else:
                dictionary[key] = np.array(val)
        elif isinstance(val, dict):
            dictionary[key] = _from_json_dict(val, type_dict)
    return dictionary


def _obj_to_dict(obj, attrs):
    dout = {}
    for attr in attrs:
        val = getattr(obj, attr)
        if isinstance(val, np.ndarray):
            val = np.copy(val)
        elif isinstance(val, list):
            val = val.copy()

        if hasattr(val, 'to_dict'):
            dout[attr] = val.to_dict()
        elif isinstance(val, Quantity):
            dout[attr] = val.magnitude
            dout[attr + '_unit'] = str(val.units)
        else:
            dout[attr] = val
    return dout


def _process_dict(dictionary, quantities={}, optional={}):
    """
    Process an input dictionary for creating objects. Convert keys in
    'quantities' to Quantity objects, and if any 'optional' keys are
    missing, set them to None
    """
    dictionary = copy.deepcopy(dictionary)
    for okey in optional:
        if not okey in dictionary.keys():
            dictionary[okey] = None

    for qkey in quantities:
        val = dictionary.pop(qkey)
        if val is not None:
            val = val*ureg(dictionary.pop(qkey + '_unit'))
        dictionary[qkey] = val
    return dictionary


def _obj_to_json_file(obj, filename):
    """
    Generic function for writing to a JSON file from a Euphonic object
    """
    dout = _to_json_dict(obj.to_dict())
    with open(filename, 'w') as f:
        json.dump(dout, f, indent=4, sort_keys=True)
    print(f'Written to {os.path.realpath(f.name)}')


def _obj_from_json_file(cls, filename, type_dict={}):
    """
    Generic function for reading from a JSON file to a Euphonic object
    """
    with open(filename, 'r') as f:
        obj_dict = json.loads(f.read())
    obj_dict = _from_json_dict(obj_dict, type_dict)
    return cls.from_dict(obj_dict)
