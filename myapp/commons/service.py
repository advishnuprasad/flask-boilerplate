import boto3

from myapp import config


class EmailService:
    @classmethod
    def ses_client(cls):
        return boto3.client(
            "ses",
            region_name="ap-south-1",
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        )

    @classmethod
    def send_verification_mail(cls, email_address, complete_registration_link):
        template = f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">myapp</a></div><p style="font-size:1.1em">Hi,</p><p>Thank you for choosing myapp. Use the following link to verify your Email.</p><p>{complete_registration_link}</p><p style="font-size:0.9em;">Regards,<br />myapp</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300"><p>myapp</p><p>Hyderabad</p><p>Chennai</p></div></div></div>'

        client = cls.ses_client()

        client.send_email(
            Destination={
                "ToAddresses": [email_address],
            },
            Message={
                "Body": {"Html": {"Charset": "UTF-8", "Data": template}},
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": "Verify your email for myapp",
                },
            },
            Source="noreply@myapp.in",
        )

    @classmethod
    def send_otp_mail(cls, email_address, otp):
        template = f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">myapp</a></div><p style="font-size:1.1em">Hi,</p><p>Thank you for choosing myapp. Use the following OTP to complete your Login.</p><h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2><p style="font-size:0.9em;">Regards,<br />myapp</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300"><p>myapp</p><p>Hyderabad</p><p>Chennai</p></div></div></div>'

        client = cls.ses_client()

        client.send_email(
            Destination={
                "ToAddresses": [email_address],
            },
            Message={
                "Body": {"Html": {"Charset": "UTF-8", "Data": template}},
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": "Your Login OTP for MyApp",
                },
            },
            Source="noreply@myapp.in",
        )

    @classmethod
    def send_reset_password_email(cls, email_address, reset_link):
        template = f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">myapp</a></div><p style="font-size:1.1em">Hi,</p><p>Thank you for choosing myapp. Use the following link to reset your password.</p><p>{reset_link}</p><p style="font-size:0.9em;">Regards,<br />myapp</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300"><p>myapp</p><p>Hyderabad</p><p>Chennai</p></div></div></div>'

        client = cls.ses_client()

        client.send_email(
            Destination={
                "ToAddresses": [email_address],
            },
            Message={
                "Body": {"Html": {"Charset": "UTF-8", "Data": template}},
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": "Reset password link for myapp",
                },
            },
            Source="noreply@myapp.in",
        )
