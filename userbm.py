import os
import sys
import torch
from model import U2NET
import numpy as np
import cv2
from skimage import io, transform
from torch.autograd import Variable
from PIL import Image



def save_output(image_name, output_name, pred, d_dir, type):
    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()
    im = Image.fromarray(predict_np*255).convert('RGB')
    image = io.imread(image_name)
    imo = im.resize((image.shape[1], image.shape[0]))
    pb_np = np.array(imo)
    if type == 'image':
        # Make and apply mask
        mask = pb_np[:, :, 0]
        mask = np.expand_dims(mask, axis=2)
        imo = np.concatenate((image, mask), axis=2)
        imo = Image.fromarray(imo, 'RGBA')

    imo.save(os.path.join(d_dir, output_name))

def removeBackground(imagePath):

    # convert string of image data to uint8
    with open(imagePath, "rb") as image:
        f = image.read()
        img = bytearray(f)

    nparr = np.frombuffer(img, np.uint8)

    if len(nparr) == 0:
        return '---Empty image---'

    # decode image
    try:
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except:
        return "---Empty image---"

    # processing
    image = transform.resize(img, (320, 320), mode='constant')

    tmpImg = np.zeros((image.shape[0], image.shape[1], 3))

    tmpImg[:, :, 0] = (image[:, :, 0]-0.485)/0.229
    tmpImg[:, :, 1] = (image[:, :, 1]-0.456)/0.224
    tmpImg[:, :, 2] = (image[:, :, 2]-0.406)/0.225

    tmpImg = tmpImg.transpose((2, 0, 1))
    tmpImg = np.expand_dims(tmpImg, 0)
    image = torch.from_numpy(tmpImg)

    image = image.type(torch.FloatTensor)
    image = Variable(image)

    d1, d2, d3, d4, d5, d6, d7 = net(image)
    pred = d1[:, 0, :, :]
    ma = torch.max(pred)
    mi = torch.min(pred)
    dn = (pred-mi)/(ma-mi)
    pred = dn

    CURRDIR = os.getcwd()

    save_output(imagePath, 'output.png', pred, CURRDIR, 'image')
    return "---Success---"

if __name__ == "__main__":
    # ------- Load Trained Model --------
    print("---Loading Model---")
    model_name = 'u2net'
    model_dir = os.path.join(model_name + '.pth')
    net = U2NET(3, 1)
    if torch.cuda.is_available():
        net.load_state_dict(torch.load(model_dir))
        net.cuda()
    else:
        net.load_state_dict(torch.load(model_dir, map_location='cpu'))

    # ----------- Get Image ---------------

    # imgPath = "D:\\ImageBackgroundRemover\\demo.jpg" 
    imgPath = sys.argv[1]

    # --------- remove background 

    status = removeBackground(imgPath)
    print(status)
