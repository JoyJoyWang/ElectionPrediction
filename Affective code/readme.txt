===
情绪识别

---
##文件描述
*train.py: 情绪识别训练模块，训练好的模型参数放于/recoder文件夹中[不用处理]

**test.py: 情绪识别模块**

*./img: 输入面部图像存放，尺寸不要求统一，最好是224*224.  test.py的输入
*./recoder: 训练好的模型 ./[04-24]-[16-58]-model_best.pth
*./save: 预测输出，test.py的输出

# 运行 test.py
python test.py --source './code/img' --save_path './code/save' --model_path './code/recoder/[04-24]-[16-58]-model_best.pth'

#自己修改--source, --save_path,--model_path的绝对路径

#描述
--source：存放输入image的文件夹，或图像如：'./code/img/test_0107_aligned.jpg' 

--save_path： 情绪类别的预测输出
	*result.csv：img_path，pred_emotion，pred_class，pred_class_probability，arousal，valence
	*xx.img: 预测输出--情绪类别、唤醒效价值

--model_path：加载预训练的模型参数