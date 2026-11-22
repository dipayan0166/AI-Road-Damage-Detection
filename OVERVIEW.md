**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

**IPCV PROJECT PLANNING** 

# **AI-Based Smart Road Damage Detection System** 

Complete project discussion, methodology, model selection and implementation roadmap 

**IMAGE PROCESSING AND COMPUTER VISION** 

Compiled from the project-planning conversation 

6 November 2026 

AI-Based Smart Road Damage Detection System  •  1 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

## **Contents** 

1. Original project brief 

2. Project concept and problem definition 

3. Overall system architecture 

4. Pretrained model selection 

5. Dataset selection and preparation 

6. Fine-tuning methodology 

7. Adding locally collected Indian road images 

8. Object detection versus segmentation 

9. Application architecture and technology stack 

10. Model evaluation and experiments 

11. Complete implementation roadmap 

12. Engineering considerations and limitations 

13. Recommended initial project configuration 

14. Decisions to finalize before implementation 

15. Resource links 

#### **Document scope** 

This document preserves the written project discussion, technical tables, example code, and resource links. Image panels shown in the original chat were generated as illustrative search-image groups and are not embedded in this Word copy; their subjects are described in the relevant sections. 

AI-Based Smart Road Damage Detection System  •  2 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

## **1. Original project brief** 

User: 

_“I want to make my college project on IPCV (Image processing and Computer vision). The topic of my project is AIbased Smart Road damage detection System. So, basically I am planning to use a pretrained ai model, and integrate in my project by fine tuning the model so that it fits accordingly to our project. So , lets discuss on this. How we gona do this, lets plan the begining, the methodology, the implementation plan, models that we can select to use in our project. The complete walthrough and overview of our project. and also suggest me if this is a good approcah or are there any better methods, tech stacks, implementation  plans that we can follow.”_ 

## **2. Project concept and problem definition** 

The recommended direction is to build more than a standalone road-damage detector. The proposed system combines image processing, deep-learning-based detection, and a reporting application. 

- Image Processing: prepare road images and extract useful visual information. 

- Computer Vision and Deep Learning: identify and localize road damage using a pretrained, fine-tuned model. 

- Application Development: present detected damage, generate inspection reports, and optionally record GPS coordinates. 

### **Proposed project title** 

AI-Based Smart Road Damage Detection and Geo-Tagged Reporting System 

### **Problem statement** 

Road damage such as potholes, longitudinal cracks, transverse cracks, and alligator cracking can lead to accidents, vehicle damage, and deterioration of road infrastructure. Traditional road inspection relies heavily on manual observation, which is time-consuming, labour-intensive, and difficult to scale. 

The proposed system will use computer vision and deep learning to automatically identify and localize road damage from images and videos. It will provide a visual representation of detected damage and optionally record its geographical location for future inspection and maintenance. 

### **Initial damage categories** 

|**Class**|**Damage type**|**Description**|
|---|---|---|
|D00|Longitudinal crack|Cracks running parallel to the direction of the<br>road.|
|D10|Transverse crack|Cracks running across the road,<br>perpendicular to the direction of travel.|
|D20|Alligator crack|Interconnected cracks forming a pattern<br>resembling reptile skin.|
|D40|Pothole|Depressions or holes caused by pavement<br>deterioration.|



These four categories are established categories used by the Road Damage Dataset 2022 (RDD2022). This provides a defined classification system and avoids inventing labels from scratch. 

## **3. Overall system architecture** 

The complete system is intended to process road images or video, detect damage, attach inspection metadata, store the results, and present them through a dashboard. 

AI-Based Smart Road Damage Detection System  •  3 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

Road Images / Video / Camera | v Image Acquisition | v Image Preprocessing (OpenCV) | v Fine-Tuned Road Damage Model | v Detection and Classification | v Confidence Filtering | v Bounding Boxes and Labels | v Damage Analysis | v GPS / Timestamp Information | v Database | v Smart Inspection Dashboard /       |        \ v        v         v Reports   Damage Map   Detection Results 

