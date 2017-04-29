import os
from colorthief import ColorThief
import argparse
import re
import math
import shutil

#color_thief = ColorThief('008887_000.jpg')
#dominant_color = color_thief.get_color(quality=1)


parser = argparse.ArgumentParser(description="Split cat dataset into folder by color.")
parser.add_argument("--path", required=True, help="Path to image folder" )
args = parser.parse_args()
fp_dir = args.path
fps = [f for f in os.listdir(fp_dir) if os.path.isfile(os.path.join(fp_dir, f))]
fps = [os.path.join(fp_dir, f) for f in fps]
fps_img = [fp for fp in fps if re.match(r".*\.jpg$", fp)]

color_map = {
	'black': (0,0,0),
	'white': (183,178,172),
	'golden': (188,130,78),
	'grey': (178,174,166)
}

def color_distance(color1, color2):
	r1,g1,b1 = color1
	r2,g2,b2 = color2
	dist = math.pow(r1-r2,2) + math.pow(g1-g2,2) + math.pow(b1-b2,2)
	return dist

def find_closest_color(dominant_color):
	closest_k = 'black'
	closest_v = '1000000000' #some huge num
	for k,v in color_map.iteritems():
		d = color_distance(dominant_color,v)
		if d < closest_v:
			closest_v = d
			closest_k = k
	return (closest_k,closest_v)

#print color_map
#print color_distance((0,0,0),(255,255,255))

def create_color_folders():
	for k,v in color_map.iteritems():
		folder  = os.path.join(fp_dir, k)	
		if not os.path.exists(folder):
			os.makedirs(folder)

def cp_color_folder(file, color):
	folder  = os.path.join(fp_dir, color)
	shutil.copy(file,folder)

create_color_folders()

for f in fps_img:
	color_thief = ColorThief(f)
	dominant_color = color_thief.get_color(quality=1)
	print (f + " " + str(dominant_color))
	color,distance =  find_closest_color(dominant_color)
	print (str(color) +  " " + str(distance))
	cp_color_folder(f,color)

