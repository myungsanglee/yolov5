python detect.py \
--weights 'runs/train/exp3/weights/best.pt' \
--source '/home/fssv2/myungsang/datasets/lpd/green_plate' \
--data data/lpd.yaml \
--img 224 \
--conf-thres 0.4 \
--iou-thres 0.5 \
--device '0' \
--nosave \
--view-img