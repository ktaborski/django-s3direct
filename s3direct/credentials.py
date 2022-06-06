import datetime

from django.conf import settings

# django-s3direct accesses AWS credentials from Django config and provides
# an optional ability to retrieve credentials from EC2 instance profile if
# AWS settings are set to None. This optional ability requires botocore,
# however dependency on botocore is not enforced as this a secondary
# method for retrieving credentials.
try:
    from botocore import session
except ImportError:
    session = None



class CachedAWSCredentials:
    TTL=getattr(settings, 'S3DIRECT_CREDENTIALS_TTL', 30)
    secret_key=None
    access_key=None
    token=None
    updated=None
    
    @staticmethod
    def get():
        if not session:
            return CachedAWSCredentials
        now = datetime.datetime.now()
        if CachedAWSCredentials.updated is None or CachedAWSCredentials.expired(now):
            creds = session.get_session().get_credentials()
            CachedAWSCredentials.secret_key = creds.secret_key
            CachedAWSCredentials.access_key = creds.access_key
            CachedAWSCredentials.token = creds.token
            CachedAWSCredentials.updated = now
        return CachedAWSCredentials

    def expired(current_time):
        return (current_time - CachedAWSCredentials.updated).seconds > CachedAWSCredentials.TTL

        