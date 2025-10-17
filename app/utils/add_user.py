from ..sec import SECRET_KEY, ALGORITHM
import jwt
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from decouple import config

sg = SendGridAPIClient(config('SENDGRID_API_KEY'))

async def encode_email_token(payload, expires_delta: int = 4320):
    """
    Encode a JWT token with the given payload and 72 hours expiration time.
    Args:
        payload (dict): The data to encode in the token.
        expires_delta (int, optional): Expiration time in minutes. Default is 120 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expires_delta)

    # Add issued-at and expiry
    to_encode.update({
        "iat": now,
        "exp": expire
    })

    # return encoded JWT token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def send_verification_email(email, token, username):
    """
    Send verification email to user
    
    Args:
        email: Recipient email address
        token: Verification token
        username: User's name for personalization
    """
    # placeholder for development testing
    backend_url = "http://127.0.0.1:8000"
    verification_link = f"{backend_url}/user/verify-email?token={token}"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4CAF50;">Welcome to ACSPTechAcademy! 🎉</h2>
                
                <p>Hi {username},</p>
                
                <p>Thank you for registering! Please verify your email address to activate your account.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_link}" 
                       style="background-color: #4CAF50; 
                              color: white; 
                              padding: 12px 30px; 
                              text-decoration: none; 
                              border-radius: 5px;
                              display: inline-block;
                              font-weight: bold;">
                        Verify Email Address
                    </a>
                </div>
                
                <p style="color: #666; font-size: 14px;">
                    This link will expire in 72 hours.
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #999; font-size: 12px;">
                    If you didn't create an account, please ignore this email.
                </p>
            </div>
        </body>
    </html>
    """
    try:
        print(f"Attempting to send verification email")
        
        message = Mail(
            from_email=Email(config('MAIL_FROM_EMAIL'), config('MAIL_FROM_NAME')),
            to_emails=To(email),
            subject='Verify Your Email - CAT FACT',
            html_content=Content("text/html", html_body)
        )
        
        response = sg.send(message)
        print("email successfully sent")    
    except Exception as e:
        print(f"Failed to send verification email: {str(e)}")


