import matplotlib.pyplot as plt
import matplotlib.transforms as tr
from PIL import Image
import json
import os
import re

"""
输出结果在：algo_interview-main/output文件中
实现效果：1.根据坐标点还原笔记  2.将坐标点用线段连接  3.体现每个笔记点的粗细变化  4.将输出结果呈现正确方向
未解决内容：1.书写时压力值p在画图中表现为每个点的粗细，最终效果应该为表现每两个点之间线段粗细的过渡。暂无很好的解决思路
"""

def Handwritten_restore(file_name):
    """
    filename: The name of json files
    流程思路：
    方法1：直接使用原坐标格式在坐标轴上画出散点图。
        缺点：由于同一笔画的不同坐标点的x坐标（或y坐标）不在一个列表内，使用matplotlib工具不方便将散点图连线。
    方法2：整理坐标数据、变换格式，使同一笔话的所有坐标点的x坐标（或y坐标）在放入同一数组，方便plot工具连线。
    原格式为：[[[x1,y1,p1], [x2,y2,p2]], [[x3,y3,p3], [x4,y4,p4]]]  共两个笔画，
    变换后的格式为：[[[x1,x2],[x3,x4], [y1,y2],[y3,y4], [p1,p2],[p3,p4]]]
    """
    with open(file_name, encoding='utf-8') as a:
        file = json.load(a)

    # 创建三个空的二维列表
    x_list = [[] for i in range(len(file))]
    y_list = [[] for i in range(len(file))]
    p_list = [[] for i in range(len(file))]

    # 双层for循环，遍历每一个笔画中每一个点的x、y、p坐标放入列表，并为每一笔画画图
    for num_spell in range(len(file)):
        for num_dot in range(len(file[num_spell])):
            x_list[num_spell].append(file[num_spell][num_dot][0])
            y_list[num_spell].append(file[num_spell][num_dot][1])
            p_list[num_spell].append(file[num_spell][num_dot][2]/4.0)  # /4.0：为后续粗细做归一化

        # 依次对每一个笔画散点图和连线图，x、y代表左边；p代表压力值，表现为散点粗细
        # 为何分别划散点图和连线图：
        # 因为plt.scatter()散点图接口中才有s这一参数来指定粗细，但scatter()无法连线。
        # plt.plot()连线图接口中无指定每个点或每条线段粗细的参数
        plt.scatter(x_list[num_spell], y_list[num_spell], s=p_list[num_spell], c='b', marker='.')
        plt.plot(x_list[num_spell], y_list[num_spell], marker='.', linestyle='solid', color='b')

    output_name = re.split("[\\\ |.]", file_name)[1] + '.png'  # 提取文件名
    output_dir = os.path.join('output', output_name)  # 构造文件地址


    plt.axis('off')  # 隐藏坐标轴
    plt.savefig(output_dir)  # 保存文件
    print(output_dir + '保存成功')

    # 发现文字方向错误，对结果旋转180度并左右镜像翻转
    pic_flip = Image.open(output_dir)
    pic_flip = pic_flip.rotate(180)
    pic_flip = pic_flip.transpose(Image.FLIP_LEFT_RIGHT)
    pic_flip.save(output_dir)
    print(output_dir + '翻转成功')

    plt.show()
    plt.close()

if __name__ == '__main__':
    # 遍历data文件夹中的每个Json文件，依次送入Handwritten_restore()函数，生成复原后的图片
    for root, dirs, files in os.walk('data'):
        for f in files:
            Handwritten_restore(file_name=os.path.join(root, f))  # data\亥.json
