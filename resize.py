from importlib.resources import path
from PIL import Image, ImageOps
import sys

  



def padding(img, pad):
    width, height = img.size
    new_width = width + pad[0]*2
    new_height = height + pad[0]*2
    result = Image.new(img.mode, (new_width, new_height), (0, 0, 255))
    result.paste(img, pad)
    return result


def resize_with_padding(img, expected_size):
    img.thumbnail((expected_size[0], expected_size[1]))
    # My image is a 200x374 jpeg that is 102kb large
    # I downsize the image with an ANTIALIAS filter (gives the highest quality)
    img = img.resize(expected_size,Image.ANTIALIAS)
    return padding(img, (50,50))




if __name__ == "__main__":
    # for arg in sys.argv:
                    
    img = Image.open(sys.argv[1])
    print(img)
    img = resize_with_padding(img, (300, 300))
    print(img.size)
    img.show()
    img.save("resized_img.jpg")

    # img = Image.open("C:\\Users\\dhanr\\Downloads\\UN0387571.jpg")
    # print(img)
    # img = resize_with_padding(img, (300, 300))
    # print(img.size)
    # img.show()
    # img.save("C:\\Users\\dhanr\\Downloads\\resized_img.jpg")