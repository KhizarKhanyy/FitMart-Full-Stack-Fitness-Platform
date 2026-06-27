"""
══════════════════════════════════════════════════════════════
  FITMART — Email Service v2.0
  Supports: SMTP (Gmail/Mailgun/etc), SendGrid, Resend, Console
  Set EMAIL_PROVIDER env var: smtp | sendgrid | resend | console
══════════════════════════════════════════════════════════════
"""
import os
import smtplib
import html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from typing import Optional

# ── Config ────────────────────────────────────────────────
EMAIL_PROVIDER  = os.getenv("EMAIL_PROVIDER",  "console")
SMTP_HOST       = os.getenv("SMTP_HOST",       "smtp.gmail.com")
SMTP_PORT       = int(os.getenv("SMTP_PORT",   "587"))
SMTP_USER       = os.getenv("SMTP_USER",       "")
SMTP_PASSWORD   = os.getenv("SMTP_PASSWORD",   "")
FROM_EMAIL      = os.getenv("FROM_EMAIL",      "noreply@fitmart.pk")
FROM_NAME       = os.getenv("FROM_NAME",       "FitMart")
SENDGRID_KEY    = os.getenv("SENDGRID_API_KEY","")
RESEND_KEY      = os.getenv("RESEND_API_KEY",  "")
FRONTEND_URL    = os.getenv("FRONTEND_URL",    "http://localhost:5500")

# ── Template base ─────────────────────────────────────────
def _wrap(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{html.escape(title)}</title>
</head>
<body style="margin:0;padding:0;background:#080e14;font-family:'DM Sans',Arial,sans-serif;color:#edf4f0;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#080e14;padding:40px 20px;">
    <tr><td align="center">
      <table width="580" cellpadding="0" cellspacing="0" style="max-width:580px;width:100%;">
        <!-- Header -->
        <tr>
          <td style="background:#0e1c24;border-radius:20px 20px 0 0;padding:32px 40px;border-bottom:1px solid #1a2d3a;">
            <div style="display:flex;align-items:center;gap:12px;">
              <span style="font-size:24px;font-weight:800;letter-spacing:-1px;color:#edf4f0;">
                Fit<span style="color:#b5ff47;">Mart</span>
              </span>
            </div>
          </td>
        </tr>
        <!-- Body -->
        <tr>
          <td style="background:#0e1c24;padding:40px;border-radius:0 0 20px 20px;">
            {body}
            <div style="margin-top:40px;padding-top:24px;border-top:1px solid #1a2d3a;font-size:12px;color:rgba(237,244,240,0.4);line-height:1.8;">
              <p>© {datetime.utcnow().year} FitMart. All rights reserved.</p>
              <p>This email was sent to you because you have an account on FitMart.</p>
              <p>
                <a href="{FRONTEND_URL}" style="color:#b5ff47;text-decoration:none;">Visit FitMart</a> ·
                <a href="{FRONTEND_URL}/contact.html" style="color:#b5ff47;text-decoration:none;">Contact Support</a>
              </p>
            </div>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def _heading(text: str, sub: str = "") -> str:
    sub_html = f'<p style="margin:8px 0 0;font-size:15px;color:rgba(237,244,240,0.6);line-height:1.6;">{sub}</p>' if sub else ""
    return f"""<h1 style="margin:0 0 8px;font-size:26px;font-weight:800;letter-spacing:-1px;color:#edf4f0;">
      {html.escape(text)}
    </h1>{sub_html}<div style="margin:28px 0;height:1px;background:#1a2d3a;"></div>"""


def _btn(label: str, url: str, color: str = "#b5ff47") -> str:
    text_color = "#080e14" if color == "#b5ff47" else "#edf4f0"
    return f"""<div style="margin:28px 0;">
      <a href="{url}" style="display:inline-block;background:{color};color:{text_color};font-weight:700;font-size:14px;padding:14px 32px;border-radius:100px;text-decoration:none;letter-spacing:0.3px;">
        {html.escape(label)} →
      </a>
    </div>"""


def _info_row(label: str, value: str) -> str:
    return f"""<tr>
      <td style="padding:10px 0;font-size:13px;color:rgba(237,244,240,0.5);width:140px;">{html.escape(label)}</td>
      <td style="padding:10px 0;font-size:13px;color:#edf4f0;font-weight:500;">{html.escape(value)}</td>
    </tr>"""


def _alert_box(msg: str, severity: str = "warning") -> str:
    colors = {
        "critical": ("#ff6347", "rgba(255,99,71,0.08)", "🚨"),
        "warning":  ("#f59e0b", "rgba(245,158,11,0.08)", "⚠️"),
        "info":     ("#2dd4bf", "rgba(45,212,191,0.08)", "ℹ️"),
    }
    color, bg, icon = colors.get(severity, colors["warning"])
    return f"""<div style="background:{bg};border:1px solid {color}33;border-radius:12px;padding:16px 20px;margin:16px 0;font-size:14px;color:{color};line-height:1.6;">
      {icon} {html.escape(msg)}
    </div>"""


# ── Send function ──────────────────────────────────────────
def _send(to: str, subject: str, html_body: str):
    """Route email through configured provider."""
    provider = EMAIL_PROVIDER.lower().strip()

    if provider == "sendgrid" and SENDGRID_KEY:
        _send_sendgrid(to, subject, html_body)
    elif provider == "resend" and RESEND_KEY:
        _send_resend(to, subject, html_body)
    elif provider == "smtp" and SMTP_USER and SMTP_PASSWORD:
        _send_smtp(to, subject, html_body)
    else:
        # Console fallback — log to stdout (dev mode)
        _send_console(to, subject, html_body)


def _send_smtp(to: str, subject: str, html_body: str):
    msg = MIMEMultipart("alternative")
    msg["From"]    = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"]      = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as s:
            s.ehlo()
            s.starttls()
            s.login(SMTP_USER, SMTP_PASSWORD)
            s.sendmail(FROM_EMAIL, to, msg.as_string())
        print(f"[EMAIL] ✓ Sent to {to}: {subject}")
    except Exception as e:
        print(f"[EMAIL] ✗ SMTP failed for {to}: {e}")
        raise


def _send_sendgrid(to: str, subject: str, html_body: str):
    try:
        import httpx
        r = httpx.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={"Authorization": f"Bearer {SENDGRID_KEY}", "Content-Type": "application/json"},
            json={
                "personalizations": [{"to": [{"email": to}]}],
                "from": {"email": FROM_EMAIL, "name": FROM_NAME},
                "subject": subject,
                "content": [{"type": "text/html", "value": html_body}]
            },
            timeout=10
        )
        if r.status_code not in (200, 202):
            raise Exception(f"SendGrid HTTP {r.status_code}: {r.text[:200]}")
        print(f"[EMAIL] ✓ SendGrid to {to}: {subject}")
    except Exception as e:
        print(f"[EMAIL] ✗ SendGrid failed: {e}")
        raise


