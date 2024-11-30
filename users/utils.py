from pyotp import TOTP
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.conf import settings

def verify_token(token: str) -> bool:
    """verify a given token"""

    totp = TOTP(settings.SECRET_KEY, interval=6000)
    return totp.verify(token)

def get_token() -> str:
    """generate token for user verification"""

    totp = TOTP(settings.SECRET_KEY, interval=6000)
    token = totp.now()
    return token

# def send_mail(user_email: str, token: str) -> None:
#     """send verification email to user"""

#     html_content = f"""
#     <html>
#         <body>
#             <div style='margin: 5px; padding: 5px; color: rgb(23 37 84);
#                         background-color: rgb(239 246 255);
#                         font-family: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;'>
#                 <h1 style='margin: 5px; text-align: center; font-weight: bold;'>Enterprisiin</h1>
#                 <h2 style='margin: 5px; text-align: center; font-weight: bold;'>Verify Your Email</h2>
#                 <p><em style='font-size: 15px; text-align: center;'>
#                     Your account creation is almost complete. By confirming your email address, you let
#                     us know you are the rightful owner to this address
#                 </em></p>
#                 <p style='margin: 5px; text-align: center; font-weight: bolder;'>TOKEN: {token}</p>
#             </div>
#         </body>
#     </html>
#     """

#     msg = MIMEMultipart('alternative')
#     msg['From'] = settings.EMAIL_USER
#     msg['To'] = user_email
#     msg['Subject'] = 'Verify Your Email'
#     html_part = MIMEText(html_content, 'html')
#     msg.attach(html_part)
#     with SMTP(settings.EMAIL_HOST, port=settings.EMAIL_PORT) as connection:
#         connection.starttls()
#         connection.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
#         connection.sendmail(settings.EMAIL_USER, user_email, msg.as_string())


# def send_generated_otp_to_email(email, request): 
#     subject = "Welcome to Brand Me"
#     otp=random.randint(1000, 9999) 
#     current_site=  settings.FRONTEND_URL #get_current_site(request).domain
#     user = CustomUser.objects.get(email=email)
#     email_body = f"Hi {user.first_name},\n\nWelcome to {current_site}!\n\nWe're excited to be part of your professional growth journey. To stay updated on the latest developments with the Brand Me project and other relevant opportunities in your country, be sure to follow our social media pages.\n\nThe best way to get started is by logging in and exploring. If you'd prefer a more structured introduction, check out the 'How to Use' page for a detailed quickstart guide.\n\nQuick Tip: The website is accessible in multiple languages. Be sure to choose the language that works best for you!\n\nTo verify your email, please use the one-time passcode: {otp}\n\nIf you need any assistance, have suggestions, or encounter any issues, feel free to reach out via our contact form: https://www.nowbrandme.eu/contact\n\nCheers,\nThe Brand Me Project Team"

#     from_email=settings.EMAIL_HOST
#     otp_obj=OneTimePassword.objects.create(user=user, otp=otp)
#     #send the email 
#     d_email=EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[user.email])
#     d_email.send()





def custom_exception_handler(exc, context):
    # Get the standard response from DRF's default exception handler
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the error response structure
        custom_response = {
            "success": False,
            "status_code": response.status_code,
            "errors": response.data,
        }
        return Response(custom_response, status=response.status_code)

    # If no response is generated, return the default error
    return Response(
        {"success": False, "error": "An unexpected error occurred."}, status=500
    )
