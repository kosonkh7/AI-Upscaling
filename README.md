# AI based Image Super Resolution (Real-HAT-GAN)

## 🚀 Project Overview

This project provides a web-based AI image upscaling service. It leverages state-of-the-art deep learning models to enhance the resolution of images, making them clearer and more detailed. The backend is built with FastAPI for a robust API, and the frontend is a simple web interface for easy interaction.

For personal learning only. Not for commercial use.

## ✨ Features

-   **High-Quality Upscaling**: Utilizes the Hybrid Attention Transformer (HAT) model for superior image resolution enhancement.
-   **Selectable Upscaling Models**: Users can choose between different HAT models (e.g., general-purpose, realistic) directly from the web interface.
-   **Web Interface**: User-friendly web frontend for easy image upload and upscaling.
-   **RESTful API**: FastAPI backend provides a clean and efficient API for integration with other applications.
-   **GPU Acceleration Support**: Configured to leverage NVIDIA GPUs for faster processing.

## 🛠️ Technologies Used

-   **Backend**: Python, FastAPI, Uvicorn, PyTorch, BasicSR, GFPGAN, OpenCV, Pillow
-   **Frontend**: HTML, CSS, JavaScript
-   **AI Models**: Hybrid Attention Transformer (HAT)

### Hybrid Attention Transformer (HAT) Models
The HAT model is a state-of-the-art image super-resolution model based on the Transformer architecture. It is designed to effectively capture long-range dependencies and fine-grained details in images, leading to superior upscaling quality.

This project now supports multiple HAT models, allowing users to select their preferred upscaling style:

-   **HAT_SRx4_ImageNet-pretrain.pth**: A general-purpose HAT model pre-trained on the ImageNet dataset for 4x upscaling. It excels at producing high-fidelity, clean results.
-   **Real_HAT_GAN_SRx4.pth**: A GAN-based HAT model designed for more realistic and visually pleasing results, often with enhanced textures and details, also for 4x upscaling. This model might introduce more artistic interpretations compared to the ImageNet-pretrain version.

Users can select between these models directly from the web interface.

## 📚 References
This project was developed by integrating and adapting components from the following open-source projects and research:

