from PIL import Image, ImageChops


def compare_images(imga, imgb):

    print("Comparing: ")
    print("        Img_A: "+imga)
    print("        Img_B: "+imgb)

    im1 = Image.open(imga).convert('RGBA')
    im2 = Image.open(imgb).convert('RGBA')
    diff = ImageChops.difference(im1, im2)

    if diff.getbbox():
        print("        Img_A and Img_B are different")
        return False
    else:
        print("        Img_A and Img_B are equal")
        return True
