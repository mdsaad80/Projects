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
import picamera
from PIL import Image
import json
import time
import math
import os
import json
import sys
from time import sleep
from fractions import Fraction as F

 
def main():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = F(1 , 2)
        camera.start_preview()
        for filename in camera.capture_continuous('img{counter:03d}.jpg'):
            result=[]
            #time.sleep(1)
            print('Captured video stream as frame with name %s' % filename)
            path = "/home/pi/Desktop/Apna/%s" % filename
            with open(path, 'rb') as fp:
                response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                files=dict(upload=fp),
                headers={'Authorization': 'Token ' + '90ab0162c21a21e1147936f45c7566ecd0ce7c8a'})
                result.append(response.json())
                if result:    
                    print(response.json())
                    with open('data.json', 'w') as outfile:
                        json.dump(result, outfile)
                        header = {}
                        #print(path)
                        new_plate = result[0]['results'][0]['plate']
                        print(new_plate)
                        try:
                            req = requests.get("http://192.168.43.224:5000/api/numberplate/by_number/"+new_plate, headers=header, )
                        except requests.exceptions.RequestException as e:  # This is the correct syntax
                            print(e)
                            sys.exit(1)

                        print(req.status_code, req.reason)
                        recieved_data  = req.json()
                        if recieved_data:
                            print("Offender Vehicle has been Detected with plate no " + new_plate+ "at the time " +time.asctime( time.localtime(time.time()) ) )
                            
                        #print(recieved_data)
                        if not recieved_data:
                            payload = {"plate_number": result[0]['results'][0]['plate'], "camera_id":'1234'}
                            fin = open(path, 'rb')
                            files = {'plate_image': fin}
                            try:
                                req = requests.post("http://192.168.43.224:5000/api/numberplate/add", headers=header, data= payload, files = files )
                            except requests.exceptions.RequestException as e:
                                print(e)
                                sys.exit(1)
                            print(req.status_code, req.reason)
            os.remove("%s" %filename)
            #print(json.dumps(result, indent=2))
    camera.stop_preview()     

if __name__ == '__main__':
    main()
        

