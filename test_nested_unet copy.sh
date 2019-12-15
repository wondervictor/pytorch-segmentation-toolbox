#!/bin/bash
uname -a
#date
#env
date

CS_PATH=$1
LR=1e-2
WD=5e-4
BS=8
STEPS=40000
GPU_IDS=0,1,2,3

#variable ${LOCAL_OUTPUT} dir can save data of you job, after exec it will be upload to hadoop_out path 
python train.py --model nested_unet --data-dir ${CS_PATH} --random-mirror --random-scale --gpu ${GPU_IDS} --learning-rate ${LR}  --weight-decay ${WD} --batch-size ${BS} --num-steps ${STEPS}
python evaluate.py --model nested_unet --data-dir ${CS_PATH} --gpu 0