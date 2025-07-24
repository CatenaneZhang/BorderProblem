# 边界问题
多个半径相同的圆在平面上随机分布。该代码可计算它们的边界。这一边界考虑到了圆相交的情况，给出了实际产生的边界。
## 输入和参数
允许给出圆的位置，用存储二元组的列表实现；圆的半径；输出边界上点的采样密度。以及显示理论边界或是显示实际输出的点。
## 输出
输出为一系列轨迹列表trajs，其中的每个traj都是一个列表，其中存储了从轨迹上采样的点坐标。这一采样密度可以从参数中修改。
## 特点
### 可视化
采用matplotlib完成可视化，显示生成的圆、交点及其边界。对于不同的边界，代码采用不同的颜色标识以示区别。
### 空隙处理
对于多个圆形成的空隙，例如，当四个圆的圆心处于正方形的四个顶点上，邻边的圆相交而斜边的圆相离，此时四个圆中会形成空隙。代码可以正确处理这些空隙。返回空隙的边界。


# BorderProblem
Multiple circles with the same radius are randomly distributed on a plane. This code calculates their boundaries. This boundary takes into account the intersection of circles and gives the actual boundary produced.
