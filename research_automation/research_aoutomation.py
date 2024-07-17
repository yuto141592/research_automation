from PIL import Image
import os
import cv2 as cv
import numpy as np

def align(path, new_path):
    if os.path.exists(path) == True:
        img = Image.open(path)
        img.save(new_path, dpi = (200, 200))
        img.close

def add_margin(img, width, height, top, right, bottom, left, color):
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(img.mode, (new_width, new_height), color)
    result.paste(img, (left, top))
    return result

def resize_image(path, path2):
    if os.path.exists(path) == True:
                            
        img = Image.open(path)
        width, height = img.size

        right = int((3402 - width)/2)
        left = right
        top = int((2646 - height)/2)
        bottom = top
        color = (0, 0, 0)
        im_new = add_margin(img, width, height, top, right, bottom, left, color)
        im_new.save(path2, dpi = (200, 200))
        img.close()

        img2 = Image.open(path2)
        img_resize = img2.resize((1024, 796))
        img_resize.save(path2, dpi = (200, 200))
        img2.close()

#A : ウェルの番号
#B : スライドガラスの番号
#C : 切片の番号
A = [1, 2, 3, 4, 5, 6]
B = [1, 2, 3]
C = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for a in A:
    for b in B:
        for c in C:
            path = './raw_img/well{}-{}-{}.jpg'.format(a, b, c)
            path2 = './resize/well{}_{}_{}.jpg'.format(a, b, c)
            FRpath = './raw_img/well{}-{}-{}_FR.jpg'.format(a, b, c)
            FRpath2 = './resize/well{}_{}_{}_FR.jpg'.format(a, b, c)
            DAPIpath = './raw_img/well{}-{}-{}_DAPI.jpg'.format(a, b, c)
            DAPIpath2 = './resize/well{}_{}_{}_DAPI.jpg'.format(a, b, c)
            resize_image(path, path2)
            resize_image(FRpath, FRpath2)
            resize_image(DAPIpath, DAPIpath2)


            d = a + 72 * (b - 1) + 6 * (c - 1)

            new_path = './alignment/{}.jpg'.format(d)
            new_path_FR = './alignment_FR/{}_FR.jpg'.format(d)
            new_path_DAPI = './alignment_DAPI/{}_DAPI.jpg'.format(d)

            align(path2, new_path)
            align(FRpath2, new_path_FR)
            align(DAPIpath2, new_path_DAPI)

            img_path = new_path
            print(img_path, a, b, c, d)
            path2 = './mask_img/{}.jpg'.format(d)

            lower_value = 90
            M = 0
            m = 1
            while M < 2 * m and lower_value < 160:
                lower_value += 10
                img = cv.imread(img_path)

                hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

                lower = np.array([155,170,lower_value])
                upper = np.array([180,255,255])

                frame_mask = cv.inRange(hsv, lower, upper)
    
                dst = cv.bitwise_and(img, img, mask=frame_mask)
                cv.imwrite(path2, dst)

                img = Image.open(path2)
                img2 = cv.imread(img_path)
                img3 = cv.imread(path2)

                width, height = img.size

                q = int(img.size[0])
                r = int(img.size[1])
                Q = int(q / 10)
                R = int(r / 10)

                List = []
                for k in range(1,Q):
                    for l in range(1,R):
                        value = img.getpixel((10 * k, 10 * l))[2]
                        List.append(int(value))

                end = int((q * r) / 100)
                left_end = int((49/100) * end)
                right_start = int((51/100) * end)

                left_list = sorted(List[1 : left_end], reverse=True)
                right_list = sorted(List[right_start : end], reverse=True)

                left_sig = sum(left_list[1 : 16])
                right_sig = sum(right_list[1 : 16])

                M = max(left_sig, right_sig)
                m = min(left_sig, right_sig)

            if left_sig > right_sig:
                img_flip_lr = cv.flip(img2, 1)
                img_flip_lr2 = cv.flip(img3, 1)
                cv.imwrite(img_path, img_flip_lr)
                cv.imwrite(path2, img_flip_lr2)
                img = Image.open(img_path)
                img.save(img_path, dpi = (200, 200))
                img.close()
         



                