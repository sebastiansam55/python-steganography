from PIL import Image
import numpy as np
from collections import Counter
import argparse
import hashlib
import random
import sys

parser = argparse.ArgumentParser(description="Compare two images")
parser.add_argument('infile', help="Input file")
parser.add_argument('outfile', help="Output file")

args = parser.parse_args()

def load_file(filename):
	img = Image.open(filename)
	img = img.convert('RGBA')
	return img

infile = args.infile
outfile = args.outfile

reference_image = load_file(infile)
orig_size = reference_image.size

comp_image = load_file(outfile)
comp_size = comp_image.size


print("Input Image: ", orig_size[0], orig_size[1])
print("Comparison Image: ", comp_size[0], comp_size[1])

ref_color_data = np.array(reference_image)
comp_color_data = np.array(comp_image)

if ref_color_data.shape == comp_color_data.shape:
	print("Images same size proceeding")
else:
	sys.exit("Images not the same size")

diff_num = 0
for x in range(0, orig_size[0]):
	for y in range(0, orig_size[1]):
		ref_point = ref_color_data[x][y]
		comp_point = comp_color_data[x][y]
		if (ref_point!=comp_point).any():
			r1,g1,b1,a1 = ref_point
			r,g,b,a = comp_point
			print("Diff at:", (x,y), ref_point, "[", int(r)-int(r1), int(g)-int(g1), int(b)-int(b1), "]", comp_point)
			diff_num+=1
print("Total number of diffs found: ", diff_num)