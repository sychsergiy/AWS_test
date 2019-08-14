LAMBDA_FILE_NAME = lambda.py
OUTPUT_ZIP_FILENAME = function.zip
DEPENDENCIES_DIR = package
ROOT = ${PWD}

build: install_libs zip_libs zip_lambda cleanup

install_libs:
	pip2 install --target=./package pymysql

zip_libs:
	cd ${DEPENDENCIES_DIR} && \
	zip -r9 ${ROOT}/${OUTPUT_ZIP_FILENAME} . && \
	cd ${ROOT}

zip_lambda:
	zip -g ${OUTPUT_ZIP_FILENAME} ${LAMBDA_FILE_NAME}

cleanup:
	rm -rf ${DEPENDENCIES_DIR}