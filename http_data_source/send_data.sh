set -e

# Exit if conda environment not activated
if [[ $CONDA_DEFAULT_ENV != "firehose-demo-data-source" ]]; then
    echo "Conda environment must be activated!"
    echo ""
    exit 1
fi

python send_data.py $1