**pcba缺陷检测模型**

# 说明介绍

基于yolov8模型训练pcba缺陷检测模型


# 使用：

构建镜像：

```
docker build . -t ultralytics-pcba-model:local
```

启动

```
docker run -ti --rm -p 8080:8080 ultralytics-pcba-model:local
```

测试

1. 下载pcba测试缺陷数据集
   
[PCB Dataset Defect.v1-initital-ver.yolov8.zip](https://pcba-test.obs.cn-north-4.myhuaweicloud.com/PCB%20Dataset%20Defect.v1-initital-ver.yolov8.zip)

2. 调用模型推理接口

   `curl --location 'http://localhost:8080/'
--form 'images=@"xxx/12_short_08_jpg.rf.cb1c21591b1952f754c510b329192c98.jpg"'
--form 'images=@"xxx/12_spur_07_jpg.rf.e16007d5253256d437db4a50206f6665.jpg"'`
