LAMBDA_FILE_NAME = lambda.py
OUTPUT_ZIP_FILENAME = function.zip
DEPENDENCIES_DIR = package
ROOT = ${PWD}

S3_BUCKET = aws.cloudformation.test

build: install_libs zip_libs zip_lambda cleanup push_lambda

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

push_lambda:
	aws s3 cp ${ROOT}/${OUTPUT_ZIP_FILENAME} s3://${S3_Bucket}/${OUTPUT_ZIP_FILENAME}

create_stack:
	aws cloudformation create-stack --stack-name ${stack_name} \
	--template-body file://./template.json --capabilities CAPABILITY_IAM
