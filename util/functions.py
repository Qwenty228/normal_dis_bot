import numpy as np
from urllib import request
import cv2, os
import imageio as iio

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
	return image

def byte_to_image(byte):
  nparr = np.fromstring(byte, np.uint8)
  img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR) #in OpenCV 3.1
  return img_np


def url_gif(url):
  fname = "tmp.gif"
  ## Read the gif from the web, save to the disk
  imdata = request.urlopen(url).read()
  path = "util/assets/"
  open(os.path.join(path ,fname),"wb+").write(imdata)
  #gif = iio.mimread(os.path.join(path ,fname))
  #nums = len(gif)
  #print(nums)
  return path + fname
  
  
def amiya(p):
  url = "https://tenor.com/view/arknights-amiya-totouri-dancing-gif-16422546.gif"
  path = url_gif(url)
  im = iio.get_reader(path)

  s_img = byte_to_image(p)
  #s_img = np.dstack((s_img, np.zeros(s_img.shape[:-1])))
  s_img = cv2.cvtColor(s_img, cv2.COLOR_RGB2BGRA)
  #print(s_img.shape)

  width = 150
  height = int(s_img.shape[0] * width/ s_img.shape[1])
  dim = (width, height)

  s_img = cv2.resize(s_img, dim, interpolation = cv2.INTER_AREA)  

  x_offset=[120 for i in range(9)]
  y_offset=[340, 300, 280, 360, 420 ,350 ,320 ,400, 360]

  writer = iio.get_writer("util/assets/done.gif", fps=30)

  for i, frame in enumerate(im):
      #print(frame.shape)
      h = int(280/y_offset[i] * height)
      s_img = cv2.resize(s_img, (width, h), interpolation = cv2.INTER_AREA)
      frame[y_offset[i]:y_offset[i]+s_img.shape[0], x_offset[i]:x_offset[i]+s_img.shape[1]] = s_img[:frame.shape[0]-y_offset[i], :]
      
      writer.append_data(frame)

  writer.close()
  
def rabbit_hump(p):
  path = url_gif("https://tenor.com/view/rabbit-fuck-humping-gif-17155293.gif")
  im = iio.get_reader(path)
  s_img = byte_to_image(p)
  #s_img = np.dstack((s_img, np.zeros(s_img.shape[:-1])))
  s_img = cv2.cvtColor(s_img, cv2.COLOR_RGB2BGRA)
  #print(s_img.shape)

  width = 80
  height = int(s_img.shape[0] * width/ s_img.shape[1])
  dim = (width, height)

  s_img = cv2.resize(s_img, dim, interpolation = cv2.INTER_AREA)  

  writer = iio.get_writer("util/assets/done.gif", fps=30)
  
  x_offset=[215 for i in range(21)]
  y_offset=[140 for i in range(21)]


  for i, frame in enumerate(im):
      #print(frame.shape)
      i = i if i < len(x_offset) else -1
      frame[y_offset[i]:y_offset[i]+s_img.shape[0], x_offset[i]:x_offset[i]+s_img.shape[1]] = s_img[:frame.shape[0]-y_offset[i], :]
      
      writer.append_data(frame)

  writer.close()