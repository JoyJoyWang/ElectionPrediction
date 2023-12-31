# 来自opencv\sources\samples/python2/opt_flow.py
import cv2 as cv
import numpy as np
import os

es = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))

dir_path=r'C:\Users\Zhuxuanzi Wang\Desktop\csz'
file_ls=os.listdir(dir_path)
compare_matrix=[]

for f in file_ls:
    pt="C:/Users/Zhuxuanzi Wang/Desktop/csz/"+f
    cap = cv.VideoCapture(pt)
    frame1 = cap.read()[1]
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    hsv[..., 1] = 255
    
    # 视频文件输出参数设置
    out_fps = 12.0  # 输出文件的帧率
    fourcc = cv.VideoWriter_fourcc('M', 'P', '4', '2')
    sizes = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
    out1 = cv.VideoWriter(r'E:\\AI结题设计\\output\\output1.avi', fourcc, out_fps, sizes)
    out2 = cv.VideoWriter(r'E:\\AI结题设计\\output\\output2.avi', fourcc, out_fps, sizes)
    
    count=0
    
    summean=[]
    bool0=True
    while bool0==True:
        (ret, frame2) = cap.read()
        if ret==False:
            break
        next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mean0 = np.mean(flow)
    
        mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
    
        bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    
        draw = cv.cvtColor(bgr, cv.COLOR_BGR2GRAY)
        draw = cv.morphologyEx(draw, cv.MORPH_OPEN, kernel)
        draw = cv.threshold(draw, 25, 255, cv.THRESH_BINARY)[1]
    
        contours, hierarchy = cv.findContours(draw.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
        for c in contours:
            if cv.contourArea(c) < 500:
                continue
            (x, y, w, h) = cv.boundingRect(c)
            cv.rectangle(frame2, (x, y), (x + w, y + h), (255, 255, 0), 2)
    
        cv.imshow('frame2', bgr)
    
        cv.imshow('draw', draw)
        cv.imshow('frame1', frame2)
        out1.write(bgr)
        out2.write(frame2)
    
        k = cv.waitKey(200) & 0xff
        if k == 27 or k == ord('q'):
            break
        elif k == ord('s'):
            cv.imwrite('opticalfb.png', frame2)
            cv.imwrite('opticalhsv.png', bgr)
        prvs = next
    
        count+=1
        summean.append(mean0)
        print(count,mean0)
    finalmean=np.mean(summean)
    compare_matrix.append([f,finalmean])
    out1.release()
    out2.release()
    cap.release()
    cv.destroyAllWindows()
    