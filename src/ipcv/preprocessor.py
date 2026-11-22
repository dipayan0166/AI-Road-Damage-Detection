"""
IPCV Preprocessing Module
Classical Image Processing techniques tailored for road defect inspection:
1. CLAHE (Contrast Limited Adaptive Histogram Equalization) in LAB color space
   - Overcomes harsh direct Indian sunlight and dense tree canopy shadows.
2. Bilateral Filtering
   - Smooths coarse asphalt aggregate noise while preserving sharp crack edges.
3. Region of Interest (ROI) Road Masking
   - Filters out top 20-30% of camera frames (sky, horizon, trees, overhead wires).
"""

import cv2
import numpy as np
from typing import Tuple, Optional

class RoadImagePreprocessor:
    def __init__(
        self,
        clahe_clip_limit: float = 2.5,
        clahe_tile_grid: Tuple[int, int] = (8, 8),
        bilateral_d: int = 5,
        bilateral_sigma_color: float = 50.0,
        bilateral_sigma_space: float = 50.0,
        roi_top_crop_ratio: float = 0.20
    ):
        self.clahe_clip_limit = clahe_clip_limit
        self.clahe_tile_grid = clahe_tile_grid
        self.bilateral_d = bilateral_d
        self.bilateral_sigma_color = bilateral_sigma_color
        self.bilateral_sigma_space = bilateral_sigma_space
        self.roi_top_crop_ratio = roi_top_crop_ratio
        
        # Initialize OpenCV CLAHE object
        self.clahe = cv2.createCLAHE(
            clipLimit=self.clahe_clip_limit,
            tileGridSize=self.clahe_tile_grid
        )

    def apply_clahe(self, image_bgr: np.ndarray) -> np.ndarray:
        """
        Apply CLAHE on the Lightness (L) channel in LAB color space.
        Enhances local contrast of thin cracks without distorting asphalt color balance.
        """
        # Convert BGR to LAB color space
        lab = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        
        # Apply CLAHE to L-channel
        enhanced_l = self.clahe.apply(l_channel)
        
        # Merge back and convert to BGR
        enhanced_lab = cv2.merge((enhanced_l, a_channel, b_channel))
        enhanced_bgr = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        return enhanced_bgr

    def apply_bilateral_filter(self, image_bgr: np.ndarray) -> np.ndarray:
        """
        Smooth high-frequency gravel/tar grain noise while preserving sharp crack boundaries.
        """
        return cv2.bilateralFilter(
            image_bgr,
            d=self.bilateral_d,
            sigmaColor=self.bilateral_sigma_color,
            sigmaSpace=self.bilateral_sigma_space
        )

    def extract_road_roi(self, image_bgr: np.ndarray) -> Tuple[np.ndarray, Tuple[int, int, int, int]]:
        """
        Mask out non-road regions (sky, horizon, overhead wires) from the top of the frame.
        Returns: (cropped_image, (x1, y1, x2, y2))
        """
        h, w = image_bgr.shape[:2]
        crop_y = int(h * self.roi_top_crop_ratio)
        roi = image_bgr[crop_y:h, 0:w]
        bbox_coords = (0, crop_y, w, h)
        return roi, bbox_coords

    def preprocess_pipeline(
        self,
        image_bgr: np.ndarray,
        use_clahe: bool = True,
        use_bilateral: bool = False,
        use_roi_mask: bool = False
    ) -> Tuple[np.ndarray, Optional[Tuple[int, int, int, int]]]:
        """
        Execute full classical preprocessing pipeline.
        """
        processed = image_bgr.copy()
        roi_box = None
        
        if use_roi_mask:
            processed, roi_box = self.extract_road_roi(processed)
            
        if use_clahe:
            processed = self.apply_clahe(processed)
            
        if use_bilateral:
            processed = self.apply_bilateral_filter(processed)
            
        return processed, roi_box

    def generate_comparison_image(self, image_bgr: np.ndarray) -> np.ndarray:
        """
        Generate a side-by-side comparison (Raw vs CLAHE Enhanced) for visual evaluation.
        """
        enhanced = self.apply_clahe(image_bgr)
        h, w = image_bgr.shape[:2]
        
        # Draw labels on images
        raw_labeled = image_bgr.copy()
        enh_labeled = enhanced.copy()
        
        cv2.putText(raw_labeled, "Original Raw Image", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(enh_labeled, "CLAHE Contrast Enhanced", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
        
        comparison = np.hstack((raw_labeled, enh_labeled))
        return comparison