def _send_resend(to: str, subject: str, html_body: str):
    try:
        import httpx
        r = httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_KEY}", "Content-Type": "application/json"},
            json={"from": f"{FROM_NAME} <{FROM_EMAIL}>", "to": [to],
                  "subject": subject, "html": html_body},
            timeout=10
        )
        if r.status_code not in (200, 201):
            raise Exception(f"Resend HTTP {r.status_code}: {r.text[:200]}")
        print(f"[EMAIL] ✓ Resend to {to}: {subject}")
    except Exception as e:
        print(f"[EMAIL] ✗ Resend failed: {e}")
        raise


def _send_console(to: str, subject: str, html_body: str):
    """Dev mode: print email to console."""
    print(f"\n{'═'*60}")
    print(f"  📧 [DEV EMAIL] To: {to}")
    print(f"  Subject: {subject}")
    print(f"  Provider: console (set EMAIL_PROVIDER to send real emails)")
    print(f"{'═'*60}\n")


# ── Public API ────────────────────────────────────────────
def send_welcome(to: str, name: str, plan: str = "Basic"):
    subject = f"Welcome to FitMart, {name}! 🎉"
    body = _wrap(subject, f"""
      {_heading(f"Welcome, {name}!", "Your fitness journey starts now.")}
      <p style="font-size:15px;color:rgba(237,244,240,0.8);line-height:1.8;margin:0 0 20px;">
        You're now part of the FitMart community on the
        <strong style="color:#b5ff47;">{html.escape(plan)}</strong> plan.
        Here's what you can do right away:
      </p>
      <ul style="padding:0;margin:0 0 24px;list-style:none;">
        {''.join(f'<li style="padding:8px 0;font-size:14px;color:rgba(237,244,240,0.7);display:flex;gap:10px;"><span style=color:#b5ff47>✓</span>{t}</li>' for t in [
          'Log your first workout and track progress',
          'Record your health vitals (BP, heart rate, blood sugar)',
          'Generate an AI-powered workout plan tailored to you',
          'Book a doctor appointment for a health baseline',
        ])}
      </ul>
      {_btn("Go to Dashboard", f"{FRONTEND_URL}/dashboard.html")}
      <p style="font-size:13px;color:rgba(237,244,240,0.4);margin-top:20px;">
        Questions? Reply to this email or visit our
        <a href="{FRONTEND_URL}/contact.html" style="color:#b5ff47;">support page</a>.
      </p>
    """)
    _send(to, subject, body)


def send_password_reset(to: str, name: str, token: str):
    reset_url = f"{FRONTEND_URL}/auth-reset.html?token={token}"
    subject = "Reset your FitMart password"
    body = _wrap(subject, f"""
      {_heading("Password Reset", "Someone requested a password reset for your account.")}
      <p style="font-size:15px;color:rgba(237,244,240,0.8);line-height:1.8;margin:0 0 20px;">
        Hi <strong>{html.escape(name)}</strong>, click the button below to set a new password.
        This link expires in <strong style="color:#b5ff47;">30 minutes</strong>.
      </p>
      {_btn("Reset My Password", reset_url)}
      {_alert_box("If you didn't request this, you can safely ignore this email. Your password won't change.", "info")}
      <p style="font-size:12px;color:rgba(237,244,240,0.3);margin-top:20px;word-break:break-all;">
        Or paste this link in your browser:<br/>
        <span style="color:#b5ff47;">{html.escape(reset_url)}</span>
      </p>
    """)
    _send(to, subject, body)


