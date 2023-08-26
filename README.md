# ElectionPrediction
本课题爬取了台湾地区6市候选人选前之夜视频数据，筛选后剪辑为时长1秒、帧数为30的视频文件共计868条。主要基于Farneback算法计算稠密光流，具体算法如下：
##1 光流分析的预处理操作
调用OpenCV库的VideoCapture函数，通过视频解码器来解码视频文件，并将解码后的帧返回。
将输入的连续帧图像转换为灰度图像，这可以减少计算量并保留足够的图像特征。转换后的灰度图像存储在变量prvs中，作为光流法分析的起始帧。具体通过“prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)”实现：frame1是当前帧的彩色图像，cv.cvtColor函数用于进行颜色空间转换，cv.COLOR_BGR2GRAY指定了颜色空间转换的方式，将彩色图像转换为灰度图像。
创建一个用于可视化光流的Hue-Saturation-Value（HSV）图像，具体通过“hsv = np.zeros_like(frame1); hsv[..., 1] = 255”实现：np.zeros_like(frame1)创建了一个和frame1具有相同维度的全零数组，即创建了一个和当前帧相同大小的图像。hsv是一个用于存储Hue（色调）、Saturation（饱和度）和Value（明度）的图像。hsv[..., 1] = 255将hsv图像的Saturation通道设置为最大值255，这样在后续的光流可视化中，光流向量会以全彩色表示。
##2 建立calcOpticalFlowFarneback函数近似光流场
对于每个像素位置，选择一个固定大小的局部窗口（例如15x15的窗口），将该窗口内的像素视为局部区域。在该局部区域中，通过计算像素灰度值的二阶导数，获取局部区域的空间梯度信息。这些空间梯度信息用于构建光流场的局部模型。
利用这些导数值，构建一个二维多项式模型来近似描述局部区域内的光流场变化。通常使用二阶多项式，即考虑平移、旋转和缩放。通过在局部区域内最小化光流误差的方法（如最小二乘法），拟合二维多项式模型的系数。通过对空间梯度信息进行加权，可以估计多项式模型的系数。使用得到的多项式模型，通过计算多项式的根，得到局部区域内每个像素位置的光流向量。
重复上一步骤，对图像中的每个像素位置都进行多项式展开，从而得到整个图像的光流场估计。对于稠密光流场，使用插值方法来计算非整数像素位置的光流向量，这样可以得到更平滑的光流场结果。
##3 批量计算视频光流强度
接下来进行相邻帧的光流值计算，并计算每个视频（30帧）的平均光流强度，并对所有视频进行批量计算：
进入一个循环，即视频仍有帧可读取。
使用cap.read()函数读取视频的下一帧。如果返回值ret为False，表示视频已经读取完毕，退出循环。
将当前帧转换为灰度图像，使用cv.cvtColor函数将frame2从BGR颜色空间转换为灰度图像。
使用calcOpticalFlowFarneback函数计算当前帧和上一帧之间的光流。其中，prvs为上一帧灰度图像，next为当前帧灰度图像。
通过对光流矢量求平方和的平均值，得到当前帧的光流强度均值。
将当前帧设置为下一次循环的上一帧，即将next赋值给prvs。
存储光流强度均值：将当前帧的光流强度均值添加到summean列表中。
视频读取完毕后，计算所有帧的光流强度均值的平均值finalmean。
将视频文件名和光流强度均值的结果存储在compare_matrix列表中。
释放视频捕获对象cap，关闭所有打开的窗口，将结果存储。
##4 光流可视化并标记运动
使用cv.cartToPolar函数将光流向量的x和y分量转换为极坐标形式，得到光流的幅值(mag)和角度(ang)。
将角度(ang)映射到HSV颜色空间的色调通道(hsv[..., 0])，以便将角度信息表示为颜色。通过将角度乘以180并除以π乘2来进行映射。
使用cv.normalize函数将光流的幅值(mag)归一化到0-255的范围，并存储在HSV颜色。使用cv.cvtColor函数将HSV图像(hsv)转换为BGR图像(bgr)。
将BGR图像转换为灰度图像(draw)，然后应用形态学开运算(cv.morphologyEx)进行图像处理，使图像中的噪声减少，并保留运动物体的结构。
使用cv.threshold函数对灰度图像进行阈值处理，将灰度值大于阈值的像素置为255，小于等于阈值的像素置为0，生成二值图像(draw)。
使用cv.findContours函数在二值图像中寻找轮廓，得到轮廓列表(contours)和轮廓的层级结构(hierarchy)。
遍历每个轮廓，对于面积小于500的轮廓，跳过；对于面积大于等于500的轮廓，获取其边界框的坐标并使用矩形框标记在原始图像(frame2)上。
使用cv.imshow函数显示处理后的图像，包括光流可视化图像(bgr)、二值图像(draw)和原始图像(frame2)。将光流可视化图像(bgr)和原始图像(frame2)写入视频文件。
