from PIL import Image
import numpy as np
from collections import Counter
import argparse
import hashlib
import random
import sys

parser = argparse.ArgumentParser(description="Basic steganography. Only takes lowercase a-z and space characters. Built under the assumption of lossless compression.")
parser.add_argument('-i', '--input', dest='infile', action="store", help="Input file")
parser.add_argument('-e', '--encode', dest="code", action="store", help="Code to hide in image")
parser.add_argument('-o', '--output', dest='outfile', action="store", help="Output file")
parser.add_argument('-d', '--decode', dest="code_len", action="store", help="Length of code to extract from image")
parser.add_argument('-s', '--show', dest="show", action="store_true", help="Show images")
parser.add_argument('-p', '--password', dest="password", action='store', help="\"Password\"")
parser.add_argument('-n', '--noise', dest="noise", action='store', help="Add noise when encoding to cover tracks")
#TODO should be able to list encoding from password and image size?
# parser.add_argument('-ls', '--list', dest="list", action='store', help="Provide password and code len and image size (using this flag in format 128,128) to get locations for encoding")
#TODO add map ability
# parser.add_argument('-m', '--map', dest="map", action='store', help="Use custom map for char translation")


args = parser.parse_args()

char_map = {
	"a":(-1, -1, -1),
	"b":(-1, -1, 0),
	"c":(-1, -1, 1),
	"d":(-1, 0, -1),
	"e":(-1, 0, 0),
	"f":(-1, 0, 1),
	"g":(-1, 1, -1),
	"h":(-1, 1, 0),
	"i":(-1, 1, 1),
	"j":(0, -1, -1),
	"k":(0, -1, 0),
	"l":(0, -1, 1),
	"m":(0, 0, -1),
	"n":(0, 0, 0),
	"o":(0, 0, 1),
	"p":(0, 1, -1),
	"q":(0, 1, 0),
	"r":(0, 1, 1),
	"s":(1, -1, -1),
	"t":(1, -1, 0),
	"u":(1, -1, 1),
	"v":(1, 0, -1),
	"w":(1, 0, 0),
	"x":(1, 0, 1),
	"y":(1, 1, -1),
	"z":(1, 1, 0),
	" ":(1, 1, 1)
}

def load_file(filename):
	img = Image.open(filename)
	img = img.convert('RGBA')
	return img

def get_locations(code_len, seed, img_size, blocklist=None):
	locations = []
	random.seed(seed)
	i = 0
	while True:
		x = random.randrange(0,img_size[0])
		y = random.randrange(0,img_size[1])
		#check that changing data wont overflow
		# if not bypass:
		# 	r,g,b,a = ref_color_data[x][y]
		# else:
		# 	r,g,b,a=0,0,0,0
		r,g,b,a = ref_color_data[x][y]
		if (check_color(r) and check_color(g) and check_color(b)):#or bypass
			if blocklist:
				if (x,y) not in blocklist:
					locations.append((x,y))
					i+=1
			else:
				locations.append((x,y))
				i+=1
		if i==code_len:
			break
	return locations

def check_color(color):
	if color==255:
		return False
	elif color==0:
		return False
	else:
		return True

# if args.list:
# 	print(args.list)
# 	l = args.list.split(",")
# 	seed = hashlib.md5(bytes(args.password, 'ascii')).hexdigest()
# 	locations = get_locations(int(args.code_len),seed,(int(l[0]),int(l[1])), bypass=True)
# 	print(locations)
# 	sys.exit()


if args.infile:
	infile = args.infile
	reference_image = load_file(infile)
	orig_size = reference_image.size
	total_points = orig_size[0]*orig_size[1]
	print("Input Image: ", orig_size[0], orig_size[1])
else:
	print("Need infile")
	sys.exit()

code = args.code
outfile = args.outfile

if not args.password:
	print("Using file hash for seed")
	with open(filename, 'rb') as f:
		hexdig = hashlib.md5(f.read()).hexdigest()
	seed = bytes(hexdig, 'ascii')
else:
	print("Using password hash for seed")
	seed = hashlib.md5(bytes(args.password, 'ascii')).hexdigest()
random.seed(seed)

ref_color_data = np.array(reference_image)

#decoding
if args.code_len:
	code_len = int(args.code_len)

	locations = get_locations(code_len, seed, orig_size)
	print("Encoding Locations: ", locations)

	encoded_file = load_file(outfile)
	encoded_data = np.array(encoded_file)

	message = ""
	print("Original RGB data", "Shift", "Encoded Data")
	for i in locations:
		x = i[0]
		y = i[1]
		rdiff = int(encoded_data[...,:-1][x][y][0])-int(ref_color_data[...,:-1][x][y][0])
		gdiff = int(encoded_data[...,:-1][x][y][1])-int(ref_color_data[...,:-1][x][y][1])
		bdiff = int(encoded_data[...,:-1][x][y][2])-int(ref_color_data[...,:-1][x][y][2])
		print(ref_color_data[...,:-1][x][y], (rdiff, gdiff, bdiff), encoded_data[...,:-1][x][y])
		for item in char_map:
			if char_map[item]==(rdiff,gdiff,bdiff):
				message+=item

	print("Decoded message!: "+message)


#Encoding
elif args.code:
	print("Inserting \""+code+"\" into image via pixel manipulation. Using "+str(len(code))+" most common colors")
	locations = get_locations(len(code), seed, orig_size)
	print("Encoding Locations: ",locations)
	j = 0
	print("Location | ", "Original RGB data | ", "Shift", " | Encoded Data")
	for i in locations:
		char = code[j]
		x = i[0]
		y = i[1]
		color = ref_color_data[...,:-1][x][y].copy()
		shift_map = char_map[char]
		shift = (shift_map[0]+color[0], shift_map[1]+color[1], shift_map[2]+color[2])
		ref_color_data[...,:-1][x][y] = shift
		j+=1
		print((x,y),color, (shift_map[0], shift_map[1], shift_map[2]), shift)

	if args.noise:
		noise_num = int(args.noise)
		if noise_num>=orig_size[0]*orig_size[1]-len(code):
			sys.exit("Too much noise!")
		noise_loc = get_locations(noise_num, random.random(), orig_size, locations)
		for loc in noise_loc:
			x = loc[0]
			y = loc[1]
			color = ref_color_data[...,:-1][x][y].copy()
			shift = (random.randrange(-1,2)+color[0], random.randrange(-1,2)+color[1], random.randrange(-1,2)+color[2])

			ref_color_data[...,:-1][x][y] = shift

		print("Added noise in", len(noise_loc), "locations")



	encoded_image = Image.fromarray(ref_color_data)
	if args.show:
		reference_image.show()
		encoded_image.show()
	encoded_image.save(outfile)