# python-steganography
Basic Steganography Tool

## Requirements


## Usage
This was just a weekend project do not use this tool in any serious fashion for hiding/storing data. Aside from the obvious limitations (only can encode [a-z] plus space characters) that the process of encoding is documented here means it would be pretty easy to reverse engineer.

### Encoding
The below command takes an input PNG `pfp1.png` (also provided in the repo), a "password" of `test`, the data to be encoded `abc`.

Using the `md5hash` of the "password" the program selects `n` number of locations to encode the bytes of data. `n` here is determined by the length of the data to encode.

At each location the program maps the character into a three digit code provided in `char_map` on line 19. The each digit of the code has three different values possible (-1,0,1), this **tr**inary dig**it** (trit) is then used to change the RGB values at the selected locations. 

`python3 stegano.py -p test -i pfp1.png -o pfpout.png -e abc`

As one might be able to guess this method alone leaves it open to a number of different tracking techniques. Provided in this repo is `compare.py` which will find all of the different pixels between two images. Simply using the above method for encoding leaves the data very easily accessible (assuming that the cracker has access to the original file).

Running `python3 compare.py pfp1.png pfpout.png` returns the locations and values of the shifts, but does not translate as a cracker could not assume that you are using the same `char_map`
#### compare.py output
```bash
Input Image:  2048 2048
Comparison Image:  2048 2048
Images same size proceeding
Diff at: (672, 1126) [249 162   5 255] [ -1 -1 -1 ] [248 161   4 255]
Diff at: (898, 1533) [249 162   5 255] [ -1 -1 1 ] [248 161   6 255]
Diff at: (1253, 670) [199  44  22 255] [ -1 -1 0 ] [198  43  22 255]
Total number of diffs found:  3
```

To counter this there is the `-n` or `--noise` flag which will choose a given number of locations (up to number of pixels in image - code length) at which to perform a similar operation to the encoding done above but with random values (still trit values). Then sifting out the irrelevant pixel shifts becomes more difficult without knowing the seed used to select the locations (password or file hash as described above). 

You can probably figure out a way to get the encoding locations using only the password and image size but it gets complicated because the program checks that the RGB values aren't `0` or `255` in order to avoid an overflow scenario. I left some of my code attempting to do this in the script if anyone is curious.


### Decoding
The below command decodes the above command back into the original data. 

`python3 stegano.py -p test -i pfp1.png -o pfpout.png -d 3`

It does this by getting the locations the same way the encoding portion of the program does and comparing them to the original, taking that change and looking it up in the `char_map`.

If the password is different the output of the command will be all "n"s unless it is able to find the changes or the noise by random chance. The reason for this is clear if you look at the `char_map` which has `(0, 0, 0)` mapped to `n`. Meaning if the program tries to compare a point that has been unchanged the result will be `(0, 0, 0)`.

## `sig` script
Small script from another project that I also found useful here. Takes a file extension as the only option at gets the image signature (using imagemagcik's `identify`) and prints them out.

### Improvements
Obviously expanding the number of characters available. I kept away from changing transparency as I think that a lot of sites probably totally strip that out when uploading. Probably colud get away with changing the colors by more than one per channel.

I initially started the program looking for the most common colors and altering those across the picture as I figured (knowing nothing about compression nitty gritty) that larger chunks of an image that are the same color would probably stay more or less the same under compression.

I know that there is a whole field of study about this kind of thing but I didn't know what it was called and wanted to see what my solution/implementation would look like before consulting reference materials.


# Bonus points
Bonus points if any one is able to find what message I hid in the `pfpout.png`.

I'll give you one hint and say that you need to read a book.