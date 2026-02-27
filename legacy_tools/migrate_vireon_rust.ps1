# VIREON IP Protection - Migration Script
# ========================================
# Moves proprietary Rust code to private repository

$ErrorActionPreference = "Stop"

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "VIREON IP PROTECTION - RUST CODE MIGRATION" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Configuration
$PRIVATE_REPO = "https://github.com/symbeon-labs/vireon-core-proprietary.git"
$VIREON_PUBLIC = "c:\Users\João\Desktop\PROJETOS\03_AI_AGENTS\VIREON"
$TEMP_DIR = "c:\Users\João\Desktop\PROJETOS\03_AI_AGENTS\vireon-core-proprietary"

Write-Host "`n[STEP 1/5] Preparing environment..." -ForegroundColor Yellow
if (Test-Path $TEMP_DIR) {
    Write-Host "  Cleaning existing directory...: $TEMP_DIR" -ForegroundColor Yellow
    Remove-Item -Recurse -Force $TEMP_DIR
}

Write-Host "  Cloning private repository..." -ForegroundColor Yellow
git clone $PRIVATE_REPO $TEMP_DIR
Write-Host "  ✅ Cloned successfully" -ForegroundColor Green

Write-Host "`n[STEP 2/5] Creating directory structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "$TEMP_DIR\sage_x_rust_module" | Out-Null
New-Item -ItemType Directory -Force -Path "$TEMP_DIR\symbiotic_core" | Out-Null
Write-Host "  ✅ Directories created" -ForegroundColor Green

Write-Host "`n[STEP 3/5] Copying Rust source code (proprietary)..." -ForegroundColor Yellow

# sage_x_rust_module
if (Test-Path "$VIREON_PUBLIC\core\sage_x_rust_module\src") {
    Copy-Item -Recurse -Force "$VIREON_PUBLIC\core\sage_x_rust_module\src" "$TEMP_DIR\sage_x_rust_module\"
    Write-Host "  ✅ sage_x_rust_module/src" -ForegroundColor Green
}

if (Test-Path "$VIREON_PUBLIC\core\sage_x_rust_module\Cargo.toml") {
    Copy-Item -Force "$VIREON_PUBLIC\core\sage_x_rust_module\Cargo.toml" "$TEMP_DIR\sage_x_rust_module\"
    Write-Host "  ✅ Cargo.toml" -ForegroundColor Green
}

if (Test-Path "$VIREON_PUBLIC\core\sage_x_rust_module\Cargo.lock") {
    Copy-Item -Force "$VIREON_PUBLIC\core\sage_x_rust_module\Cargo.lock" "$TEMP_DIR\sage_x_rust_module\"
    Write-Host "  ✅ Cargo.lock" -ForegroundColor Green
}

# symbiotic_core Rust files
Write-Host "`n  Copying symbiotic_core Rust files..." -ForegroundColor Yellow
if (Test-Path "$VIREON_PUBLIC\core\symbiotic_core") {
    $rsFiles = Get-ChildItem "$VIREON_PUBLIC\core\symbiotic_core" -Filter "*.rs" -Recurse
    foreach ($file in $rsFiles) {
        $relativePath = $file.FullName.Substring(("$VIREON_PUBLIC\core\symbiotic_core").Length + 1)
        $destFile = Join-Path "$TEMP_DIR\symbiotic_core" $relativePath
        $destDir = Split-Path $destFile -Parent
        
        if (!(Test-Path $destDir)) {
            New-Item -ItemType Directory -Force -Path $destDir | Out-Null
        }
        
        Copy-Item $file.FullName $destFile -Force
        Write-Host "  ✅ $relativePath" -ForegroundColor Green
    }
}

Write-Host "`n[STEP 4/5] Creating README in private repo..." -ForegroundColor Yellow
$readme = @"
# VIREON Core - Proprietary Rust Engine

⚠️ **CONFIDENTIAL - Symbeon Labs Internal Use Only**

This repository contains the proprietary Rust implementation of VIREON's:
- Advanced governance algorithms
- Hallucination detection engine
- Performance-critical orchestration logic

## 📜 License

**© 2025 Symbeon Labs. All Rights Reserved.**

This code is confidential and proprietary. 
Unauthorized access, use, or distribution is strictly prohibited.

## 🔨 Building

````bash
# Build release binaries for distribution
cargo build --release --target x86_64-unknown-linux-gnu
cargo build --release --target x86_64-pc-windows-msvc
cargo build --release --target x86_64-apple-darwin
````

## 📦 Distribution

Compiled binaries (.so/.dll/.dylib) are distributed via the public repository:
**https://github.com/symbeon-labs/vireon**

**Source code is NEVER published.**

## 👥 Access

Only authorized Symbeon Labs team members have access to this repository.

---

**Created:** 2025-12-08  
**Maintainer:** JX (SH1W4)  
**License:** Proprietary
"@

Set-Content -Path "$TEMP_DIR\README.md" -Value $readme -Force
Write-Host "  ✅ README.md created" -ForegroundColor Green

Write-Host "`n[STEP 5/5] Committing and Pushing to PRIVATE repo..." -ForegroundColor Yellow
Push-Location $TEMP_DIR

# Ensure .gitignore exists to prevent clutter
if (-not (Test-Path ".gitignore")) {
    Set-Content -Path ".gitignore" -Value "target/`n**/*.rs.bk`n.DS_Store"
}

git add .
$status = git status --short

if ($status) {
    git commit -m "feat: initial import of proprietary Rust core"
    git push
    Write-Host "  ✅ Pushed to symbeon-labs/vireon-core-proprietary" -ForegroundColor Green
} else {
    Write-Host "  No changes to commit." -ForegroundColor Yellow
}

Pop-Location

Write-Host "`n[STEP 6/6] Cleaning up PUBLIC repo..." -ForegroundColor Yellow
Push-Location $VIREON_PUBLIC

# Remove source code but keep dir for binaries
if (Test-Path "core/sage_x_rust_module/src") {
    Remove-Item -Recurse -Force "core/sage_x_rust_module/src"
    Write-Host "  🗑️ Removed public Rust source (sage_x_rust_module)" -ForegroundColor Green
}

if (Test-Path "core/symbiotic_core") {
    Get-ChildItem "core/symbiotic_core" -Filter "*.rs" | Remove-Item -Force
    Write-Host "  �️ Removed public Rust source (symbiotic_core/*.rs)" -ForegroundColor Green
}

# Create placeholder for binaries
if (-not (Test-Path "core/sage_x_rust_module/lib")) {
    New-Item -ItemType Directory -Force -Path "core/sage_x_rust_module/lib" | Out-Null
}
Set-Content -Path "core/sage_x_rust_module/lib/.gitkeep" -Value ""

git add .
git commit -m "refactor: move proprietary Rust source to private repo (IP protection)"
git push

Write-Host "  ✅ Public repo cleaned and pushed" -ForegroundColor Green

Pop-Location

Write-Host "`n" 
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "✅ MIGRATION & CLEANUP COMPLETED SUCCESSFULLY" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
