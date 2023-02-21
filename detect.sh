python detect.py \
--weights 'runs/train/exp/weights/best.pt' \
--source '0-0-2-rj-8-0-5-4.jpg' \
--data data/lpr.yaml \
--img 224 \
--conf-thres 0.4 \
--iou-thres 0.5 \
--device '0'