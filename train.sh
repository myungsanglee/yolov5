python train.py \
--weights '' \
--cfg models/yolov5m.yaml \
--data data/lpr.yaml \
--hyp data/hyps/hyp.lpr.yaml \
--epochs 300 \
--batch-size 128 \
--img 224 \
--device '0' \
--workers 32