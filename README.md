# AI-Upscaling Project

## 🚀 Project Overview

This project provides a web-based AI image upscaling service. It leverages state-of-the-art deep learning models to enhance the resolution of images, making them clearer and more detailed. The backend is built with FastAPI for a robust API, and the frontend is a simple web interface for easy interaction.

## ✨ Features

-   **High-Quality Upscaling**: Utilizes the Hybrid Attention Transformer (HAT) model for superior image resolution enhancement.
-   **Web Interface**: User-friendly web frontend for easy image upload and upscaling.
-   **RESTful API**: FastAPI backend provides a clean and efficient API for integration with other applications.
-   **GPU Acceleration Support**: Configured to leverage NVIDIA GPUs for faster processing.

## 🛠️ Technologies Used

-   **Backend**: Python, FastAPI, Uvicorn, PyTorch, BasicSR, GFPGAN, OpenCV, Pillow
-   **Frontend**: HTML, CSS, JavaScript
-   **AI Models**: Hybrid Attention Transformer (HAT)

## 📂 Project Structure

The project is organized into a separate frontend and backend.

```
AI-Upscaling/
├── backend/                  # FastAPI backend application
│   ├── app/                  # Core application logic
│   │   ├── api/              # API routes
│   │   ├── services/         # Business logic (upscaling service)
│   │   ├── config.py         # Application configuration
│   │   └── main.py           # FastAPI app entry point
│   ├── models/               # Custom model architectures
│   ├── model_weights/        # Directory for pre-trained model weights (.pth)
│   ├── requirements.txt      # Python dependencies
│   └── run.py                # Script to run the FastAPI application
├── frontend/                 # Web frontend files
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .gitignore
├── README.md                 # This file
└── venv/                     # Python virtual environment (ignored)
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
    git clone https://github.com/your-username/AI-Upscaling.git
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
    The project uses the `HAT_SRx4_ImageNet-pretrain.pth` model. Download its pre-trained weights and place them in the `backend/model_weights/` directory.
    -   **Download Link**: [HAT_SRx4_ImageNet-pretrain.pth](https://github.com/XPixelGroup/HAT/releases/download/v0.1.0/HAT_SRx4_ImageNet-pretrain.pth)
    -   **Placement**: Save the downloaded file to `backend/model_weights/HAT_SRx4_ImageNet-pretrain.pth`.

## 🚀 Usage

To run the service, you need to start the backend and frontend servers separately in **two different terminals**.

### Terminal 1: Run the Backend (API Server)

Navigate to the project root and run the FastAPI application.
```bash
python backend/run.py
```
The backend API will start on `http://127.0.0.1:8000`. You will see logs from the Uvicorn server in this terminal.

### Terminal 2: Run the Frontend (Web Interface)

In a new terminal, navigate to the `frontend` directory and start a simple Python web server.
```bash
cd frontend
python -m http.server 3000
```
This will serve the `index.html` file on `http://127.0.0.1:3000`.

### Accessing the Application

Once both servers are running, open your web browser and go to:
> **http://127.0.0.1:3000**

You can now upload an image to be upscaled.

## 🔧 Troubleshooting

-   **`ModuleNotFoundError: No module named 'torchvision.transforms.functional_tensor'`**
    -   **Cause**: This error occurs because the standard versions of `basicsr` or `gfpgan` from PyPI are not compatible with recent versions of `torchvision`. The `functional_tensor` module was refactored in newer `torchvision` releases.
    -   **Solution**: This project's `requirements.txt` file resolves this by installing these libraries directly from their official GitHub repositories, which contain the latest compatibility fixes. If you encounter this error, ensure you have correctly installed the dependencies using `pip install -r backend/requirements.txt`.

## 💡 Future Improvements

-   **Model Diversity**: Integrate specialized models for different image types (e.g., faces, illustrations).
-   **Performance Optimization**: Explore ONNX/TensorRT conversion for further speedup.
-   **User Experience**: Enhance the frontend with progress indicators and before/after comparisons.

## 🤝 Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.
