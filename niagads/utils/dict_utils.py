""" library of object / dictionary / hash manipulation functions """

import json
import warnings
from collections import abc
from niagads.utils.string_utils import is_float, is_integer, xstr
import niagads.utils.array_utils as array_utils


def get(obj, attribute, default=None, errorAction="fail"):
    """
    retrieve attribute if in dict
    Args:
        obj (dict): dictionary object to query
        attribute (string): attribute to return
        default (obj): value to return on KeyError. Defaults to None
        errorAction (string, optional): fail or warn on KeyError. Defaults to False
        
    Returns:
        the value of the attribute or the supplied `default` value if the attribute is missing  
    """
    if errorAction not in ['warn', 'fail', 'ignore']:
        raise ValueError("Allowable actions upon a KeyError are `warn`, `fail`, `ignore`")
    
    try:
        return obj[attribute]
    except KeyError as err:
        if errorAction == 'fail':
            raise err
        elif errorAction == 'warn':
            warnings.warn("KeyError:" + err, RuntimeWarning)
            return default
        else:
            return default


def drop_nulls(obj):
    """ find nulls and remove from the object """
    if isinstance(obj, list):
        array_utils.drop_nulls(obj)
    if isinstance(obj, dict):
        return {k: v for k, v in obj.items() if v}
    

def dict_to_info_string(obj):
    """ wrapper for dict_to_string (semantics )"""
    return dict_to_string(obj, '.')


def dict_to_string(obj, nullStr):
    """ translate dict to attr=value; string list"""
    pairs = [ k + "=" + xstr(v, nullStr=nullStr) for k,v in obj.items()]
    pairs.sort()
    return ';'.join(pairs)


def deep_update(d, u):
    """! deep update a dict
    based on https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth/60321833
    answer: https://stackoverflow.com/a/3233356 
    but may not handle all variations

        @param d             source dict to be updated
        @param u             overrides
        @returns             the deep updated source dict
    """
    for k, v in u.items():
        if isinstance(v, abc.Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d



def convert_str2numeric_values(cdict, nanAsStr=True, infAsStr=True):
    """!  converts numeric values in dictionary stored as strings 
    to numeric

        @param cdict             dictionary to conver
        @param nanAsStr          treat NaN/nan/NAN as string?
        @returns                 the converted dictionary
    """
    for key, value in cdict.items():
        if str(value).upper() == 'NAN' and nanAsStr:
            # is_float test will be true for NaN/NAN/nan/Nan etc
            continue
        if 'inf' in str(value).lower() and infAsStr:
            # is_float test will be true for Infinity / -Infinity
            continue
        if is_float(value): # must check float first b/c integers are a subset
            cdict[key] = float(value)
        if is_integer(value):
            cdict[key] = int(value)

    return cdict