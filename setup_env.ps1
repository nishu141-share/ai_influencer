# Create tools directory
$toolsDir = "C:\Users\nishu\.gemini\antigravity\scratch\ai_influencer\tools"
if (!(Test-Path -Path $toolsDir)) {
    New-Item -ItemType Directory -Path $toolsDir | Out-Null
    Write-Host "Created tools directory."
}

# Install Fooocus
Set-Location $toolsDir
if (!(Test-Path "$toolsDir\Fooocus")) {
    Write-Host "Cloning Fooocus..."
    git clone https://github.com/lllyasviel/Fooocus.git
    Write-Host "Fooocus cloned. Note: The first run will download massive models (approx 6-10GB)."
}
else {
    Write-Host "Fooocus already exists."
}

# Setup Voice Directory
$voiceDir = "C:\Users\nishu\.gemini\antigravity\scratch\ai_influencer\voice_gen"
if (!(Test-Path -Path $voiceDir)) {
    New-Item -ItemType Directory -Path $voiceDir | Out-Null
    Write-Host "Created voice_gen directory."
}

# Setup Video Directory
$videoDir = "C:\Users\nishu\.gemini\antigravity\scratch\ai_influencer\video_gen"
if (!(Test-Path -Path $videoDir)) {
    New-Item -ItemType Directory -Path $videoDir | Out-Null
    Write-Host "Created video_gen directory."
}

# Install Python dependencies for Voice
Write-Host "Installing edge-tts..."
pip install edge-tts

# Install SadTalker (Video)
Set-Location $toolsDir
if (!(Test-Path "$toolsDir\SadTalker")) {
    Write-Host "Cloning SadTalker..."
    git clone https://github.com/OpenTalker/SadTalker.git
    
    Write-Host "SadTalker cloned."
    Write-Host "IMPORTANT: We have created a custom script to download only the essential models."
    Write-Host "Please run: .\tools\download_minimal_models.ps1"
    
    Write-Host "Installing SadTalker requirements..."
    Set-Location "$toolsDir\SadTalker"
    pip install -r requirements.txt
}
else {
    Write-Host "SadTalker already exists."
}

Write-Host "Setup script completed."
