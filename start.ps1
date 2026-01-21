# QuantResearch Quick Start Script
# This script starts both backend and frontend servers

Write-Host "🚀 Starting QuantResearch Application..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
$projectRoot = "c:\Users\PRAJWAL\OneDrive\Desktop\quantresearch\QuantResearch"
if (-not (Test-Path $projectRoot)) {
    Write-Host "❌ Error: Project directory not found!" -ForegroundColor Red
    Write-Host "Expected location: $projectRoot" -ForegroundColor Yellow
    exit 1
}

Set-Location $projectRoot

# Check Python installation
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js installation
Write-Host "🔍 Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📝 To start the application, you need TWO terminal windows:" -ForegroundColor Cyan
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "TERMINAL 1 - Backend Server (FastAPI)" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "cd `"$projectRoot`"" -ForegroundColor White
Write-Host "uvicorn src.quant_research_starter.api.main:app --reload --port 8000 --host 0.0.0.0" -ForegroundColor White
Write-Host ""
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "TERMINAL 2 - Frontend Server (React + Vite)" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "cd `"$projectRoot\src\quant_research_starter\frontend\cauweb`"" -ForegroundColor White
Write-Host "npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Frontend will be available at: http://localhost:3003" -ForegroundColor Green
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Quick Access URLs" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "🌐 Frontend App:     http://localhost:3003" -ForegroundColor White
Write-Host "🔌 Backend API:      http://localhost:8000" -ForegroundColor White
Write-Host "📚 API Docs:         http://localhost:8000/docs" -ForegroundColor White
Write-Host "❤️  Health Check:    http://localhost:8000/api/health" -ForegroundColor White
Write-Host ""

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Do you want to start the backend server now? (Y/N)" -ForegroundColor Yellow
$response = Read-Host
Write-Host ""

if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host "🚀 Starting Backend Server..." -ForegroundColor Cyan
    Write-Host "📖 For full documentation, see: SETUP_COMPLETE.md" -ForegroundColor Gray
    Write-Host ""
    
    # Start backend server
    uvicorn src.quant_research_starter.api.main:app --reload --port 8000 --host 0.0.0.0
} else {
    Write-Host "✅ Setup information displayed. Start servers manually when ready." -ForegroundColor Green
    Write-Host "📖 For detailed documentation, see: SETUP_COMPLETE.md" -ForegroundColor Gray
}
