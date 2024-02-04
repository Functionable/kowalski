mkdir -p ./web-docs/docs/api-reference/classes ./web-docs/docs/api-reference/libraries
cp ./out/classes/* ./web-docs/docs/api-reference/classes
cp ./out/libraries/* ./web-docs/docs/api-reference/libraries
cp ./out/events/* ./web-docs/docs/api-reference/events
cp ./out/enums/* ./web-docs/docs/api-reference/enums
cp ./out/mkdocs.yml ./web-docs/mkdocs.yml
cp ./out/globals.md ./web-docs/docs/api-reference/globals.md