|**Component**|**Responsibility**|
|---|---|
|Image acquisition|Accept road images, videos or camera input.|
|Preprocessing|Resize, normalize and prepare images.|
|AI detection|Detect and classify road damage.|
|Post-processing|Filter low-confidence predictions.|
|Damage analysis|Count and summarize detected damage.|
|GPS integration|Associate damage with geographical coordinates.|
|Database|Store inspection records.|
|Dashboard|Display detections and inspection results.|
|Reporting|Generate downloadable inspection reports.|



## **4. Pretrained model selection** 

The model-selection problem can be approached through image classification, object detection, semantic segmentation, instance segmentation, and transformer-based object detection. The recommended starting point is object detection using a YOLO model. 

AI-Based Smart Road Damage Detection System  •  4 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

### **Candidate models** 

|**Model**|**Strengths and role**|**Suggested use**|
|---|---|---|
|YOLO26n|Small, computationally efficient object<br>detector; supports custom training and<br>export.|Primary starting model: yolo26n.pt.|
|YOLO11n|Established YOLO architecture with<br>pretrained weights and documentation.|Comparison model: yolo11n.pt.|
|RT-DETR-R18|Transformer-based real-time object detector.|Optional research comparison.|
|YOLO26n-seg / SegFormer-B0|Pixel-level segmentation for describing<br>damage shape and area.|Advanced extension after detection works.|



### **Why YOLO26n was recommended** 

- Computational requirements: the nano-sized model is a sensible starting point for an RTX 3050 Ti Laptop GPU with 4 GB VRAM. 

- Transfer learning: pretrained weights can be adapted to the four road-damage classes rather than training from scratch. 

- Deployment: the same model can support image uploads, video processing, and camera-based demonstrations. 

The prior discussion noted that YOLO26 has dedicated detection and segmentation variants, pretrained weights, and export support. The nano detection model was cited as having approximately 2.4 million parameters in its published configuration. 

### **Proposed model experiment sequence** 

|**Experiment**|**Model**|**Purpose**|
|---|---|---|
|1|YOLO26n|Primary model.|
|2|YOLO11n|Performance comparison.|
|3|YOLO26n-seg|Optional advanced segmentation<br>experiment.|



## **5. Dataset selection and preparation** 

### **RDD2022 — Road Damage Dataset** 

RDD2022 was recommended as the main dataset. The dataset contains approximately 47,420 road images collected across six countries: India, Japan, Czech Republic, Norway, the United States, and China. Its annotations include roaddamage categories such as D00, D10, D20, and D40. 

The initial recommendation is to start with the Indian data because the application is intended for Indian road conditions. Road surfaces, repair practices, markings, lighting, and damage appearances can vary by region. Additional countries can later be included to improve generalization. 

The previous discussion included the following approximate official challenge split counts: 

|**Country**|**Training images**|**Test images**|
|---|---|---|
|India|9,000|1,000|
|Japan|10,000|1,000|



AI-Based Smart Road Damage Detection System  •  5 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

|**Country**|**Training images**|**Test images**|
|---|---|---|
|Czech Republic|2,000|1,000|
|Norway|9,000|1,000|
|United States|5,000|1,000|
|China|3,500|1,000|



#### **Important split consideration** 

The official challenge test images are distributed without corresponding annotations in the cited repository. Create the project validation and test splits from annotated training data. Avoid leakage: where possible, split by capture sequence or road segment instead of randomly splitting near-identical frames. 

### **Suggested YOLO dataset structure** 

