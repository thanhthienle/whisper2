mkdir -p RAW/data/RAW/train/waves/RAWTRAIN
mkdir -p RAW/data/RAW/dev/waves/RAWTEST
mkdir -p RAW/data/RAW/test/waves/RAWTEST
unzip -q RAW/train_data.zip
mv Train/* RAW/data/RAW/train/waves/RAWTRAIN/
rm -rf Train __MACOSX train_data.zip
echo "Done unzip and move"
python RAW/preprocess.py
echo "Done preprocess"
gzip RAW/data/prompts-*
tar -czf "RAW/data/RAW.tar.gz" RAW/data/RAW
echo "Done zipping"
