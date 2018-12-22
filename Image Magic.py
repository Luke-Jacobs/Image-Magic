from PIL import Image
import random
import argparse
import math


class steganography:

    def genrandcoords(res, genr):
        x = genr.randrange(0, res[0])
        y = genr.randrange(0, res[1])
        c = genr.randrange(0, 3)
        return (x, y, c)

    def ntocoord(n, res):
        y = math.floor(n / res[0])
        x = ((n / res[0]) - y) * res[0]
        return (x, y)

    def coordton(coord, res):
        return (coord[1] * res[1]) + coord[0]

    def encodebit(n, sbyte, i):
        a = '{0:08b}'.format(ord(sbyte))
        if a[i] == "1":
            return n | 1
        else:
            return n & 0

    def lsbseed(filename, seed, data, function):
        genr = random.Random()
        genr.seed(seed)
        if function == "e":
            convtoRGB(filename)
            img = Image.open(filename)
            res = (img.width, img.height)
            img2 = Image.new("RGB", res)
            data += "\x00"
            for i in range(0, len(data)):
                for i2 in range(0, 8):
                    r = steganography.genrandcoords(res, genr)
                    pixel = img.getpixel((r[0],r[1]))
                    pixelar = [pixel[0], pixel[1], pixel[2]]
                    pixelar[r[2]] = steganography.encodebit(pixel[r[2]], data[i], i2)
                    img2.putpixel((r[0],r[1]), (pixelar[0], pixelar[1], pixelar[2]))
            img2.save(filename)
            img2.close()
        if function == "d":
            data = ""
            img = Image.open(filename)
            res = (img.width, img.height)
            while (data.find('\x00') == -1):
                byte = ""
                for i in range(0, 8):
                    r = steganography.genrandcoords(res, genr)
                    pixel = img.getpixel((r[0], r[1]))
                    byte += str(pixel[r[2]] & 1)
                data += chr(int(byte, 2))
            return data[:-1:]


def genrandimg(args):
    size = (int(args.x), int(args.y))
    fp = Image.new("RGB", size)
    data = []

    if not args.c:
        for i in range(size[0]*size[1]):
            r = random.choice([0x00, 0xff])
            data.append((r, r, r))
    else:
        for i in range(size[0]*size[1]):
            r = [random.choice(range(0, 256)) for _ in range(0, 3)]
            r = (r[0], r[1], r[2])
            data.append(r)

    fp.putdata(data)
    print("Saving to "+args.o+"...")
    fp.save(args.o)
    fp.close()


def average(filename):
    convtoRGB(filename)
    img = Image.open(filename)
    data = img.getdata()
    rgb = [0, 0, 0]
    res = img.height*img.width
    for a in range(0, 3):
        for b in range(0, res):
            rgb[a] += data[b][a]
    return (rgb[0]//res, rgb[1]//res, rgb[2]//res)


def convtoRGB(filename):
    fp = Image.open(filename)
    if (fp.mode == "RGB"):
        return 0
    fp = fp.convert("RGB")
    fp.save(filename)
    fp.close()
    return 1


def tuple_operation(a, b, op):
    o = []
    for i in range(0, 3):
        if (op=="xor"):
            o.append(a[i] ^ b[i])
        if (op=="and"):
            o.append(a[i] & b[i])
        if (op=="or"):
            o.append(a[i] | b[i])
    return (o[0], o[1], o[2])


def img_operation(args):
    a = args.a
    b = args.b
    o = args.o
    op = args.operation

    convtoRGB(a)
    convtoRGB(b)
    a = Image.open(a)
    b = Image.open(b)

    if (not ((a.mode and b.mode) == "RGB" and a.height == b.height and a.width == b.width)):
        print("Error: the dimensions of the images do not match")
        exit(-1)

    c = Image.new(a.mode, (a.width, a.height))
    a_data = a.getdata()
    b_data = b.getdata()
    c_data = []

    for i in range(0, len(a_data)):
        t_data = tuple_operation(a_data[i], b_data[i], op)
        c_data.append(t_data)
    c.putdata(c_data)
    if (o):
        print("Saving to "+args.o+"...")
        c.save(o)
    else:
        print("Saving to "+args.b+"...")
        c.save(b)
    c.close()


def main():
    parser = argparse.ArgumentParser(description="Perform operations on images")
    subparsers = parser.add_subparsers(help='Functions')
    parser_gen = subparsers.add_parser('gen', help='generator help')
    parser_op = subparsers.add_parser('op', help='operation help')

    parser_op.add_argument("a", help="The first file to input", metavar="File1")
    parser_op.add_argument("operation", help="Either: xor, and, or")
    parser_op.add_argument("b", help="The second file to input (if -o is not specified, the output will be written to this file", metavar="File2")
    parser_op.add_argument("-o", metavar="Output", action="store", required=False, help="Optional output", default=False)
    parser_op.set_defaults(func=img_operation)

    parser_gen.add_argument("x", help="Width of image to generate")
    parser_gen.add_argument("y", help="Height of image to generate")
    parser_gen.add_argument("o", metavar="Output", action="store", help="Required output")
    parser_gen.add_argument("-c", action="store_true", required=False, help="Toggle color mode", default=False)
    parser_gen.set_defaults(func=genrandimg)
    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
