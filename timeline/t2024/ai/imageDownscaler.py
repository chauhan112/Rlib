import cv2
import numpy as np
from typing import Tuple, Union
from pathlib import Path

class ImageDownscaler:
    @staticmethod
    def calculate_new_dimensions(width: int, height: int, factor: float) -> Tuple[int, int]:
        new_width = int(width / factor)
        new_height = int(height / factor)
        return max(1, new_width), max(1, new_height)

    @staticmethod
    def reduce_resolution_cv2(image: Union[str, np.ndarray], factor: float, interpolation: int = cv2.INTER_AREA) -> np.ndarray:
        if isinstance(image, str):
            img = cv2.imread(image)
            if img is None:
                raise ValueError(f"Could not load image from path: {image}")
        else:
            img = image.copy()

        height, width = img.shape[:2]
        new_width, new_height = ImageDownscaler.calculate_new_dimensions(width, height, factor)
        return cv2.resize(img, (new_width, new_height), interpolation=interpolation)

    @staticmethod
    def reduce_resolution_numpy(image: Union[str, np.ndarray], factor: int) -> np.ndarray:
        if not isinstance(factor, int):
            raise ValueError("Factor must be an integer for NumPy method")

        if isinstance(image, str):
            img = cv2.imread(image)
            if img is None:
                raise ValueError(f"Could not load image from path: {image}")
        else:
            img = image.copy()

        height, width = img.shape[:2]
        if factor >= width or factor >= height:
            raise ValueError("Reduction factor too large for image dimensions")

        new_height = height - (height % factor)
        new_width = width - (width % factor)
        img = img[:new_height, :new_width]
        return img.reshape(new_height//factor, factor, new_width//factor, factor, -1).mean(axis=(1,3))

    @staticmethod
    def save_image(image: np.ndarray, output_path: str) -> None:
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(output_path, image):
            raise ValueError(f"Failed to save image to {output_path}")
class Main:
    def downscale(input_path, output_path = "out.jpg"):
        reduction_factor = 2.0
    
        try:
            downscaler = ImageDownscaler()
            reduced_cv2 = downscaler.reduce_resolution_cv2(input_path, reduction_factor)
            
            # if isinstance(reduction_factor, int):
            #     reduced_numpy = downscaler.reduce_resolution_numpy(input_path, reduction_factor)
            #     downscaler.save_image(reduced_numpy, "output_numpy.jpg")
            
            downscaler.save_image(reduced_cv2, output_path)
            
            original_img = cv2.imread(input_path)
            print(f"Original dimensions: {original_img.shape}")
            print(f"New dimensions: {reduced_cv2.shape}")
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
