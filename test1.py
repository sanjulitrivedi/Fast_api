import boto3  # pip install boto3

# Let's use Amazon S3
s3 = boto3.client("s3")
s3.upload_file(
    Filename="/Users/sanjulitrivedi/Documents/orm_Session/test1.py",
    Bucket="test1234567891234567",
    Key="uploaded_by_Sanjuli",
)