
# depth_from_video_in_the_wild_eval

[Original](https://github.com/google-research/google-research/tree/master/depth_from_video_in_the_wild)

# Example input

## Train example (KITTI)

- [Data Preparation](https://github.com/go125/PrepareDataForDFV)
- [ImageNet Checkpoint Preparation](https://github.com/dalgu90/resnet-18-tensorflow)

```script
nohup python -m depth_from_video_in_the_wild.train \
--data_dir /home/ubuntu/data/kitti_result_all_20200715 \
--checkpoint_dir=/home/ubuntu/data/kitti_experiment_checkpoint_20201201 \
--imagenet_ckpt=/home/ubuntu/data/ResNet18/model.ckpt \
--train_steps=10000
-- fps 1 &
```

## Finetuning with the video taken in Saitama

Under Construction

## 1. Use StereoAVIToPNG.py

```
nohup python StereoAVIToPNG.py \
--path_avi /home/ubuntu/data/StereoVideo/V2-mv-20200716103312-ulrg.avi \
--path_output_png /home/ubuntu/data/Sayama/all_video/video1top_png/ \
--option top &
```

```
nohup python StereoAVIToPNG.py \
--path_avi /home/ubuntu/data/StereoVideo/V2-mv-20200716103312-ulrg.avi \
--path_output_png /home/ubuntu/data/Sayama/all_video/video1middle_png/ \
--option middle &
```

```
nohuo python StereoAVIToPNG.py \
--path_avi /home/ubuntu/data/StereoVideo/V2-mv-20200716105152-ulrg.avi \
--path_output_png /home/ubuntu/data/Sayama/all_video/video2top_png/ \
--option top &
```

```
nohup python StereoAVIToPNG.py \
--path_avi /home/ubuntu/data/StereoVideo/V2-mv-20200716105152-ulrg.avi \
--path_output_png /home/ubuntu/data/Sayama/all_video/video2middle_png/ \
--option middle &
```

## 2 Use CropPNG.py

```script
nohup python CropPNG.py --base_path /home/ubuntu/data/Sayama/all_video/ \
--WIDTH 416 \
--HEIGHT 128 \
--OUTPUT_DIR /home/ubuntu/data/Sayama/out \
--TEMP_DIR /home/ubuntu/data/Sayama/tmpdir &
```

## 3 Use MakeMask.py
"all video" dir should include only "video2top_png" dir.

```script
nohup python MakeMask.py --base_path /home/ubuntu/data/Sayama/all_video/ \
--ROOT_DIR ../Mask_RCNN \
--WIDTH 416 \
--HEIGHT 128 \
--OUTPUT_DIR /home/ubuntu/data/Sayama/out \
--TEMP_DIR /home/ubuntu/data/Sayama/tmpdir &
```

## 4. Training

```script
nohup python -m depth_from_video_in_the_wild.train \
--data_dir /home/ubuntu/data/Sayama/training_data \
--checkpoint_dir=/home/ubuntu/data/kitti_experiment_checkpoint_20200716 \
--imagenet_ckpt=/home/ubuntu/data/ResNet18/model.ckpt \
--train_steps=1000000 &
```

## Evaluation

### Before fine tuning

### Getting Predicted Depth

```shell
python inference_dfv.py \
    --logtostderr \
    --file_extension png \
    --depth \
    --egomotion false \
    --input_dir /home/ubuntu/data/Sayama/tmpdir/2020_08_04/video1top_png/image_02/data/ \
    --output_dir /home/ubuntu/Sayama/result_video1top_273486/ \
    --model_ckpt /home/ubuntu/data/kitti_experiment_checkpoint_20200716/model-273486
```

### Getting Abs Rel Error

```shell
python kitti_eval/eval_depth.py --kitti_dir=/home/ubuntu/data/raw_data_KITTI/ --pred_file=/home/ubuntu/data/result_20200716_273486/result.npy
```

### After fine tuning

### Getting Predicted Depth

```shell
python inference_dfv.py \
    --logtostderr \
    --file_extension png \
    --depth \
    --egomotion false \
    --input_dir /home/ubuntu/Sayama/tmpdir/2020_08_04/video1top_png/image_02/data/ \
    --output_dir /home/ubuntu/Sayama/result_video1top_279296/ \
    --model_ckpt /home/ubuntu/data/kitti_experiment_checkpoint_20200716/model-279296
```

### Getting Abs Rel Error

```shell
python kitti_eval/eval_depth.py --kitti_dir=/home/ubuntu/data/raw_data_KITTI/ --pred_file=/home/ubuntu/data/result_20200716_279296/result.npy
```
