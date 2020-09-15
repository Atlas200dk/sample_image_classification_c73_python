import os
import cv2
import numpy as np
import argparse
import sys
sys.path.append('..')
from model_processor import ModelProcessor
import acl
from acl_resource import AclResource

MODEL_PATH = "./model/googlenet.om"
DATA_PATH = './data/dog1.jpg'

def execute(model_path, frames_input_src, output_dir):
    

    ## Initialization ##
    #initialize acl runtime 
    acl_resource = AclResource()
    acl_resource.init()
    
    ## Prepare Model ##
    # parameters for model path and model inputs
    model_parameters = {
        'model_dir': model_path,
        'width': 224, # model input width      
        'height': 224, # model input height
    }
    # perpare model instance: init (loading model from file to memory)
    # model_processor: preprocessing + model inference + postprocessing
    model_processor = ModelProcessor(acl_resource, model_parameters)

    ## Get Input ##
    # Read the image input using OpenCV; OpenCV imread as BGR
    img_original = cv2.imread(args.frames_input_src)

    ## Model Prediction ##
    # model_processor.predict: processing + model inference + postprocessing
    # category: the category with hightest prob.
    category = model_processor.predict(img_original)

    # Save the detected results
    cv2.putText(img_original,category,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.imwrite(os.path.join(args.output_dir, 'Result.jpg'), img_original)
    

if __name__ == '__main__':   
    description = 'Load a model for classification'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--model', type=str, default=MODEL_PATH)
    parser.add_argument('--frames_input_src', type=str,default=DATA_PATH, help="Directory path for image")
    parser.add_argument('--output_dir', type=str, default='./outputs', help="Output Path")

    args = parser.parse_args()
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    execute(args.model, args.frames_input_src, args.output_dir)
