# Image Magic

This dense script can generate and perform operations on image files.

## Generation

The program can generate color or black-and-white images of any size. 

```
usage: xor_img.py gen [-h] [-c] x y Output
```

A 400x300 png image of random pixels:

![Random.png](random.png)

## Operations

The program can perform a bitwise AND, OR, or XOR operation on two input images. 

```
usage: xor_img.py op [-h] [-o Output] File1 operation File2
```

But why would anyone in their right mind ever perform an XOR on two images? Well, to encrypt an image with a secret seed! 

Unencrypted image:

![Unencrypted.png](logo.png)

Now let's perform an XOR on this image and the previous random image! 

```
python "Image Magic.py" op -o output.png logo.png xor random.png
```

![Encrypted.png](encrypted.png)

Without knowing the random seed used to generate the key image, it is nearly impossible to reverse this process to recover the original image.
