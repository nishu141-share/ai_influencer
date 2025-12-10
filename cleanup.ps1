# AI Influencer Project Cleanup Script
# This script removes unnecessary files and folders

Write-Host "🧹 AI Influencer Project Cleanup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Error: Please run this script from the ai_influencer directory" -ForegroundColor Red
    exit 1
}

Write-Host "⚠️  WARNING: This will delete files and folders!" -ForegroundColor Yellow
Write-Host "   Make sure you have a backup before proceeding." -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Do you want to continue? (yes/no)"

if ($confirm -ne "yes") {
    Write-Host "❌ Cleanup cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Starting cleanup..." -ForegroundColor Green
Write-Host ""

# Track what we're removing
$removed = @()
$failed = @()

# Function to remove item safely
function Remove-ItemSafe {
    param($Path, $Description)
    
    if (Test-Path $Path) {
        try {
            Remove-Item -Path $Path -Recurse -Force
            Write-Host "✅ Removed: $Description" -ForegroundColor Green
            $script:removed += $Description
        } catch {
            Write-Host "❌ Failed to remove: $Description" -ForegroundColor Red
            $script:failed += $Description
        }
    } else {
        Write-Host "⏭️  Skipped (not found): $Description" -ForegroundColor Gray
    }
}

Write-Host "📦 Removing reference projects..." -ForegroundColor Cyan
Remove-ItemSafe "AI-Influencer" "AI-Influencer reference project"
Remove-ItemSafe "Text-To-Video-AI" "Text-To-Video-AI reference project"
Remove-ItemSafe "gemini-youtube-automation" "gemini-youtube-automation reference project"

Write-Host ""
Write-Host "📄 Removing old/duplicate files..." -ForegroundColor Cyan
Remove-ItemSafe "main_agent.py" "Old main_agent.py"
Remove-ItemSafe "README.md" "Old README.md"
Remove-ItemSafe "Start_Fooocus.bat" "Unrelated Start_Fooocus.bat"
Remove-ItemSafe "character_prompt.txt" "character_prompt.txt"
Remove-ItemSafe "hello_world.mp3" "Test file hello_world.mp3"
Remove-ItemSafe "output_audio.mp3" "Test file output_audio.mp3"

Write-Host ""
Write-Host "📁 Removing old output folders..." -ForegroundColor Cyan
Remove-ItemSafe "output_agent_video" "Empty output_agent_video folder"
Remove-ItemSafe "output\indian_influencer_avatar.png" "Old test avatar"
Remove-ItemSafe "output\test_voice.mp3" "Old test voice"

# Remove old dated output folders
Get-ChildItem -Path "output" -Directory | Where-Object { $_.Name -match "^\d{4}_\d{2}_\d{2}_" } | ForEach-Object {
    Remove-ItemSafe $_.FullName "Old output folder: $($_.Name)"
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "🎉 Cleanup Summary" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Successfully removed: $($removed.Count) items" -ForegroundColor Green

if ($failed.Count -gt 0) {
    Write-Host "❌ Failed to remove: $($failed.Count) items" -ForegroundColor Red
    Write-Host ""
    Write-Host "Failed items:" -ForegroundColor Red
    $failed | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
}

Write-Host ""
Write-Host "📊 Disk space freed: Run 'Get-ChildItem -Recurse | Measure-Object -Property Length -Sum' to check" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Test the system: python main.py --video-type short_form" -ForegroundColor White
Write-Host "2. Commit changes: git add . && git commit -m 'Cleaned up project'" -ForegroundColor White
Write-Host ""
