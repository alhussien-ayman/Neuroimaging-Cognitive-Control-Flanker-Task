#!/bin/bash

# 1. تحديد المسار الحالي (تأكد أنك واقف في الفولدر اللي فيه ملفات الـ nii.gz)
BASE=$(pwd)

# 2. تحديد ملفات الـ Input
Z_CON="$BASE/allZstats_cope2.nii.gz"
Z_INCON="$BASE/allZstats_cope1.nii.gz"
Z_DIFF="$BASE/allZstats.nii.gz"

# 3. الفولدر اللي هيطلع فيه النتائج
OUTDIR="$BASE/ROI_results_new"
mkdir -p "$OUTDIR"

# 4. مسار الـ Template الأساسي
TEMPLATE=$FSLDIR/data/standard/MNI152_T1_2mm_brain.nii.gz

# 5. قائمة الإحداثيات (بناءً على مخرجاتك الأخيرة)
# الصيغة: "رقم_المنطقة X Y Z"
ROIs=(
"1 39 25 62"
"2 66 19 33"
"3 18 32 26"
"4 21 66 47"
"5 44 72 58"
"6 29 74 32"
)

# 6. حلقة التكرار لمعالجة كل حالة (con, incon, diff)
for cond in con incon diff; do
    
    # تحديد الملف المستخدم بناءً على الحالة
    if [ "$cond" == "con" ]; then
        ZMAP=$Z_CON
    elif [ "$cond" == "incon" ]; then
        ZMAP=$Z_INCON
    else
        ZMAP=$Z_DIFF
    fi

    # التأكد من وجود ملف الـ Z-stat قبل البدء
    if [ ! -f "$ZMAP" ]; then
        echo "Warning: $ZMAP not found, skipping $cond..."
        continue
    fi

    # حلقة التكرار لكل ROI داخل كل حالة
    for line in "${ROIs[@]}"; do
        read -r ROI_ID X Y Z <<< "$line"

        echo "Processing ROI $ROI_ID ($cond) at Voxel [$X $Y $Z]..."

        MASK="${OUTDIR}/ROI${ROI_ID}_${cond}_mask.nii.gz"
        OUTTXT="${OUTDIR}/ROI${ROI_ID}_${cond}_Z.txt"

        # إنشاء الـ Mask الكروي (5mm) مباشرة واستخراج القيم
        # الخطوة أ: إنشاء Seed وتكبيره ليكون كرة ثم تحويله لـ Binary
        fslmaths "$TEMPLATE" -mul 0 -add 1 -roi "$X" 1 "$Y" 1 "$Z" 1 0 1 \
                 -kernel sphere 5 -fmean -bin "$MASK"

        # الخطوة ب: استخراج المتوسط الحسابي للقيم داخل الـ Mask
        fslmeants -i "$ZMAP" -m "$MASK" -o "$OUTTXT"
    done
done

echo "----------------------------------------------"
echo "Done! Check your results in: $OUTDIR"
echo "----------------------------------------------"