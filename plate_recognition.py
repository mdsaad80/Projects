#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import argparse
import requests
import json
import time



def main():
    #args = parse_arguments()
	
    result = []
    paths = glob.glob("C:/Users/Mohammad/Desktop/New folder/api based/new/*.jpg")
	
    if len(paths) == 0:
        print('File {} does not exist.')
        return
    for path in paths:
        with open(path, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                files=dict(upload=fp),
                headers={'Authorization': 'Token ' + '90ab0162c21a21e1147936f45c7566ecd0ce7c8a'})
            result.append(response.json())
        time.sleep(1)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
