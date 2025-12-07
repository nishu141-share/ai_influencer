$sadtalkerDir = "C:\Users\nishu\.gemini\antigravity\scratch\ai_influencer\tools\SadTalker"
$checkpointsDir = "$sadtalkerDir\checkpoints"
$gfpganDir = "$sadtalkerDir\gfpgan\weights"

# Ensure directories exist
if (!(Test-Path $checkpointsDir)) { New-Item -ItemType Directory -Path $checkpointsDir | Out-Null }
if (!(Test-Path $gfpganDir)) { New-Item -ItemType Directory -Path $gfpganDir | Out-Null }

# Using HuggingFace mirror for reliability
$models = @(
    @{
        Url  = "https://huggingface.co/wuhuikai/SadTalker/resolve/main/checkpoints/mapping_00229-model.pth.tar"
        Dest = "$checkpointsDir\mapping_00229-model.pth.tar"
    },
    @{
        Url  = "https://huggingface.co/wuhuikai/SadTalker/resolve/main/checkpoints/SadTalker_V0.0.2_256.safetensors"
        Dest = "$checkpointsDir\SadTalker_V0.0.2_256.safetensors"
    },
    @{
        Url  = "https://huggingface.co/wuhuikai/SadTalker/resolve/main/checkpoints/SadTalker_V0.0.2_512.safetensors"
        Dest = "$checkpointsDir\SadTalker_V0.0.2_512.safetensors"
    },
    @{
        Url  = "https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/facevid2vid_00189-model.pth.tar"
        Dest = "$checkpointsDir\facevid2vid_00189-model.pth.tar"
    },
    @{
        Url  = "https://github.com/Winfredy/SadTalker/releases/download/v0.0.2/wav2lip.pth"
        Dest = "$checkpointsDir\wav2lip.pth"
    }
)

Write-Host "Starting Minimal Model Download for SadTalker (Attempt 2)..."
Write-Host "Target Directory: $sadtalkerDir"

foreach ($model in $models) {
    if (!(Test-Path $model.Dest)) {
        Write-Host "Downloading $($model.Dest | Split-Path -Leaf)..."
        try {
            Start-BitsTransfer -Source $model.Url -Destination $model.Dest -ErrorAction Stop
            Write-Host "Downloaded."
        }
        catch {
            Write-Host "Download failed for $($model.Dest | Split-Path -Leaf): $_"
        }
    }
    else {
        Write-Host "$($model.Dest | Split-Path -Leaf) already exists. Skipping."
    }
}

Write-Host "Download complete! You are ready to generate videos."
