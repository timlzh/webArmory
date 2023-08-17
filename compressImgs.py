#coding:utf-8
from PIL import Image
from tqdm import tqdm
import os

def toMB(size):
    return size/1024/1024

#图片压缩批处理  
def compressImage(srcPath):
    totSrcSize=0
    totDstSize=0
    file_count = sum(len(files) for _, _, files in os.walk(srcPath))
    with tqdm(total=file_count) as pbar:  # Do tqdm this way
        for root, dirs, files in os.walk(srcPath):
            for file in files:
                pbar.update(1)
                if file.endswith(".jpg") or file.endswith(".png"):
                    try:
                        srcFile=os.path.join(root,file)
                        srcSize=toMB(os.path.getsize(srcFile))
                        totSrcSize+=srcSize
                        # print(srcFile)
                        sImg=Image.open(srcFile)
                        w,h=sImg.size
                        dImg=sImg.resize((int(w/2),int(h/2)),Image.Resampling.LANCZOS)
                        dImg.save(srcFile, quality=95)
                        dstSize=toMB(os.path.getsize(srcFile))
                        totDstSize+=dstSize
                        tqdm.write(f"[{file}] {srcSize:.2f} -> {dstSize:.2f} {(srcSize - dstSize)/srcSize*100:.2f}%")
                    except Exception as e:
                        # tqdm.write(f"Error! [{file}] {e}")
                        # cannot write mode RGBA as JPEG
                        if "cannot write mode RGBA as JPEG" in str(e):
                            try:
                                sImg=sImg.convert('RGB')
                                sImg.save(srcFile, quality=95)
                                dstSize=toMB(os.path.getsize(srcFile))
                                totDstSize+=dstSize
                                tqdm.write(f"[{file}] {srcSize:.2f} -> {dstSize:.2f} {(srcSize - dstSize)/srcSize*100:.2f}%")
                            except Exception as e:
                                tqdm.write(f"Error! [{file}] {e}")
                        else:
                            tqdm.write(f"Error! [{file}] {e}")
    print(f"Total: {totSrcSize:.2f} -> {totDstSize:.2f} {(totSrcSize - totDstSize)/totSrcSize*100:.2f}%")

if __name__=='__main__':  
    compressImage("./site")