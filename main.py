from PIL import Image
import sys

if (len(sys.argv) != 4):
    exit(-1) #exit if the program has not received 3 params

[q,w,e] = sys.argv[1::] #filename1, filename2, outputFile
a = Image.open(q)
b = Image.open(w)

if (not ((a.mode and b.mode) == "RGB" and a.height == b.height and a.width == b.width)):
    exit(-2)

c = Image.new(a.mode, (a.width, a.height))

a_data = a.getdata() #get image data as bytes
b_data = b.getdata()
c_data = [] #buffer for output image data

for i in range(0, len(a_data)): #do the (regrettably inefficient) xor operation on each pixel
    c_data.append((a_data[i][0] ^ b_data[i][0],
                   a_data[i][1] ^ b_data[i][1],
                   a_data[i][2] ^ b_data[i][2]))
c.putdata(c_data)
c.save(e)