def send_appointment_confirmation(to: str, name: str, doctor: str,
                                  date: str, time: str, appt_type: str):
    subject = f"Appointment Confirmed — {doctor} on {date}"
    body = _wrap(subject, f"""
      {_heading("Appointment Confirmed ✓", "Your booking has been received.")}
      <p style="font-size:15px;color:rgba(237,244,240,0.8);line-height:1.8;margin:0 0 24px;">
        Hi <strong>{html.escape(name)}</strong>, here are your appointment details:
      </p>
      <table cellpadding="0" cellspacing="0" style="width:100%;background:#091520;border-radius:14px;padding:4px 20px;border:1px solid #1a2d3a;">
        {_info_row("Doctor",     doctor)}
        {_info_row("Date",       date)}
        {_info_row("Time",       time or "To be confirmed")}
        {_info_row("Type",       appt_type)}
        {_info_row("Status",     "Pending Confirmation")}
      </table>
      {_btn("View My Appointments", f"{FRONTEND_URL}/appointment.html")}
      {_alert_box("Please arrive 10 minutes early for in-clinic appointments and ensure you have stable internet for video/phone consultations.", "info")}
    """)
    _send(to, subject, body)


def send_health_alert(to: str, name: str, alert_type: str,
                      message: str, safe_range: str):
    subject = f"🚨 Health Alert — Abnormal Reading Detected"
    body = _wrap(subject, f"""
      {_heading("Health Alert", "An abnormal vital reading was detected.")}
      <p style="font-size:15px;color:rgba(237,244,240,0.8);line-height:1.8;margin:0 0 20px;">
        Hi <strong>{html.escape(name)}</strong>, your recent health check flagged an abnormal reading
        that may need attention.
      </p>
      {_alert_box(message, "critical")}
      <table cellpadding="0" cellspacing="0" style="width:100%;background:#091520;border-radius:14px;padding:4px 20px;border:1px solid #1a2d3a;">
        {_info_row("Vital",      alert_type.replace('_',' ').title())}
        {_info_row("Safe Range", safe_range)}
        {_info_row("Action",     "Consult your doctor immediately if symptoms persist")}
      </table>
      {_btn("Book a Doctor Now", f"{FRONTEND_URL}/appointment.html", "#ff6347")}
      <p style="font-size:13px;color:rgba(237,244,240,0.4);margin-top:20px;line-height:1.7;">
        <strong style="color:#f59e0b;">Disclaimer:</strong> This is an automated alert based on the data you entered.
        It is not a medical diagnosis. Please consult a qualified healthcare provider for medical advice.
      </p>
    """)
    _send(to, subject, body)


def send_plan_upgrade(to: str, name: str, old_plan: str, new_plan: str):
    subject = f"Plan Upgraded to {new_plan} 🚀"
    body = _wrap(subject, f"""
      {_heading(f"You're now on {new_plan}!", f"Upgraded from {old_plan}.")}
      <p style="font-size:15px;color:rgba(237,244,240,0.8);line-height:1.8;margin:0 0 20px;">
        Hi <strong>{html.escape(name)}</strong>, your plan upgrade is active.
        Enjoy your enhanced benefits!
      </p>
      {_btn("Explore New Features", f"{FRONTEND_URL}/dashboard.html")}
    """)
    _send(to, subject, body)


def send_weekly_report(to: str, name: str, wellness_score: int,
                       workouts: int, calories: int, streak: int):
    score_color = "#b5ff47" if wellness_score>=70 else "#f59e0b" if wellness_score>=40 else "#ff6347"
    subject = f"Your Weekly FitMart Report — Score: {wellness_score}/100"
    body = _wrap(subject, f"""
      {_heading("Your Weekly Report 📊", f"Week ending {datetime.utcnow().strftime('%B %d, %Y')}")}
      <p style="font-size:15px;color:rgba(237,244,240,0.8);line-height:1.8;margin:0 0 24px;">
        Great work this week, <strong>{html.escape(name)}</strong>! Here's your summary:
      </p>
      <div style="background:#091520;border-radius:16px;padding:28px;border:1px solid #1a2d3a;text-align:center;margin-bottom:24px;">
        <div style="font-size:56px;font-weight:800;color:{score_color};letter-spacing:-3px;line-height:1;">{wellness_score}</div>
        <div style="font-size:13px;color:rgba(237,244,240,0.5);margin-top:6px;letter-spacing:2px;text-transform:uppercase;">Wellness Score</div>
      </div>
      <table cellpadding="0" cellspacing="0" style="width:100%;background:#091520;border-radius:14px;padding:4px 20px;border:1px solid #1a2d3a;">
        {_info_row("Workouts",         f"{workouts} sessions")}
        {_info_row("Calories Burned",  f"{calories:,} kcal")}
        {_info_row("Active Days",      f"{streak} day streak")}
      </table>
      {_btn("View Full Report", f"{FRONTEND_URL}/reports.html")}
    """)
    _send(to, subject, body)
