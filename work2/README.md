# 作业 2：几何运算

## 1. 运行方式

在终端输入以下命令：

```shell
$ python .\geometric_operation.py image_path geometric_operation1 [geometric_operation2 ...]
```

其中 `image_path` 为必选参数，表示图片所在路径。`geometric_operation1` 为必选参数，表示几何运算类型，提供了以下可选选项：

- `shift` ：平移
- `horizonal` ：水平镜像
- `vertical` ：竖直镜像
- `rotate`：选择

`[geometric_operation2 ...]` 为可选参数，可选值与参数 `geometric_operation1` 相同。



## 2. 示例

原始图片为：

<div>
    <center>
    	<img src="imgs/Lenna.jpg" >
    </center>
</div>




经过不同的几何运算后，得到以下图片：

平移：

<div>
    <center>
    	<img src="imgs/shift_Lenna.jpg" >
    </center>
</div>



水平镜像：

<div>
    <center>
    	<img src="imgs/horizonal_Lenna.jpg" >
    </center>
</div>



竖直镜像：

<div>
    <center>
    	<img src="imgs/vertical_Lenna.jpg" >
    </center>
</div>



旋转：

<div>
    <center>
    	<img src="imgs/rotate_Lenna.jpg" >
    </center>
</div>

复合：

<div>
    <center>
    	<img src="imgs/composed_Lenna.jpg" >
    </center>
</div>