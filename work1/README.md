# 作业 1：点运算

## 1. 运行方式

在终端输入以下命令：

```shell
$ python .\point_operation.py image_path operation_type
```

其中 `file_name` 为必选参数，表示图片所在路径。`operation_type` 为必选参数，表示点运算类型，提供了以下可选选项：

- `linear` ：线性点运算
- `segment` ：分段线性点运算
- `non_linear` ：非线性点运算



## 2. 示例

原始灰度图为：

<div>
    <center>
    	<img src="imgs/original.png" >
    </center>
</div>



经过不同的点运算后，得到以下图片：

线性点运算：

<div>
    <center>
    	<img src="imgs/linear_original.png" >
    </center>
</div>


分段线性点运算：

<div>
    <center>
    	<img src="imgs/segment_original.png" >
    </center>
</div>


非线性点运算：

<div>
    <center>
    	<img src="imgs/non_linear_original.png" >
    </center>
</div>