RoadDamageDataset/ |-- images/ |   |-- train/ |   |-- val/ |   `-- test/ | |-- labels/ |   |-- train/ |   |-- val/ |   `-- test/ | `-- data.yaml 

Each image has a corresponding annotation file containing the damage class and normalized bounding-box coordinates. 

### **Annotation conversion: Pascal VOC XML to YOLO** 

RDD2022 provides Pascal VOC XML annotations. YOLO uses a text format with class ID and normalized bounding-box center, width, and height. 

Example source annotation: <object> <name>D40</name> <bndbox> <xmin>100</xmin> <ymin>150</ymin> <xmax>300</xmax> <ymax>350</ymax> </bndbox> </object> Example YOLO line: 3 0.3125 0.4167 0.3125 0.3333 

- Class ID 3 represents the pothole class in this illustrative mapping. 

- The next two values represent the normalized bounding-box center coordinates. 

- The final two values represent normalized width and height. 

The four categories must have one consistent numerical mapping throughout training, validation, and inference. 

AI-Based Smart Road Damage Detection System  •  6 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

### **Initial dataset split** 

|**Subset**|**Percentage**|
|---|---|
|Training|70%|
|Validation|15%|
|Testing|15%|



## **6. Fine-tuning methodology** 

The proposed training method is transfer learning through supervised fine-tuning. A pretrained YOLO26 model already contains general visual feature knowledge such as edges, textures, shapes, and patterns. Fine-tuning adapts those weights to the road-damage categories using images paired with ground-truth annotations. 

### **Training workflow** 

1. Dataset preparation: download RDD2022, select the Indian images, convert annotations, remove corrupt or incorrectly annotated samples, inspect class distribution, and create train/validation/test splits. 

2. Image preprocessing: resize while preserving aspect ratio, normalize, and apply appropriate augmentation. 

3. Model initialization: load pretrained YOLO26n weights. 

4. Training: fine-tune the model on the custom dataset. 

5. Validation: evaluate on images not used for weight updates. 

6. Optimization: adjust hyperparameters, image resolution, and augmentation based on validation results. 

7. Final testing: evaluate the best checkpoint on the independent test set. 

### **Image preprocessing and augmentation** 

- Resizing and aspect-ratio preservation. 

- Image normalization. 

- Brightness and contrast augmentation. 

- Limited rotation and perspective transformation. 

- Blur and noise augmentation. 

- Appropriate horizontal flipping. 

Road cracks can be extremely thin. Aggressive resizing and cropping may remove them, so the preprocessing pipeline should preserve small damage features. 

### **Initial training configuration** 

|**Parameter**|**Initial value**|
|---|---|
|Base model|YOLO26n|
|Training approach|Transfer learning|
|Image size|512|
|Epochs|80 maximum|
|Batch size|2|
|Optimizer|Automatic initial selection|
|Precision|Mixed precision, where supported|
|Early stopping patience|15–20 epochs|



AI-Based Smart Road Damage Detection System  •  7 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

|**Parameter**|**Initial value**|
|---|---|
|Dataset|RDD2022 India|
|GPU|CUDA|



These are starting parameters, not guaranteed optimal settings. A short training test should be run first to check GPU memory use. Cloud GPU training is an alternative if full training is inconvenient locally. 

### **Illustrative Python training implementation** 

from ultralytics import YOLO # Load pretrained model model = YOLO("yolo26n.pt") # Fine-tune on our custom road damage dataset results = model.train( data="road_damage.yaml", epochs=80, imgsz=512, batch=2, device=0, workers=2, patience=20, amp=True, cache=False, project="RoadDamage", name="YOLO26n_Experiment" ) # Validate the trained model metrics = model.val(data="road_damage.yaml") print(metrics) 

After training, the best checkpoint is expected under a path similar to the following. The best.pt file is the primary trained model, selected using validation performance. 

runs/detect/RoadDamage/ `-- YOLO26n_Experiment/ `-- weights/ |-- best.pt `-- last.pt 

### **Controlled fine-tuning experiments** 

|**Experiment**|**Training data**|**Objective**|
|---|---|---|
|A|India only|Establish a baseline.|
|B|India + other countries|Explore improved generalization.|
|C|India + locally collected road images|Adapt to local road conditions.|



For a smaller dataset, an optional two-stage strategy is to freeze parts of the backbone initially and subsequently unfreeze them. This can help investigate training stability and overfitting. 

