import matplotlib.pyplot as plt
import matplotlib
def getTreeDepth(myTree):
    leaf_depth = 0
    feat = list(myTree.keys())[0]
    feat_value = myTree[feat]
    for key in feat_value.keys():
        if type(feat_value[key]).__name__ == 'dict':
            deep = 1 + getTreeDepth(feat_value[key])
        else:
            deep = 1
        if deep > leaf_depth : leaf_depth = deep
    return leaf_depth

def getTreeLeaf(myTree):
    leaf_num = 0 # 叶子节点数
    feat = list(myTree.keys())[0]
    # print(feat)
    feat_value = myTree[feat]
    # print(feat_value)
    for key in feat_value.keys():
        if type(feat_value[key]).__name__ == 'dict':
            leaf_num += getTreeLeaf(feat_value[key])
        else:
            leaf_num += 1
    return leaf_num


# 节点样式
decisionNode = dict(boxstyle = "sawtooth", fc="0.8")
leaf_Node = dict(boxstyle = "round4", fc="0.8")
# 箭头样式
arrow = dict(arrowstyle="<-")

def plot_Node(node_Text, centerPt, parentPt, node_Type):
    createPlot.ax1.annotate(node_Text, xy=parentPt, \
                            xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction', \
                            va="center", ha="center", bbox=node_Type, arrowprops=arrow)


def plot_Mid_Text(cntrPt, parentPt, textString):
    xmid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0] # 计算文字x轴
    ymid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1] # 计算文字y轴
    createPlot.ax1.text(xmid, ymid, textString)

def createPlot(inTree):

    matplotlib.rcParams['font.sans-serif'] = ['KaiTi']
    # 新建一个面板，背景色为白色
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    axprops = dict(xticks=[],yticks=[])
    # 创建一个1行1列的figure，并把网格里面的第一个figure的Axes实例返回ax1作为函数createPlot()的
    # 的属性，这个属性ax1相当于一个全局变量，可以给plot_Node()函数使用
    createPlot.ax1 = plt.subplot(111,frameon=False, **axprops)
    # 获取树的叶子节点
    plotTree.totalW = float(getTreeLeaf(inTree))
    # 获取树的深度
    plotTree.totalD = float(getTreeDepth(inTree))
    # 节点的x轴的偏移量为 -1/plotTree.totalW/2, 1为x轴的长度，除以2保证每一个节点的X轴之间的距离
    # 为1/plotTree.totalW*2
    plotTree.xoff = -0.5 / plotTree.totalW
    plotTree.yoff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()

def plotTree(myTree, parentPt, node_text):
    # 计算树的叶子节点数
    leaf_num = getTreeLeaf(myTree)
    # print("树的叶子节点数为："+str(leaf_num))
    # 计算树的深度
    leaf_depth = getTreeDepth(myTree)
    # print("数的深度为："+str(leaf_depth))
    # 获取第一个键名
    first_str = list(myTree.keys())[0]
    # 计算子节点的坐标
    cntrPt = (plotTree.xoff + (1.0 + float(leaf_num)) / 2.0/plotTree.totalW, plotTree.yoff)
    # 绘制线上的文字
    plot_Mid_Text(cntrPt, parentPt, node_text)
    # 绘制节点
    plot_Node(first_str, cntrPt, parentPt, decisionNode)
    # 获取第一个键值
    second_dict = myTree[first_str]
    # 计算节点y方向上的偏移量，根据树的深度
    plotTree.yoff = plotTree.yoff - 1.0 / plotTree.totalD
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ =='dict':
            # 递归绘制树
            plotTree(second_dict[key], cntrPt, str(key))
        else:
            # 更新x的偏移量，每个叶子节点x轴方向上的距离为 1/plotTree.totalW
            plotTree.xoff = plotTree.xoff + 1.0 / plotTree.totalW
            # 绘制非叶子节点
            plot_Node(second_dict[key], (plotTree.xoff, plotTree.yoff),cntrPt,leaf_Node)
            # 绘制箭头上的标志
            plot_Mid_Text((plotTree.xoff, plotTree.yoff), cntrPt, str(key))
    plotTree.yoff = plotTree.yoff + 1.0 / plotTree.totalD

# myTree = {'hair': {'long hair': {'stature': {'short': 'female', 'high': {'weight': {'thin': 'female', 'fat': 'male'}}}}, 'short hair': {'weight': {'thin': {'gender': {'female': 'female', 'male': 'male'}}, 'fat': 'male'}}}}
# createPlot(myTree)