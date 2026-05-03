#!/bin/bash

# ============================================================
# fMRI Processing Pipeline (Robust + Cross-Platform)
# ============================================================

# Stop script on critical errors
set -e

# Create log file
LOG_FILE="pipeline_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -i "$LOG_FILE")
exec 2>&1

echo "=============================================="
echo "Starting Full Processing Pipeline"
echo "=============================================="
echo "Start Time: $(date)"
echo "Log File: $LOG_FILE"
echo

# Detect OS for sed compatibility
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_CMD="sed -i ''"
else
    SED_CMD="sed -i"
fi

# Loop over subjects
for id in $(seq -w 1 26); do

    subj="sub-$id"

    echo "----------------------------------------------"
    echo "Processing Subject: $subj"
    echo "----------------------------------------------"

    # Check if subject directory exists
    if [ ! -d "$subj" ]; then
        echo "ERROR: Directory $subj not found. Skipping..."
        continue
    fi

    cd "$subj" || exit
    echo "Entered directory: $(pwd)"

    # ========================================================
    # Step 1: Skull Stripping
    # ========================================================
    echo "Checking for brain extraction file..."

    if [ ! -f "anat/${subj}_T1w_brain_f02.nii.gz" ]; then
        echo "WARNING: Brain file not found. Running BET..."

        if [ -f "anat/${subj}_T1w.nii.gz" ]; then
            echo "Running bet2 on ${subj}_T1w.nii.gz"

            bet2 "anat/${subj}_T1w.nii.gz" \
                 "anat/${subj}_T1w_brain_f02.nii.gz" -f 0.2

            echo "Skull stripping completed"
        else
            echo "ERROR: Input MRI file not found. Skipping subject..."
            cd ..
            continue
        fi
    else
        echo "Brain file already exists. Skipping BET"
    fi

    # ========================================================
    # Step 2: Copy Design Files
    # ========================================================
    echo "Copying design files..."

    if cp ../design_run1.fsf . && cp ../design_run2.fsf .; then
        echo "Design files copied successfully"
    else
        echo "ERROR: Failed to copy design files"
        cd ..
        continue
    fi

    # ========================================================
    # Step 3: Update Subject ID in Design Files
    # ========================================================
    echo "Updating subject ID inside design files..."

    eval $SED_CMD "\"s|sub-08|${subj}|g\"" design_run1.fsf
    eval $SED_CMD "\"s|sub-08|${subj}|g\"" design_run2.fsf

    # Verify replacement worked
    if grep -q "$subj" design_run1.fsf && grep -q "$subj" design_run2.fsf; then
        echo "Design files updated correctly"
    else
        echo "ERROR: Design file update failed. Skipping subject..."
        cd ..
        continue
    fi

    # ========================================================
    # Step 4: Run FEAT Analysis
    # ========================================================
    echo "Starting FEAT analysis..."

    echo "Run 1 started at $(date)"
    if feat design_run1.fsf; then
        echo "Run 1 completed successfully"
    else
        echo "ERROR: Run 1 failed"
        cd ..
        continue
    fi

    echo "Run 2 started at $(date)"
    if feat design_run2.fsf; then
        echo "Run 2 completed successfully"
    else
        echo "ERROR: Run 2 failed"
        cd ..
        continue
    fi

    # ========================================================
    # Step 5: Finish Subject
    # ========================================================
    echo "Finished processing $subj"
    echo "End Time: $(date)"

    cd ..
    echo
done

echo "=============================================="
echo "All Subjects Processing Completed"
echo "End Time: $(date)"
echo "=============================================="