- HAT (Hybrid Attention Transformer): Official GitHub repository for the HAT model. (https://github.com/XPixelGroup/HAT)
- BasicSR: An open-source image and video restoration toolbox based on PyTorch. Many utility functions and base classes are adapted from BasicSR. (https://github.com/XPixelGroup/BasicSR)
- Real-ESRGAN: Practical algorithms for Real-world Image Super-Resolution. The RealESRGANer utility class was adapted from this project. (https://github.com/xinntao/Real-ESRGAN)

## 📂 Project Structure

The project is organized into a separate frontend and backend, following a clear and maintainable structure.

```
AI-Upscaling/
├── backend/                  # FastAPI backend application for AI image upscaling
│   ├── __init__.py           # Initializes the backend Python package
│   ├── .env                  # Environment variables (e.g., for configuration)
│   ├── .gitignore            # Specifies intentionally untracked files to ignore
│   ├── requirements.txt      # Python dependencies required for the backend
│   ├── run.py                # Script to start the FastAPI application using Uvicorn
│   ├── test_upscale.py       # Unit tests for the upscaling service (if implemented)
│   ├── __pycache__/          # Python compiled bytecode cache
│   ├── app/                  # Core application logic for the FastAPI app
│   │   ├── __init__.py       # Initializes the 'app' Python package
│   │   ├── config.py         # Application-wide configuration, including model paths and settings
│   │   ├── main.py           # Main FastAPI application entry point and CORS setup
│   │   ├── __pycache__/      # Python compiled bytecode cache for 'app'
│   │   ├── api/              # API route definitions
│   │   │   ├── routes.py     # Defines API endpoints for image upscaling
│   │   │   └── __pycache__/  # Python compiled bytecode cache for 'api'
│   │   └── services/         # Business logic and service implementations
│   │       ├── realesrgan_utils.py # Utility functions for Real-ESRGAN and model loading
│   │       ├── upscale_service.py  # Core upscaling logic, loads and manages AI models
│   │       └── __pycache__/  # Python compiled bytecode cache for 'services'
│   ├── model_weights/        # Directory to store pre-trained AI model weights (.pth files)
│   └── models/               # Custom AI model architectures (e.g., HAT, SRVGG)
│       ├── __init__.py       # Initializes the 'models' Python package
│       ├── hat_arch.py       # Defines the Hybrid Attention Transformer (HAT) model architecture
│       ├── srvgg_arch.py     # Defines the SRVGG model architecture
│       └── __pycache__/      # Python compiled bytecode cache for 'models'
├── frontend/                 # Web frontend files for user interaction
│   ├── index.html            # Main HTML page for the web interface
│   ├── script.js             # JavaScript for dynamic frontend behavior and API calls
│   └── style.css             # CSS for styling the web interface
├── venv/                     # Python virtual environment (ignored by .gitignore)
│   ├── Include/...           # Standard Python virtual environment directories
│   ├── Lib/...
│   ├── Scripts/...
│   └── share/...
├── .gitignore                # Specifies files and directories to be ignored by Git
├── README.md                 # Project README file (this file)
└── .git/                     # Git version control metadata
```

## ⚙️ Setup and Installation

Follow these steps to get the project up and running on your local machine.

### Prerequisites

-   Python 3.8+ (Python 3.10+ recommended)
-   Git
-   **NVIDIA GPU with CUDA Toolkit 12.x installed**. This project is configured for GPU acceleration and requires a compatible environment.

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kosonkh7/AI-Upscaling.git
    cd AI-Upscaling
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate it
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install backend dependencies:**
    The `requirements.txt` file is specifically configured to work with a CUDA 12.x environment and installs some libraries directly from GitHub to ensure compatibility.
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  **Verify GPU availability:**
    After installation, run this command to ensure PyTorch can detect your GPU.
    ```python
    python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}')"
    ```
    This should output `GPU Available: True`. If not, please check your NVIDIA driver and CUDA Toolkit installation.

5.  **Download and place model weights:**
    The project uses multiple HAT models. Download their pre-trained weights and place them in the `backend/model_weights/` directory.
    -   **HAT_SRx4_ImageNet-pretrain.pth**: [Download Link](https://www.kaggle.com/datasets/djokester/hat-pre-trained-weights?resource=download)
    -   **Real_HAT_GAN_SRx4.pth**: [Download Link](https://www.kaggle.com/datasets/djokester/hat-pre-trained-weights?resource=download)
    -   **Placement**: Save the downloaded files to `backend/model_weights/`.

## 🚀 Usage

To run the service, you need to start the backend servers.

Or, you can use with **Docker Image.**

### Run with Backend API Server

Navigate to the project root and run the FastAPI application.
```bash
python backend/run.py
```
The backend API will start on `http://127.0.0.1:8000`. You will see logs from the Uvicorn server in this terminal.

### Run with Docker Container

In a new terminal, navigate to the `frontend` directory and start a simple Python web server.
```docker
docker pull kosonkh7/aisr-upscaler-gpu:v0.0.0
docker run --gpus all -d -p 8000:8000 kosonkh7/aisr-upscaler-gpu:v0.0.0
```
This will also start on `http://127.0.0.1:8000`.

You can now upload an image to be upscaled.

## 🔧 Troubleshooting

-   **`ModuleNotFoundError: No module named 'torchvision.transforms.functional_tensor'`**
    -   **Cause**: This error occurs because the standard versions of `basicsr` or `gfpgan` from PyPI are not compatible with recent versions of `torchvision`. The `functional_tensor` module was refactored in newer `torchvision` releases.
    -   **Solution**: This project's `requirements.txt` file resolves this by installing these libraries directly from their official GitHub repositories, which contain the latest compatibility fixes. If you encounter this error, ensure you have correctly installed the dependencies using `pip install -r backend/requirements.txt`.

## 💡 Future Improvements
-   **Memory Efficiency**: Address CUDA out-of-memory (OOM) issues by optimizing GPU memory usage and implementing smarter batch/image size handling.

-   **Model Diversity**: Integrate specialized models for different image types (e.g., faces, illustrations) to improve quality across various domains.
-   **Performance Optimization**: Explore ONNX/TensorRT conversion for further speedup.
-   **User Experience**: Enhance the frontend with progress indicators and before/after comparisons.

## 🤝 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.
