#!/bin/bash
set -e

# Remove old package and build dir
rm -f lambda_package.zip
rm -rf build_lambda

# Create build directory
BUILD_DIR=build_lambda
mkdir $BUILD_DIR

# Install dependencies into build dir
if [ -f requirements.txt ]; then
  pip install -r requirements.txt --target $BUILD_DIR
fi

# Copy src code and resume files
cp -r src $BUILD_DIR/
cp resume.txt $BUILD_DIR/
if [ -f RafaelBrito.pdf ]; then
  cp RafaelBrito.pdf $BUILD_DIR/
fi

# Create zip from build dir
cd $BUILD_DIR
zip -r ../lambda_package.zip .
cd ..

# Verify resume files are in the zip
for file in RafaelBrito.pdf resume.txt; do
  if unzip -l lambda_package.zip | grep -q "$file"; then
    echo "$file included in lambda_package.zip."
  else
    echo "ERROR: $file NOT found in lambda_package.zip!"
    exit 1
  fi
done

# Clean up build dir
rm -rf $BUILD_DIR

echo "Lambda package created successfully."