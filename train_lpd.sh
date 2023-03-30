python train.py \
--weights '' \
--cfg models/yolov5m.yaml \
--data data/lpd.yaml \
--hyp data/hyps/hyp.lpd.yaml \
--epochs 100 \
--batch-size 32 \
--img 224 \
--device '0' \
--workers 32