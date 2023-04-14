run_ls:
	docker run -it --rm -p 8080:8080 -v $(PWD)/label_studio:/label-studio/data \
	--env LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true \
	--env LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/label-studio/files \
	-v $(PWD)/tmp:/label-studio/files heartexlabs/label-studio:latest label-studio

voc2coco:
	python3 src/voc2coco.py

voc2ls:
	python3 src/voc2ls.py