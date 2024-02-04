rm -rf ./finished-docs
mkdir ./finished-docs
cp -r ./web-docs/site/* ./finished-docs
zip -r "./docs-out.zip" ./finished-docs/*