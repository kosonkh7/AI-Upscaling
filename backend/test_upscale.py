import asyncio
import os
import sys
from PIL import Image
import io
import numpy as np

print(f"Current working directory: {os.getcwd()}")
print(f"Python sys.path: {sys.path}")

# Assuming the current working directory is AI-Upscaling/backend
# Adjust the import path if the script is run from a different location
from backend.app.services.upscale_service import upscale_service

async def run_test():
    print("Starting upscale service test...")

    # 1. Create a dummy image (e.g., a small black square)
    original_size = (32, 32) # width, height
    dummy_image_pil = Image.new('RGB', original_size, color = 'black')

    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    dummy_image_pil.save(img_byte_arr, format='PNG')
    image_bytes = img_byte_arr.getvalue()

    print(f"Dummy image created: {original_size[0]}x{original_size[1]} pixels.")

    try:
        # 2. Call the upscale_image service
        print("Calling upscale_image service...")
        upscaled_image_bytes = await upscale_service.upscale_image(image_bytes)
        print("Upscale service call completed.")

        # 3. Save the upscaled image
        output_path = "upscaled_test_image.png"
        with open(output_path, "wb") as f:
            f.write(upscaled_image_bytes)

        # Verify the output image size (optional)
        upscaled_image_pil = Image.open(io.BytesIO(upscaled_image_bytes))
        print(f"Upscaled image saved to {output_path} with size: {upscaled_image_pil.size[0]}x{upscaled_image_pil.size[1]} pixels.")

        # Expected upscale is 4x, so 10x10 -> 40x40
        expected_width = original_size[0] * upscale_service.upsampler.scale
        expected_height = original_size[1] * upscale_service.upsampler.scale

        if upscaled_image_pil.size[0] == expected_width and upscaled_image_pil.size[1] == expected_height:
            print("Test successful: Upscaled image size matches expected size.")
        else:
            print("Test warning: Upscaled image size does NOT match expected size.")

    except Exception as e:
        print(f"Test failed with an error: {e}")

if __name__ == "__main__":
    # Run the async test function
    asyncio.run(run_test())
