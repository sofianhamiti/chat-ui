FROM public.ecr.aws/lambda/python:3.10

WORKDIR ${LAMBDA_TASK_ROOT}

COPY . .

RUN pip install --no-cache -r requirements.txt


CMD [ "handler.lambda_handler" ]