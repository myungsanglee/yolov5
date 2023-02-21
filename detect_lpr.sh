python detect_lpr.py \
--weights 'runs/train/exp/weights/best.pt' \
--source '/home/fssv2/myungsang/datasets/lpr/test.txt' \
--data data/lpr.yaml \
--img 224 \
--conf-thres 0.4 \
--iou-thres 0.5 \
--device '0'