AI-Based Smart Road Damage Detection System  •  8 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

LoRA and QLoRA are not necessary for this initial object-detection implementation; conventional transfer learning and supervised fine-tuning are the appropriate starting methods. 

## **7. Adding locally collected Indian road images** 

RDD2022 provides a strong foundation, but it should not be the only source of images. Collect photographs of roads around campus and nearby locations to test performance on local conditions. 

- Potholes of different sizes. 

- Cracks under different lighting conditions. 

- Damaged roads after rainfall. 

- Repaired roads and tar patches. 

- Roads with shadows and road markings. 

- Different types of pavement. 

The discussion suggested 200–500 properly annotated local images as a useful additional domain-specific experiment. The actual benefit depends on diversity and annotation quality. 

CVAT was recommended for annotation. It supports bounding boxes, polygon masks, and related annotation workflows. 

**CVAT official website:** <u>https://www.cvat.ai/</u> 

## **8. Object detection versus image segmentation** 

### **Option A — Object detection (Version 1)** 

The detector identifies damaged regions using rectangular bounding boxes. Example outputs include damage type and confidence score, such as “Pothole — 94.3%” or “Longitudinal Crack — 89.6%”. 

Advantages: easier annotation, faster training, lower implementation complexity, reuse of existing RDD2022 bounding-box annotations, and a good foundation for real-time demonstrations. 

Limitation: a rectangular bounding box does not precisely describe the shape of an irregular crack. 

### **Option B — Instance segmentation (advanced version)** 

Instance segmentation predicts a pixel-level mask for each damaged region. This can provide more detailed localization and support calculations such as damaged pixel area, crack length in pixels, crack width in pixels (with suitable measurement methods), and pothole surface area in pixels. 

A candidate is yolo26n-seg.pt. However, standard RDD2022 bounding-box annotations cannot directly train an instancesegmentation model; additional polygon or mask annotations are required. 

#### **Recommended two-stage methodology** 

Version 1: fine-tune YOLO26n for object detection using RDD2022. Version 2: experiment with YOLO26n-seg using a smaller manually annotated dataset. Do not claim that bounding-box size alone provides engineering severity. Physical measurements require scale calibration, camera geometry, and suitable measurement references. 

## **9. Application architecture and technology stack** 

The recommendation is to keep the initial software stack practical and avoid adding frameworks that are not needed for the core project. 

|**Technology**|**Usage**|
|---|---|
|Python|Main programming language.|



AI-Based Smart Road Damage Detection System  •  9 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

|**Technology**|**Usage**|
|---|---|
|PyTorch|Deep-learning framework.|
|Ultralytics|YOLO model training and inference.|
|OpenCV|Image processing and video handling.|
|NumPy|Image and numerical operations.|
|Pandas|Analysis and reporting.|
|CVAT|Image annotation.|
|FastAPI|Backend API.|
|Streamlit or React|User interface.|
|SQLite|Inspection database.|
|Folium / Leaflet|Geographical visualization.|
|Matplotlib|Training graphs and evaluation.|



### **Frontend option 1 — Streamlit** 

Recommended for the first working prototype. It is quick to develop, integrates directly with Python and YOLO, and supports image/video uploads, detection visualization, metrics, charts, and downloadable reports. 

### **Frontend option 2 — React + FastAPI** 

Recommended for a more customized, production-style interface. It provides a separate frontend and AI backend, more control over presentation, and a better foundation for a larger application. It requires more development effort. 

#### **Frontend recommendation** 

Build the model and initial application using Streamlit first. The interface can later be replaced with React without retraining the model. 

### **Proposed application modules** 

|**Module**|**Key functionality**|
|---|---|
|1. Dashboard|Show total inspected images, detected potholes, detected cracks,<br>and category statistics.|
|2. Image Inspection|Upload an image and display original and AI-annotated versions side<br>by side.|
|3. Live / Video Inspection|Process recorded videos or live camera feeds and show detections<br>frame by frame.|
|4. Geographical Damage Mapping|Display detected damage locations using GPS coordinates, when<br>available.|
|5. Inspection Reports|Generate reports containing damage images, categories, confidence<br>scores, timestamps, and coordinates.|



