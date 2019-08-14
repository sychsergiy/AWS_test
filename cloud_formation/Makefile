OUTPUT_ZIP_FILENAME = function.zip
DEPENDENCIES_DIR = package
ROOT = ${PWD}

lambda_file = lambda.py
template = template.json
stack_name = awsFinalTest

s3_bucket = aws.cloudformation.test

push: build push_lambda
build: install_libs zip_libs zip_lambda cleanup

install_libs:
	pip2 install --target=./package pymysql

zip_libs:
	cd ${DEPENDENCIES_DIR} && \
	zip -r9 ${ROOT}/${OUTPUT_ZIP_FILENAME} . && \
	cd ${ROOT}

zip_lambda:
	zip -g ${OUTPUT_ZIP_FILENAME} ${lambda_file}
	zip -r9 ${ROOT}/${OUTPUT_ZIP_FILENAME} ./services && \
	cd ${ROOT}

cleanup:
	rm -rf ${DEPENDENCIES_DIR}

push_lambda:
	aws s3 cp ${ROOT}/${OUTPUT_ZIP_FILENAME} s3://${s3_bucket}/${OUTPUT_ZIP_FILENAME}

create_stack:
	aws cloudformation create-stack --stack-name ${stack_name} \
	--template-body file://./templates/${template} --capabilities CAPABILITY_IAM
