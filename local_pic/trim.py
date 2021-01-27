from skimage import io
def corp_margin(img):
    img2=img.sum(axis=2)
    (row,col)=img2.shape
    row_top=0
    raw_down=0
    col_top=0
    col_down=0
    for r in range(0,row):
            if img2.sum(axis=1)[r]<700*col:
                    row_top=r
                    break

    for r in range(row-1,0,-1):
            if img2.sum(axis=1)[r]<700*col:
                    raw_down=r
                    break

    for c in range(0,col):
            if img2.sum(axis=0)[c]<700*row:
                    col_top=c
                    break

    for c in range(col-1,0,-1):
            if img2.sum(axis=0)[c]<700*row:
                    col_down=c
                    break

    new_img=img[row_top-5:raw_down+5,col_top-100:col_down+25,0:3]
    return new_img
if __name__ == "__main__":
    im = io.imread('result.png')
    print(1)
    img_re = corp_margin(im)
    io.imsave('result1.png',img_re)
