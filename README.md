# AI-Upscaling Project

## 🚀 Project Overview

This project provides a web-based AI image upscaling service. It leverages state-of-the-art deep learning models to enhance the resolution of images, making them clearer and more detailed. The backend is built with FastAPI for a robust API, and the frontend is a simple web interface for easy interaction.

## ✨ Features

-   **High-Quality Upscaling**: Utilizes the Hybrid Attention Transformer (HAT) model for superior image resolution enhancement.
-   **Web Interface**: User-friendly web frontend for easy image upload and upscaling.
-   **RESTful API**: FastAPI backend provides a clean and efficient API for integration with other applications.
-   **GPU Acceleration Support**: Configured to leverage NVIDIA GPUs for faster processing (if available and properly set up).

## 🛠️ Technologies Used

-   **Backend**: Python, FastAPI, Uvicorn, PyTorch, Basicsr, OpenCV, PIL
-   **Frontend**: HTML, CSS, JavaScript
-   **AI Models**: Hybrid Attention Transformer (HAT)

### Hybrid Attention Transformer (HAT) Model

The HAT model is a state-of-the-art image super-resolution model based on the Transformer architecture. It is designed to effectively capture long-range dependencies and fine-grained details in images, leading to superior upscaling quality. This project utilizes a pre-trained HAT model (specifically `HAT_SRx4_ImageNet-pretrain.pth`) which was trained on the ImageNet dataset for 4x upscaling.

## 📚 References

This project was developed by integrating and adapting components from the following open-source projects and research:

-   **HAT (Hybrid Attention Transformer)**: Official GitHub repository for the HAT model. ([https://github.com/XPixelGroup/HAT](https://github.com/XPixelGroup/HAT))
-   **BasicSR**: An open-source image and video restoration toolbox based on PyTorch. Many utility functions and base classes are adapted from BasicSR. ([https://github.com/XPixelGroup/BasicSR](https://github.com/XPixelGroup/BasicSR))
-   **Real-ESRGAN**: Practical algorithms for Real-world Image Super-Resolution. The `RealESRGANer` utility class was adapted from this project. ([https://github.com/xinntao/Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN))

## 📂 Project Structure

```
AI-Upscaling/
├── backend/                  # FastAPI backend application
│   ├── app/                  # Core application logic
│   │   ├── api/              # API routes
│   │   ├── services/         # Business logic, including upscaling service
│   │   ├── config.py         # Application configuration
│   │   └── main.py           # FastAPI app entry point
├── models/               # Custom model architectures (e.g., HAT, Real-ESRGAN components)
├── model_weights/        # Directory for storing pre-trained model weights (.pth files)
├── requirements.txt      # Python dependencies for the backend
├── run.py                # Script to run the FastAPI application
├── frontend/                 # Web frontend files
│   ├── index.html
│   ├── script.js
│   └── style.css
├── README.md                 # Project README file
└── venv/                     # Python virtual environment (ignored by Git)
```

## ⚙️ Setup and Installation

Follow these steps to get the project up and running on your local machine.

### Prerequisites

-   Python 3.8+ (Recommended: Python 3.10)
-   Git
-   (Optional for GPU acceleration) NVIDIA GPU with compatible drivers and CUDA Toolkit installed.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/AI-Upscaling.git
    cd AI-Upscaling
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install backend dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **(Important for GPU Usage) Install PyTorch with CUDA support:**
    If you have an NVIDIA GPU and want to utilize it for faster upscaling, you **must** install the correct PyTorch version that supports your CUDA Toolkit.
    
    First, uninstall any existing PyTorch installations:
    ```bash
    pip uninstall torch torchvision torchaudio
    ```
    Then, visit the official PyTorch website ([https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)) to get the exact installation command for your specific CUDA version (e.g., CUDA 11.8, CUDA 12.1). An example command might look like this:
    ```bash
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    ```
    Verify GPU availability:
    ```python
    python -c "import torch; print(torch.cuda.is_available())"
    ```
    This should output `True` if GPU setup is successful.

5.  **Download and place model weights:**
    The project uses the `HAT_SRx4_ImageNet-pretrain.pth` model. You need to download its pre-trained weights and place them in the `backend/model_weights/` directory.
    
    -   **Download Link**: [HAT_SRx4_ImageNet-pretrain.pth](https://github.com/XPixelGroup/HAT/releases/download/v0.1.0/HAT_SRx4_ImageNet-pretrain.pth)
    -   **Placement**: Save the downloaded file as `backend/model_weights/HAT_SRx4_ImageNet-pretrain.pth`.

## 🚀 Usage

### Running the Backend Server

Navigate to the project root directory (`AI-Upscaling/`) and run:

```bash
python backend/run.py
```

The backend API will be available at `http://127.0.0.1:8000`.

### Accessing the Frontend

Open `frontend/index.html` in your web browser. You can upload an image and see the upscaled result.

### API Endpoint

-   **Endpoint**: `/upscale`
-   **Method**: `POST`
-   **Content-Type**: `multipart/form-data`
-   **Form Field**: `file` (your image file)

Example using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/upscale" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/image.png;type=image/png" \
     --output upscaled_image_output.png
```

## 💡 Future Improvements & Considerations

-   **Model Diversity**: Integrate specialized models for different image types (e.g., faces, illustrations, text) to improve quality across various domains.
-   **Performance Optimization**: Explore ONNX/TensorRT conversion for further speedup, and refine tiling strategies for large images.
-   **User Experience**: Enhance the frontend with features like progress indicators, before/after comparisons, and support for more image formats.
-   **Error Handling**: Implement more robust and user-friendly error messages.

## 🤝 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For any questions or feedback, please open an issue on GitHub.
