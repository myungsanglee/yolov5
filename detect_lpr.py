# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run YOLOv5 detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.

Usage - sources:
    $ python detect.py --weights yolov5s.pt --source 0                               # webcam
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     screen                          # screenshot
                                                     path/                           # directory
                                                     list.txt                        # list of images
                                                     list.streams                    # list of streams
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s_openvino_model     # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlmodel            # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle
"""

import argparse
import os
import platform
import sys
from pathlib import Path

import torch

from PIL import ImageFont, ImageDraw, Image
from utils.augmentations import letterbox
import numpy as np

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode


@smart_inference_mode()
def run(
        weights=ROOT / 'yolov5s.pt',  # model path or triton URL
        source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        vid_stride=1,  # video frame-rate stride
):
    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)
    screenshot = source.lower().startswith('screen')
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    bs = 1  # batch_size
    if webcam:
        view_img = check_imshow(warn=True)
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        bs = len(dataset)
    elif screenshot:
        dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    vid_path, vid_writer = [None] * bs, [None] * bs


    ##########################################################################
    color = (0, 255, 0)
    font = ImageFont.truetype('malgun.ttf', 30)
    with open('/home/fssv2/myungsang/datasets/lpr/lpr_kr.names') as f:
        name_list = f.read().splitlines()
    true_num = 0
    total_num = 0
    ##########################################################################
    
    
    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:
        # print(path)
        # print(im.shape)
        # print(im0s.shape)
        
        txt_path = path.rsplit('.', 1)[0] + '.txt'
        with open(txt_path, 'r') as f:
            labels = f.read().splitlines()
        # labels = [[float(y) for y in x.split(' ')[1:]] for x in labels if x.split(' ')[0] == '8']
        labels = [[float(y) for y in x.split(' ')[1:]] for x in labels if x.split(' ')[0] == '0']
        
        img_h, img_w, _ = im0s.shape
        
        img = Image.fromarray(im0s)
        draw = ImageDraw.Draw(img)
        
        for label in labels:
            total_num += 1
            
            cx = label[0] * img_w
            cy = label[1] * img_h
            w = label[2] * img_w
            h = label[3] * img_h
            
            xmin = int(cx - (w / 2))
            ymin = int(cy - (h / 2))
            xmax = int(cx + (w / 2))
            ymax = int(cy + (h / 2))
            
            crop_img_height = ymax - ymin
            
            draw.rectangle((xmin, ymin, xmax, ymax), outline=color, width=1)
        
            crop_img = im0s[ymin:ymax, xmin:xmax].copy()
            
            print('')
            print(f'stride: {stride}, pt: {pt}')
            print('')
            im = letterbox(crop_img, imgsz, stride=stride, auto=pt)[0]
            
            im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
            im = np.ascontiguousarray(im)  # contiguous
        
            # import sys
            # sys.exit(1)
        
            with dt[0]:
                im = torch.from_numpy(im).to(model.device)
                im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim

            # Inference
            with dt[1]:
                visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
                
                pred = model(im, augment=augment, visualize=visualize)
                print(pred[0].size())
            
            # NMS
            with dt[2]:
                pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
                # print(len(pred))
                # print(pred[0].size())
                # print(pred)
            
            # Second-stage classifier (optional)
            # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

            # Process predictions
            for i, det in enumerate(pred):  # per image
                seen += 1
                if webcam:  # batch_size >= 1
                    # p, im0, frame = path[i], im0s[i].copy(), dataset.count
                    p, im0, frame = path[i], crop_img[i].copy(), dataset.count
                    s += f'{i}: '
                else:
                    # p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
                    p, im0, frame = path, crop_img.copy(), getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # im.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
                s += '%gx%g ' % im.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                imc = im0.copy() if save_crop else im0  # for save_crop
                annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, 5].unique():
                        n = (det[:, 5] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                        
                    # Write results
                    detections = []
                    for *xyxy, conf, cls in reversed(det):
                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                            with open(f'{txt_path}.txt', 'a') as f:
                                f.write(('%g ' * len(line)).rstrip() % line + '\n')

                        if save_img or save_crop or view_img:  # Add bbox to image
                        # if True:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                            annotator.box_label(xyxy, label, color=colors(c, True))
                        if save_crop:
                            save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)
                        
                        ############################################################################################
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        box = xyxy
                        detections.append([c, float(conf), int(box[0]), int(box[1]), int(box[2]), int(box[3])])
                        ############################################################################################
                    
                    ############################################################################################
                    detections = np.array(detections)
                    plate_num, detections = get_plate_number(detections, crop_img_height, name_list)
                    true_label = os.path.basename(path).rsplit('.', 1)[0]
                    if len(true_label.split('-')) > 1:
                        true_label = true_label.split('-')[0]
                    if plate_num == true_label:
                        true_num += 1
                        
                        # save_label(crop_img.copy(), detections, true_num)
                    
                    print(f'True: {true_label}, Pred: {plate_num}')
                    
                    txt_w, txt_h = draw.textsize(plate_num, font=font)
                    draw.text(((xmin, max(ymin - txt_h, 0))), f'{plate_num}', font=font, fill=color)
                    
                    # draw plate number
                    for detection in detections:
                        cls_idx, conf, x1, y1, x2, y2 = detection
                        
                        pxmin = xmin + int(x1)
                        pxmax = xmin + int(x2)
                        pymin = ymin + int(y1)
                        pymax = ymin + int(y2)
                        
                        draw.rectangle((pxmin, pymin, pxmax, pymax), outline=color, width=1)
                    
                    # conf_str = ''
                    # for conf in detections[..., 1]:
                    #     conf_str += f'{conf:.4f} '
                    # print(conf_str)
                    ############################################################################################
                    

                # Stream results
                im0 = annotator.result()
                if view_img:
                    if platform.system() == 'Linux' and p not in windows:
                        windows.append(p)
                        cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                        cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                    cv2.imshow(str(p), im0)
                    cv2.waitKey(1)  # 1 millisecond
                    
                if save_img:
                    if dataset.mode == 'image':
                        cv2.imwrite(save_path, im0)
                    else:  # 'video' or 'stream'
                        if vid_path[i] != save_path:  # new video
                            vid_path[i] = save_path
                            if isinstance(vid_writer[i], cv2.VideoWriter):
                                vid_writer[i].release()  # release previous video writer
                            if vid_cap:  # video
                                fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            else:  # stream
                                fps, w, h = 30, im0.shape[1], im0.shape[0]
                            save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                            vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                        vid_writer[i].write(im0)

            # Print time (inference-only)
            LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

        ############################################################################################
        # Show Image
        # img = np.array(img)
        # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('img', 1080, 720)
        # cv2.imshow('img', img)
        # key = cv2.waitKey(0)
        # if key == 27:
        #     break
        
        # Save Image
        # new_dir = os.path.join('/home/fssv2/myungsang/datasets/lpr/pytorch_test_3', path.split(os.sep)[-2])
        # new_dir = os.path.join('/home/fssv2/myungsang/datasets/lpr/pytorch_test_3')
        # if not os.path.isdir(new_dir):
        #     os.makedirs(new_dir, exist_ok=True)
        # new_path = os.path.join(new_dir, os.path.basename(path))
        # cv2.imwrite(new_path, img)
        ############################################################################################

    print(f'Accuracy: {true_num} / {total_num} = {(true_num / total_num)*100:.2f}%')

    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)


def save_label(img, detections, true_num):
    img_h, img_w, _ = img.shape
    
    output_dir = '/home/fssv2/myungsang/datasets/lpr/val_v4'
    output_jpg_path = os.path.join(output_dir, f'val_v4_data_{true_num:04d}.jpg')
    output_txt_path = output_jpg_path.rsplit('.', 1)[0] + '.txt'
    
    cv2.imwrite(output_jpg_path, img)
    
    f = open(output_txt_path, 'w')
    
    for detection in detections:
        cls_idx, conf, x1, y1, x2, y2 = detection

        cx = (x1 + x2) / 2 / img_w
        cy = (y1 + y2) / 2 / img_h
        w = (x2 - x1) / img_w
        h = (y2 - y1) / img_h
        
        label = f'{int(cls_idx)} {cx} {cy} {w} {h}\n'
        f.write(label)
    
    
        

def get_plate_number(detections, network_height, cls_name_list):
    detect_num = len(detections)
    if detect_num < 4:
        return 'None', detections
    elif detect_num > 8:
        detections = np.delete(detections, np.argsort(detections[..., 1])[:detect_num-8], axis=0)
    detections = detections[np.argsort(detections[..., 3])]
    
    thresh = int(network_height / 5)
    y1 = detections[1][3] - detections[0][3]
    y2 = detections[3][3] - detections[2][3]
    
    # 외교 번호판
    if y1 > thresh:
        detections[1:] = detections[1:][np.argsort(detections[1:, 2])]
    
    # 운수/건설 번호판
    elif y2 > thresh:
        detections[:3] = detections[:3][np.argsort(detections[:3, 2])]
        detections[3:] = detections[3:][np.argsort(detections[3:, 2])]
    
    # 일반 가로형 번호판
    else:
        detections = detections[np.argsort(detections[..., 2])]

    # 번호판 포맷에 맞는지 체크
    detections = check_plate(detections)

    plate_num = ''
    for cls_idx in detections[..., 0]:
        plate_num += cls_name_list[int(cls_idx)]
    
    return plate_num, detections


def check_plate(detections):
    # 가, 나, 다, ... 번호는 하나만 존재하고 그 뒤의 번호는 4자리만 올 수 있다.
    str_idx_list = np.where((10<=detections[..., 0]) & (detections[..., 0]<=48))[0]
    if len(str_idx_list):
        if len(str_idx_list) > 1:
            arg_idx = np.argsort(-detections[str_idx_list][..., 1])
            delete_idx = str_idx_list[arg_idx[1:]]
            detections = np.delete(detections, delete_idx, axis=0)
            str_idx = str_idx_list[arg_idx[0]]
        else:
            str_idx = str_idx_list[0]
            
        if len(detections[str_idx+1:]) > 4:
            delete_idx = np.argsort(-detections[str_idx+1:, 1])[4:] + (str_idx + 1)
            detections = np.delete(detections, delete_idx, axis=0)

    # 서울, 경기, ... 지역 번호는 하나만 존재
    area_idx_list = np.where((49<=detections[..., 0]) & (detections[..., 0]<=64))[0]
    if len(area_idx_list) > 1:
        arg_idx = np.argsort(-detections[area_idx_list][..., 1])
        delete_idx = area_idx_list[arg_idx[1:]]
        detections = np.delete(detections, delete_idx, axis=0)
    
    # 외교, 영사, ... 번호는 하나만 존재
    diplomacy_idx_list = np.where(64 < detections[..., 0])[0]
    if len(diplomacy_idx_list) > 1:
        arg_idx = np.argsort(-detections[diplomacy_idx_list][..., 1])
        delete_idx = diplomacy_idx_list[arg_idx[1:]]
        detections = np.delete(detections, delete_idx, axis=0)
    
    return detections


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path or triton URL')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt


def main(opt):
    check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
