from ..sec import SECRET_KEY, ALGORITHM
import jwt
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from decouple import config
from fastapi import HTTPException, status

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
    backend_url = "https://acsp-cat-fact.pxxl.click"
    verification_link = f"{backend_url}/user/verify-email?token={token}"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4CAF50;">Welcome to ACSP CAT FACT !</h2>
                
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

async def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Please log in again.",
        )
    
async def send_welcome_email(email, username, user_id):
    """
    Send welcome email after successful verification
    
    Args:
        email: User's email
        username: User's name
    """
    backend_url = "https://acsp-cat-fact.pxxl.click"
    app_link = f"{backend_url}/user?q={user_id}"

    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4CAF50;">Welcome Onboard!</h2>
                
                <p>Hi {username},</p>
                
                <p>Your email has been verified successfully! You're all set to start using ACSP cat fact. the below is your user_id</p>

                <p>{user_id},</p>
                
                <p>Here's what you can do next:</p>
                <ul>
                    <li>click on the link below to generate your random cat fact</li>
                    <li>copy and store your user id somewhere safe</li>
                    <li>should incase you lose this mail, pass your user_id as a query parameter /user?user_id</li>
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{app_link}" 
                       style="background-color: #25D366; 
                              color: white; 
                              padding: 15px 40px; 
                              text-decoration: none; 
                              border-radius: 8px;
                              display: inline-block;
                              font-weight: bold;
                              font-size: 16px;
                              box-shadow: 0 4px 6px rgba(37, 211, 102, 0.3);">
                        Click the link to generate your random cat fact!
                    </a>
                </div>
                
                <p style="text-align: center; color: #666; font-size: 14px; margin-top: 20px;">
                    you can try as many times as you want!
                </p>
                
                <p>Thanks for your interest!</p>
                
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>ACSP CAT FACT</strong>
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
            subject='WELCOME TO CAT FACT',
            html_content=Content("text/html", html_body)
        )
        
        response = sg.send(message)
        print("email successfully sent")    
    except Exception as e:
        print(f"Failed to send verification email: {str(e)}")