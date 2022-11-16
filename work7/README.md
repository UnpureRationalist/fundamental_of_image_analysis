# 作业 7：大津法和迭代法阈值分割

## 1. 运行方式

在终端输入以下命令：

```shell
$ python .\segmentation.py image_path oper_type
```

其中 `image_path` 为必选参数，表示图片所在路径。`oper_type` 为必选参数，表示分割算法类型。`oper_type` 可选值如下：

- `ostf`：大津法
- `iter`：迭代法



## 2. 示例

从左到右依次为原图、大津法分割结果、迭代法分割结果。

<div>
    <center>
    	<img src="imgs/Lenna.png" width="300">
    	<img src="imgs/ostf_Lenna.png" width="300">
        <img src="imgs/iter_Lenna.png" width="300">
    </center>
</div>



<div>
    <center>
    	<img src="imgs/parrot.png" width="300">
    	<img src="imgs/ostf_parrot.png" width="300">
        <img src="imgs/iter_parrot.png" width="300">
    </center>
</div>



## 3. 性能比较

下述实验中，迭代法两次灰度差的阈值取值为 1。

| 算法名称 |   图片名   | 分辨率  | 1000 次分割耗时(s) |
| :------: | :--------: | :-----: | :----------------: |
|  大津法  | Lenna.png  | 316×316 |       69.25        |
|  迭代法  | Lenna.png  | 316×316 |       30.74        |
|  大津法  | parrot.png | 150×200 |       12.07        |
|  迭代法  | Lenna.png  | 150×200 |        9.48        |

根据上述实验结果，可得：迭代法性能更好。