AI-Based Smart Road Damage Detection System  •  10 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

### **Avoiding duplicate counts in video** 

If a video is processed frame by frame, the same pothole may appear in hundreds of frames. It should not be counted as hundreds of separate potholes. Object tracking such as ByteTrack can track the same damage region across consecutive frames and reduce duplicate counting. 

## **10. Model evaluation and experiments** 

Object detection needs metrics beyond a single generic accuracy percentage. The proposed evaluation measures are: 

|**Metric**|**Meaning**|
|---|---|
|Precision|Of the predicted damages, how many were correct?|
|Recall|Of the actual damages, how many did the model detect?|
|F1-score|Balance between precision and recall.|
|mAP@50|Detection performance at IoU threshold 0.50.|
|mAP@50–95|Detection performance across multiple IoU thresholds.|
|Confusion matrix|Shows which damage categories are being confused.|
|Inference time|Time required to process an image.|
|FPS|Number of video frames processed per second.|



Performance should also be reported separately for each damage category. A model may identify potholes well but struggle with small longitudinal cracks; an overall mAP value alone can conceal that weakness. 

### **Proposed model comparison table** 

|**Metric**|**YOLO26n**|**YOLO11n**|
|---|---|---|
|Precision|To measure|To measure|
|Recall|To measure|To measure|
|mAP50|To measure|To measure|
|mAP50–95|To measure|To measure|
|Inference time|To measure|To measure|
|Model size|To measure|To measure|



All comparison values must come from actual experiments rather than estimated or invented results. This comparison gives the project a proper experimental component. 

## **11. Complete implementation roadmap** 

|**Phase**|**Main activities**|**Deliverable**|
|---|---|---|
|1. Research and dataset preparation|Study research; download RDD2022; inspect<br>Indian images and annotations; convert VOC to<br>YOLO; clean data; inspect class distribution;<br>create splits.|Verified and prepared road-damage dataset.|
||Set up Python, PyTorch and Ultralytics; load<br>i||
|2. Model development|pretrained YOLO26n; test inference; fine-tune;<br>save best checkpoint; validate.|Fine-tuned road-damage detection model.|



AI-Based Smart Road Damage Detection System  •  11 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

|**Phase**|**Main activities**|**Deliverable**|
|---|---|---|
|3. Model optimization|Optimize image size and batch size; experiment<br>with augmentation; compare YOLO26n and<br>YOLO11n; collect local images; evaluate local<br>performance.|Selected model with evaluation results.|
|4. Application development|Build Streamlit dashboard; integrate model;<br>implement image uploads and video processing;<br>draw boxes and confidence scores; show<br>statistics.|Working road-damage detection application.|
|5. Advanced functionality|GPS mapping; inspection history; video tracking;<br>PDF reports; experimental severity estimation;<br>segmentation.|Advanced smart road inspection system.|
|6. Testing and documentation|Test unseen images; evaluate failure cases;<br>measure speed; prepare graphs and confusion<br>matrices; document methodology and<br>architecture; prepare report and presentation.|Complete IPCV project and demonstration.|



#### **Implementation priority** 

Prioritize Phases 1–4. Phases 5–6 add value, but a properly working core system is more important than implementing too many optional features. 

## **12. Engineering considerations and limitations** 

- Do not train from scratch. Pretrained weights reduce unnecessary computation and training time. 

- Do not start with a large model. YOLO26n is a more sensible starting point for a 4 GB GPU. If full training is inconvenient locally, use a cloud GPU and bring the trained checkpoint back for local inference. 

- Do not immediately implement segmentation. Establish a successful detection pipeline first. 

- Do not rely exclusively on benchmark data. Include independently collected Indian road images to test performance outside the original dataset. 

- Do not present predictions as guaranteed road-safety assessments. The system is a visual screening and reporting tool, not a certified pavement engineering assessment. Confidence scores and severity estimates should be labelled accordingly. 

