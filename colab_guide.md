# Running SadTalker on Google Colab (Free GPU)

Since your local machine only has a CPU, video generation takes ~6 hours. On Google Colab (Free Tier), this will take **~2-5 minutes**.

### Step 1: Open Google Colab
Go to [https://colab.research.google.com/](https://colab.research.google.com/) and create a **New Notebook**.

### Step 2: Enable GPU
1. Go to **Runtime** > **Change runtime type**.
2. Set **Hardware accelerator** to **T4 GPU**.
3. Click **Save**.

### Step 3: Copy & Run these Code Blocks

**Cell 1: Setup & Install (Runs in ~2 mins)**
```python
# 1. Clone SadTalker & Install Dependencies
!git clone https://github.com/OpenTalker/SadTalker.git
%cd SadTalker
!pip install -r requirements.txt
!pip install -U "huggingface_hub[cli]"

# 2. Download Checkpoints (Automated)
!mkdir -p checkpoints
!mkdir -p gfpgan/weights
!wget https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/mapping_00109-model.pth.tar -O checkpoints/mapping_00109-model.pth.tar
!wget https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_256.safetensors -O checkpoints/SadTalker_V0.0.2_256.safetensors
!wget https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/SadTalker_V0.0.2_512.safetensors -O checkpoints/SadTalker_V0.0.2_512.safetensors
!wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth -O gfpgan/weights/GFPGANv1.3.pth
!wget https://github.com/OpenTalker/SadTalker/releases/download/v0.0.2-rc/face_alignment_version.tar.gz
!tar -xf face_alignment_version.tar.gz -C checkpoints
```

**Cell 2: Fix NumPy 2.0 Compatibility**
```python
# Fix for NumPy 2.0+ compatibility

# Fix 1: Comment out the problematic warning line
!sed -i 's/warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)/# warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)/' /content/SadTalker/src/face3d/util/preprocess.py

# Fix 2: Add flatten to lstsq
!sed -i 's/k = np.linalg.lstsq(X_homo, pts68\[:, 0\])\[0\]/k = np.linalg.lstsq(X_homo, pts68[:, 0])[0].flatten()/' /content/SadTalker/src/face3d/util/preprocess.py

# Fix 3: Replace np.float with float
!sed -i 's/np\.float/float/g' /content/SadTalker/src/face3d/util/my_awing_arch.py

print("✅ NumPy compatibility patches applied!")
```

**Cell 3: Upload Your Files**
1. Click the **Folder icon** 📁 on the left sidebar.
2. Drag and drop your:
   - **Image**: `indian_influencer_avatar.png` (from your local output folder)
   - **Audio**: `generated_audio.mp3` (from your local output folder)

**Cell 4: Generate Video**
```python
# 3. Run Inference
# Adjust filenames if yours are different
!python inference.py \
    --driven_audio "/content/SadTalker/generated_audio.mp3" \
    --source_image "/content/SadTalker/indian_influencer_avatar.png" \
    --result_dir "/content/output" \
    --still \
    --preprocess full \
    --enhancer gfpgan 
```

### Step 4: Download Result
1. The video will appear in `output/` folder on the left.
2. Right-click the `.mp4` file and select **Download**.
