python detect_lpr.py \
--weights 'runs/train/exp2/weights/best.pt' \
--source '/home/fssv2/myungsang/datasets/lpr/test_v1.txt' \
--data data/lpr.yaml \
--img 224 \
--conf-thres 0.4 \
--iou-thres 0.5 \
--device '0'