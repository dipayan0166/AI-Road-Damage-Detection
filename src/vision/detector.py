"""
Road Damage Detector Module
Supports:
1. Dual-Model Ensemble Fusion (combining regional dashcam model with multi-region global model)
2. Global Multi-Region RDD2022 model
3. Custom Fine-Tuned Indian dashcam model
Includes IPCV preprocessing, Non-Maximum Suppression (NMS) fusion,
defect thumbnail cropping, and Pavement Condition Index (PCI) analytics.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from ultralytics import YOLO

from src.ipcv.preprocessor import RoadImagePreprocessor
from src.analytics.severity import calculate_defect_severity, compute_road_condition_index

CLASS_NAMES = {
    0: "Longitudinal Crack (D00)",
    1: "Transverse Crack (D10)",
    2: "Alligator Crack (D20)",
    3: "Pothole (D40)"
}

class RoadDamageDetector:
    def __init__(
        self,
        model_weights_path: str = "models/trained/best.pt",
        global_weights_path: str = "models/pretrained/rdd2022_global.pt",
        device: str = "0"
    ):
        self.device = device
        self.preprocessor = RoadImagePreprocessor()
        self.local_weights_path = Path(model_weights_path)
        self.global_weights_path = Path(global_weights_path)
        
        # Load local fine-tuned model
        self.local_model = None
        if self.local_weights_path.exists():
            print(f"[*] Initializing Local Fine-Tuned YOLO model: {self.local_weights_path}")
            try:
                self.local_model = YOLO(str(self.local_weights_path))
            except Exception as e:
                print(f"[!] Warning: Could not load local model: {e}")

        # Load global multi-country model
        self.global_model = None
        if self.global_weights_path.exists():
            print(f"[*] Initializing Global Multi-Region YOLO model: {self.global_weights_path}")
            try:
                self.global_model = YOLO(str(self.global_weights_path))
            except Exception as e:
                print(f"[!] Warning: Could not load global model: {e}")

        # Fallback if neither found
        if self.local_model is None and self.global_model is None:
            print("[*] Initializing baseline YOLO11n fallback model")
            self.local_model = YOLO("yolo11n.pt")

    def detect_image(
        self,
        image_input,
        conf_threshold: float = 0.15,
        iou_threshold: float = 0.45,
        apply_clahe: bool = False,
        imgsz: Optional[int] = 640,
        model_mode: str = "Ensemble Fusion (Recommended)",
        save_crops_dir: Optional[str] = "data/detected_crops",
        **kwargs
    ) -> Dict:
        """
        Run road damage detection on an image (path or numpy array).
        Supports:
          - 'Ensemble Fusion (Recommended)': Runs both engines and fuses bounding boxes via NMS.
          - 'Global Multi-Region Engine': Uses high-capacity multi-national RDD2022 model.
          - 'Custom Local Model (India)': Uses regional fine-tuned model.
        Returns comprehensive detection summary, cropped defects, and road condition index.
        """
        # Load image if string path
        if isinstance(image_input, (str, Path)):
            img_path = Path(image_input)
            image_bgr = cv2.imread(str(img_path))
            if image_bgr is None:
                raise ValueError(f"Could not read image from {image_input}")
            img_name = img_path.name
        else:
            image_bgr = image_input
            img_name = "input_image.jpg"

        h, w = image_bgr.shape[:2]
        if imgsz is None:
            imgsz = 640

        # Apply classical IPCV CLAHE enhancement only if explicitly requested
        if apply_clahe:
            inference_img = self.preprocessor.apply_clahe(image_bgr)
        else:
            inference_img = image_bgr

        # Determine which models to run based on user selection
        run_local = ("Local" in model_mode or "Ensemble" in model_mode) and (self.local_model is not None)
        run_global = ("Global" in model_mode or "Ensemble" in model_mode) and (self.global_model is not None)

        if not run_local and not run_global:
            run_local = self.local_model is not None
            run_global = self.global_model is not None

        raw_candidates = []

        # 1. Inference with Local Model
        if run_local and self.local_model is not None:
            try:
                res_local = self.local_model.predict(
                    source=inference_img,
                    conf=conf_threshold,
                    iou=iou_threshold,
                    imgsz=imgsz,
                    device=self.device,
                    verbose=False
                )[0]
                if res_local.boxes is not None and len(res_local.boxes) > 0:
                    for b in res_local.boxes:
                        x1, y1, x2, y2 = map(int, b.xyxy[0].tolist())
                        c = float(b.conf[0].item())
                        raw_cls = int(b.cls[0].item())
                        std_cls = min(max(0, raw_cls), 3)
                        raw_candidates.append(([x1, y1, x2, y2], c, std_cls, "Local Model"))
            except Exception as e:
                print(f"[!] Local model inference error: {e}")

        # 2. Inference with Global Model
        if run_global and self.global_model is not None:
            try:
                res_global = self.global_model.predict(
                    source=inference_img,
                    conf=conf_threshold,
                    iou=iou_threshold,
                    imgsz=imgsz,
                    device=self.device,
                    verbose=False
                )[0]
                if res_global.boxes is not None and len(res_global.boxes) > 0:
                    for b in res_global.boxes:
                        x1, y1, x2, y2 = map(int, b.xyxy[0].tolist())
                        c = float(b.conf[0].item())
                        raw_cls = int(b.cls[0].item())
                        # Map Global classes: 0: D00, 1: D10, 2: D20, 3: D40, 4: Other/Pothole
                        std_cls = 3 if raw_cls in [3, 4] else min(raw_cls, 3)
                        raw_candidates.append(([x1, y1, x2, y2], c, std_cls, "Global Model"))
            except Exception as e:
                print(f"[!] Global model inference error: {e}")

        # 3. Non-Maximum Suppression (NMS) Fusion
        fused_boxes = []
        if raw_candidates:
            # Sort descending by confidence so highest-scoring predictions are prioritized
            raw_candidates.sort(key=lambda x: x[1], reverse=True)

            if len(raw_candidates) == 1 or not ("Ensemble" in model_mode):
                fused_boxes = raw_candidates
            else:
                boxes_xywh = [
                    [box[0], box[1], max(1, box[2] - box[0]), max(1, box[3] - box[1])]
                    for (box, c, cls_id, src) in raw_candidates
                ]
                scores = [c for (box, c, cls_id, src) in raw_candidates]
                indices = cv2.dnn.NMSBoxes(
                    bboxes=boxes_xywh,
                    scores=scores,
                    score_threshold=conf_threshold,
                    nms_threshold=iou_threshold
                )
                if len(indices) > 0:
                    for idx in np.array(indices).flatten():
                        fused_boxes.append(raw_candidates[idx])

        # 4. Generate Defect Crops & Annotated Visualizations
        crops_dir = Path(save_crops_dir) if save_crops_dir else None
        if crops_dir:
            crops_dir.mkdir(parents=True, exist_ok=True)

        annotated_bgr = image_bgr.copy()
        defects = []

        for i, (box_coords, conf, cls_id, src_engine) in enumerate(fused_boxes):
            x1, y1, x2, y2 = box_coords
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            box_w = (x2 - x1) / w
            box_h = (y2 - y1) / h
            norm_box = (
                ((x1 + x2) / 2.0) / w,
                ((y1 + y2) / 2.0) / h,
                box_w,
                box_h
            )

            sev_info = calculate_defect_severity(cls_id, norm_box, conf)

            # Crop thumbnail
            crop_path = None
            if crops_dir and (x2 > x1) and (y2 > y1):
                crop_img = image_bgr[y1:y2, x1:x2]
                crop_filename = f"{Path(img_name).stem}_defect_{i}_{sev_info['severity']}.jpg"
                crop_path = crops_dir / crop_filename
                cv2.imwrite(str(crop_path), crop_img)

            sev_info["bbox"] = [x1, y1, x2, y2]
            sev_info["crop_path"] = str(crop_path) if crop_path else ""
            sev_info["engine"] = src_engine
            defects.append(sev_info)

            # Bounding box color coding: Red=Critical, Orange=Moderate, Green=Minor
            color_bgr = (0, 0, 255) if sev_info["severity"] == "Critical" else (
                (0, 165, 255) if sev_info["severity"] == "Moderate" else (0, 200, 0)
            )

            cv2.rectangle(annotated_bgr, (x1, y1), (x2, y2), color_bgr, 2)
            label_text = f"{sev_info['class_name'].split()[0]} {conf*100:.0f}% ({sev_info['severity']})"

            # Label banner
            (tw, th), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(annotated_bgr, (x1, max(0, y1 - 20)), (x1 + tw, y1), color_bgr, -1)
            cv2.putText(annotated_bgr, label_text, (x1, max(14, y1 - 4)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # 5. Compute Composite Road Condition Index (PCI)
        condition = compute_road_condition_index(defects)

        return {
            "image_name": img_name,
            "original_image": image_bgr,
            "annotated_image": annotated_bgr,
            "defects": defects,
            "condition": condition,
            "total_defects": len(defects),
            "model_mode": model_mode
        }
