from PIL import Image
import sys

if (len(sys.argv) != 4):
    exit(-1)

[q,w,e] = sys.argv[1::]
a = Image.open(q)
b = Image.open(w)

if (not ((a.mode and b.mode) == "RGB" and a.height == b.height and a.width == b.width)):
    exit(-2)

c = Image.new(a.mode, (a.width, a.height))

a_data = a.getdata()
b_data = b.getdata()
c_data = []

for i in range(0, len(a_data)):
    c_data.append((a_data[i][0] ^ b_data[i][0],
                   a_data[i][1] ^ b_data[i][1],
                   a_data[i][2] ^ b_data[i][2]))
c.putdata(c_data)
c.save(e)