### **Licensing consideration** 

The prior discussion noted that Ultralytics uses AGPL-3.0 for its free offering and provides official licensing guidance. Review the applicable terms, especially if the project is intended to remain private or be developed commercially. Academic coursework and distribution requirements should be checked against the current terms before finalizing the framework. 

**Ultralytics licensing:** <u>https://www.ultralytics.com/license</u> 

## **13. Recommended initial project configuration** 

|**Area**|**Component**|**Selection**|
|---|---|---|
|AI / ML|Primary model|YOLO26n|
|AI / ML|Framework|PyTorch|
|AI / ML|Model library|Ultralytics|
|AI / ML|Dataset|RDD2022 India|
|AI / ML|Training|Supervised fine-tuning / transfer learning|



AI-Based Smart Road Damage Detection System  •  12 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

|**Area**|**Component**|**Selection**|
|---|---|---|
|AI / ML|Task|Object detection|
|AI / ML|Classes|D00, D10, D20, D40|
|AI / ML|Secondary model|YOLO11n|
|Image processing|Processing|OpenCV|
|Image processing|Numerical operations|NumPy|
|Image processing|Augmentation|Model training pipeline|
|Image processing|Annotation|CVAT|
|Application|Initial frontend|Streamlit|
|Application|Backend|Python / FastAPI|
|Application|Database|SQLite|
|Application|Visualization|Matplotlib|
|Application|GPS mapping|Folium|
|Deployment|Export format|ONNX (optional)|



### **Expected core deliverables** 

- Custom fine-tuned road-damage detection model. 

- Image-based damage detection. 

- Video-based damage detection. 

- Detection visualization and statistics. 

- Model evaluation and comparison. 

- Working application and project report. 

## **14. Decisions to finalize before implementation** 

The conversation ended by identifying three architectural decisions to settle before starting implementation. 

### **Decision 1 — Input types** 

|**Option**|**Scope**|
|---|---|
|Images only|Simplest implementation.|
|Images + prerecorded videos|Recommended balance.|
|Images + videos + live camera feed|Most complete input support; additional implementation effort.|



### **Decision 2 — Training and inference location** 

|**Option**|**Scope**|
|---|---|
|Entirely on laptop|Training and inference locally.|
|Cloud training, local inference|Use cloud compute for training and run the final model locally.|
|Flexible|Use whichever environment is more efficient.|



AI-Based Smart Road Damage Detection System  •  13 

**IPCV PROJECT  |  SMART ROAD DAMAGE DETECTION** 

### **Decision 3 — Project complexity** 

|**Option**|**Scope**|
|---|---|
|Basic|Detection, classification and visualization.|
|Intermediate|Detection, dashboard, GPS and reports.|
|Advanced|Segmentation, tracking, severity estimation and mapping.|



#### **Personal recommendation from the discussion** 

Images + prerecorded videos; cloud-assisted training with local inference; and the intermediate project scope. The first development task should be setting up the repository, downloading RDD2022, inspecting annotations, and creating a reliable dataset preparation and conversion pipeline. 

## **15. Resource links** 

The following resources were linked or named in the project discussion: 

**RDD2022 GitHub repository:** <u>https://github.com/sekilab/RoadDamageDetector</u> **RDD2022 official dataset page:** <u>https://crddc2022.sekilab.global/data/</u> **RDD2022 research paper DOI:** <u>https://doi.org/10.1002/gdj3.260</u> **Ultralytics YOLO26 documentation:** <u>https://docs.ultralytics.com/models/yolo26/</u> **Ultralytics YOLO11 documentation:** <u>https://docs.ultralytics.com/models/yolo11/</u> **CVAT official website:** <u>https://www.cvat.ai/</u> **Ultralytics licensing guidance:** <u>https://www.ultralytics.com/license</u> 

##### **END OF PROJECT DISCUSSION** 

AI-Based Smart Road Damage Detection System  •  14 

