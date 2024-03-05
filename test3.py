import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    # 발신자 이메일 계정 설정
    sender_email = "com"
    sender_password = ''

    # 수신자 이메일 주소 설정
    receiver_email = ""

    # SMTP 서버 설정 (예: Gmail SMTP)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # 이메일 내용 설정
    subject = "알림 울리는 지 체크"
    body = "빨리 가서 보셈"

    # 이메일 구성
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["X-Priority"] = "1"
    message.attach(MIMEText(body, "plain"))

    try:
        # SMTP 서버에 연결
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # 로그인
        server.login(sender_email, sender_password)

        # 이메일 전송
        server.sendmail(sender_email, receiver_email, message.as_string())

        # 연결 종료
        server.quit()

        print("이메일이 성공적으로 전송되었습니다.")
        
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")

send_email()