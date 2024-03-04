import boto3

from myapp import config


def send_otp(email_address, otp):
    template = f'<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2"><div style="margin:50px auto;width:70%;padding:20px 0"><div style="border-bottom:1px solid #eee"><a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">MyApp</a></div><p style="font-size:1.1em">Hi,</p><p>Thank you for choosing MyApp. Use the following OTP to complete your Login.</p><h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2><p style="font-size:0.9em;">Regards,<br />MyApp</p><hr style="border:none;border-top:1px solid #eee" /><div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300"><p>MyApp</p><p>Hyderabad</p><p>Chennai</p></div></div></div>'

    client = boto3.client(
        "ses",
        region_name="ap-south-1",
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    )

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
        Source="noreply@MyApp.in",
    )
