#! /bin/bash
base_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2021-"

# Define an array of months
months=("01" "02" "03" "04" "05" "06" "07")

local_airflow_path="$1"


# Loop through each month and download the file
for month in "${months[@]}"; do
    url="${base_url}${month}.csv.gz"  # Construct full URL
    filename="green_tripdata_2021-${month}.csv.gz"
    
    echo "[DONWLOADING]: $filename..."
    
    curl -L $url > "$local_airflow_path/dataset/$filename" # -L follows redirects

    echo "[DOWNLOADED]: $filename!!!"
    
    # Check if the file exists and extract it
    if [ -f $local_airflow_path/dataset/$filename ]; then
        echo "[EXTRACTING]: $filename ..."
        gunzip "$local_airflow_path/dataset/$filename"
        echo "[EXTRACTED]: $filename!!!"
    else
        echo "❌ Extracting failed for: $filename"
    fi

done

echo "✅ All downloads and extractions completed!"