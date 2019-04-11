#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import argparse
import requests
from PIL import Image
import json
import time
import math
import cv2
import os
import json

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Read license plates from images and output the result as JSON.',
        epilog='For example: python plate_recognition.py --api MY_API_KEY "/path/to/vehicle-*.jpg"')
    parser.add_argument('--api', help='Your API key.', required=True)
    parser.add_argument('FILE', help='Path to vehicle image or pattern.')
    return parser.parse_args()


def main():
    #args = parse_arguments()
    cap = cv2.VideoCapture(0)
    frameRate = cap.get(5)
    print(frameRate)
    seconds=60
    multiplier=frameRate*seconds
    x=1
    while (cap.isOpened()):                                            
            frameId = int(round(cap.get(1)))                             #current frame number
            print(frameId)
            ret, frame = cap.read()
            if (ret != True):
                break
            result = []
            if (frameId % multiplier == 0):
                #cv2.imshow('image', frame)
                filename = 'frameId' +  str(int(x)) + ".jpg"
                cv2.imwrite(filename, frame)
                time.sleep(1)
                #print('Reading frame %s' % frameId)
                path = "C:/Users/Mohammad/Desktop/New folder/api based/apiloop/%s" % filename
                with open(path, 'rb') as fp:
                    response = requests.post(
                    'https://api.platerecognizer.com/v1/plate-reader/',
                    files=dict(upload=fp),
                    headers={'Authorization': 'Token ' + '90ab0162c21a21e1147936f45c7566ecd0ce7c8a'})
                    result.append(response.json())
                    print(json.dumps(result, indent=2));
                    #print(path)
                    #time.sleep(1)
                    with open('data.json', 'w') as outfile:
                        json.dump(result, outfile)
                os.remove("%s" %filename)
                x+=1
                #frameId+=1
                time.sleep(1)
            #print(json.dumps(result, indent=2))
    cap.release()
if __name__ == '__main__':
    main()
