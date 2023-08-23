python train.py \
--weights '' \
--cfg models/yolov5m.yaml \
--data data/test.yaml \
--hyp data/hyps/hyp.test.yaml \
--epochs 1 \
--batch-size 1 \
--img 224 \
--device '0' \
--workers 0