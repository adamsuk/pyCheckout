"""
A module used to store any potential function that could be used
in multiple locations.

Functions
    read_json: takes a raw json with data nested in a list and formats it into a dictionary.
"""
import os
import json
import copy

def read_json(json_file, nested_key, sort_key):
    # define empty dictionary
    data={}
    # check file exists
    if os.path.isfile(json_file):
        # open the raw json
        with open(json_file, "r") as f:
            raw_data = json.load(f)
        # error if nested_key not in raw_data
        if nested_key not in raw_data.keys():
            print("Error: unable to find the key '{}' in the file:\n{}".format(nested_key, json_file))
            sys.exit(999)
        # loop over to obtain a sortable dictionary by sort_key
        for raw_item in raw_data[nested_key]:
            # check sort_key exists in item
            if sort_key.lower() not in [key.lower() for key in raw_item.keys()]:
                print("Warning: the following item was not read due to missing the sort_key '{}'".format(sort_key))
                print("   --- {}".format(raw_item))
            else:
                data[raw_item[sort_key].lower()] = raw_item
    return data

def dict_sub_filter(full_dict, filter_list, all_keys_req=False):
    if all_keys_req:
        # check every item in raw_dict exists as an item in full_dict
        if not all([item.lower() in full_dict.keys() for item in filter_list]):
            print("Error: unable to find the following items in the 'prices_dict':")
            print(', '.join(list(set(filter_list) - set(full_dict.keys()))))
            sys.exit(666)
    # obtain a cart dictionary from the raw list
    raw_dict = {item.lower(): filter_list.count(item) for item in set(filter_list)}
    # get a filtered dictionary of self.prices based on the keys in raw_dict
    return raw_dict, {item: props for item, props in copy.deepcopy(full_dict).items() if item in raw_dict.keys()}
