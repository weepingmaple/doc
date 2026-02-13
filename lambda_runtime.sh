#!/bin/bash

# Define your list of functions here
FUNCTIONS=(
    "my-python-function"
    "payment-service-prod"
    "user-auth-lambda"
    "data-processor-v2"
)

# ==========================================
# SCRIPT
# ======./====================================

BASE_BACKUP_DIR="lambda_backups"

echo "Starting batch upgrade for ${#FUNCTIONS[@]} functions..."
echo "All backups will be saved to: $BASE_BACKUP_DIR"
mkdir -p "$BASE_BACKUP_DIR"

# Loop through the array
for FUNCTION_NAME in "${FUNCTIONS[@]}"; do
    
    echo "Processing: $FUNCTION_NAME"

    # Create a specific folder for this function
    FUNC_DIR="$BASE_BACKUP_DIR/$FUNCTION_NAME"
    mkdir -p "$FUNC_DIR"

    # 1. Backup Code
    echo "  Downloading code..."
    DOWNLOAD_URL=$(aws lambda get-function --function-name "$FUNCTION_NAME" --query 'Code.Location' --output text 2>/dev/null)

    if [ $? -eq 0 ] && [ "$DOWNLOAD_URL" != "None" ]; then
        curl -s -o "$FUNC_DIR/code_backup.zip" "$DOWNLOAD_URL"
    else
        echo "  Error: Could not retrieve code for $FUNCTION_NAME. Skipping..."
        echo "FAILED: $FUNCTION_NAME (Code Download)" >> "$BASE_BACKUP_DIR/summary.log"
        continue
    fi

    # 2. Backup Config
    echo "  Backing up config..."
    aws lambda get-function-configuration --function-name "$FUNCTION_NAME" > "$FUNC_DIR/old_config.json"

    # 3. Update Runtime
    echo "  Updating to Python 3.11..."
    if aws lambda update-function-configuration \
        --function-name "$FUNCTION_NAME" \
        --runtime python3.11 > "$FUNC_DIR/new_config.json" 2>/dev/null; then
        
        echo "  Success: Updated to Python 3.11"
        echo "SUCCESS: $FUNCTION_NAME" >> "$BASE_BACKUP_DIR/summary.log"
    else
        echo "  Error: Update failed for $FUNCTION_NAME"
        echo "FAILED: $FUNCTION_NAME (Update)" >> "$BASE_BACKUP_DIR/summary.log"
    fi

done

echo "Summary log: $BASE_BACKUP_DIR/summary.log"
