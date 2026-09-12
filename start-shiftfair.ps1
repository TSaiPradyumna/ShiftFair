Write-Host ""
Write-Host "========================================"
Write-Host "       STARTING SHIFTFAIR 🚀"
Write-Host "========================================"
Write-Host ""

$ProjectRoot = "D:\shiftfair-starter\shiftfair"
$AppPath = "$ProjectRoot\shiftfair-app"
$VenvActivate = "$ProjectRoot\hackenv\Scripts\Activate.ps1"

# ----------------------------------------
# STEP 1: Check Docker
# ----------------------------------------

Write-Host "[1/6] Checking Docker..."

docker info *> $null

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker Desktop is not running."
    Write-Host "Please start Docker Desktop and run this script again."
    exit
}

Write-Host "Docker is running."

# ----------------------------------------
# STEP 2: Start LocalStack
# ----------------------------------------

Write-Host ""
Write-Host "[2/6] Starting LocalStack..."

& $VenvActivate

localstack start -d

Write-Host "Waiting for LocalStack..."

$maxAttempts = 30
$attempt = 0
$localstackReady = $false

while ($attempt -lt $maxAttempts) {

    Start-Sleep -Seconds 2

    $result = aws --endpoint-url=http://localhost:4566 dynamodb list-tables 2>$null

    if ($LASTEXITCODE -eq 0) {
        $localstackReady = $true
        break
    }

    $attempt++
    Write-Host "Waiting... ($attempt/$maxAttempts)"
}

if (-not $localstackReady) {
    Write-Host "ERROR: LocalStack did not start."
    exit
}

Write-Host "LocalStack is ready!"

# ----------------------------------------
# STEP 3: Check DynamoDB Table
# ----------------------------------------

Write-Host ""
Write-Host "[3/6] Checking DynamoDB table..."

$tableCheck = aws `
    --endpoint-url=http://localhost:4566 `
    dynamodb describe-table `
    --table-name ShiftFairTable `
    2>$null

if ($LASTEXITCODE -ne 0) {

    Write-Host "ShiftFairTable not found."
    Write-Host "Creating ShiftFairTable..."

    aws `
        --endpoint-url=http://localhost:4566 `
        dynamodb create-table `
        --table-name ShiftFairTable `
        --attribute-definitions `
            AttributeName=pk,AttributeType=S `
            AttributeName=sk,AttributeType=S `
        --key-schema `
            AttributeName=pk,KeyType=HASH `
            AttributeName=sk,KeyType=RANGE `
        --billing-mode PAY_PER_REQUEST

    Write-Host "ShiftFairTable created!"

}
else {

    Write-Host "ShiftFairTable already exists!"

}

# ----------------------------------------
# STEP 4: Build SAM
# ----------------------------------------

Write-Host ""
Write-Host "[4/6] Building SAM application..."

Set-Location $AppPath

sam build

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: SAM build failed."
    exit
}

Write-Host "SAM build successful!"

# ----------------------------------------
# STEP 5: Start SAM API
# ----------------------------------------

Write-Host ""
Write-Host "[5/6] Starting SAM API in new terminal..."

Start-Process powershell `
    -ArgumentList @(
        "-NoExit",
        "-Command",
        "cd '$ProjectRoot'; & '$VenvActivate'; cd '$AppPath'; sam local start-api --docker-network shiftfair-net"
    )

Start-Sleep -Seconds 5

# ----------------------------------------
# STEP 6: Complete
# ----------------------------------------

Write-Host ""
Write-Host "========================================"
Write-Host "       SHIFTFAIR IS STARTING! 🚀"
Write-Host "========================================"
Write-Host ""
Write-Host "API:"
Write-Host "http://127.0.0.1:3000"
Write-Host ""
Write-Host "Endpoints:"
Write-Host "POST /swap-request"
Write-Host "GET  /roster"
Write-Host "GET  /decisions"
Write-Host ""
Write-Host "LocalStack:"
Write-Host "http://localhost:4566"
Write-Host ""
Write-Host "SAM API is running in a separate terminal."