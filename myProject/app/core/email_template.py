#信息模板
from pydantic import BaseModel

class EmailData(BaseModel):
    subject: str
    html_content: str

def generate_email_code_template(email_to: str, code: str) -> EmailData:
    subject = "重置密码验证码"
    html_content = f"""
    <p>尊敬的用户，您好！</p>
    <p>您正在尝试重置密码，您的验证码是：<strong>{code}</strong></p>
    <p>验证码有效期为5分钟，请尽快完成操作。</p>
    """
    return EmailData(subject=subject, html_content=html_content)