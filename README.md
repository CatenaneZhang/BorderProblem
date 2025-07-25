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
### 灵活复杂度
代码允许自定义输出轨迹的采样密度。复杂的场景适用低采样密度以降低计算开销。

# BorderProblem
Multiple circles with the same radius are randomly distributed on a plane. This code calculates their boundaries. This boundary takes into account the intersection of circles and gives the actual boundary produced.
## Input and Parameters
Allows specifying the position of a circle, implemented using a list of tuples; the radius of the circle; the sampling density of points on the output boundary. Additionally, it can display either the theoretical boundary or the actual output points.
## Output
The output is a list of trajectory lists `trajs`, where each `traj` is a list containing the coordinates of points sampled from the trajectory. This sampling density can be modified via parameters.
## Features
### Visualization
Visualization is implemented using matplotlib, displaying the generated circles, intersection points, and their boundaries. Different colors are used to distinguish between different boundaries.
### Gap Handling
For gaps formed by multiple circles, such as when the centers of four circles are at the four corners of a square, with adjacent circles intersecting and diagonal circles separated, gaps may form between the four circles. The code can correctly handle these gaps and return their boundaries.
### Flexible Complexity
The code allows customization of the sampling density for output trajectories. A lower sampling density can be used for complex scenarios to reduce computational overhead.
