import os
import resend
from dotenv import load_dotenv
from agents.synthesizer import load_latest_briefing, DailyBriefing

load_dotenv()


def _build_html(briefing: DailyBriefing) -> str:
    articles_html = ""
    for article in briefing.articles:
        articles_html += f"""
        <div style="margin-bottom:40px; border-left:3px solid #e0e0e0; padding-left:20px;">
          <h2 style="margin:0 0 4px 0; font-size:18px;">
            <a href="{article.url}" style="color:#1a1a1a; text-decoration:none;">{article.title}</a>
          </h2>
          <p style="color:#888; font-size:13px; margin:0 0 16px 0;">Source: {article.source}</p>

          <p style="margin:0 0 4px 0; font-size:13px; font-weight:700; color:#2563eb;">📈 Market</p>
          <p style="margin:0 0 16px 0; font-size:14px; line-height:1.6; color:#333;">{article.market}</p>

          <p style="margin:0 0 4px 0; font-size:13px; font-weight:700; color:#16a34a;">🔬 Tech</p>
          <p style="margin:0 0 16px 0; font-size:14px; line-height:1.6; color:#333;">{article.tech}</p>

          <p style="margin:0 0 4px 0; font-size:13px; font-weight:700; color:#9333ea;">🏛 Society</p>
          <p style="margin:0 0 16px 0; font-size:14px; line-height:1.6; color:#333;">{article.society}</p>

          <p style="margin:0 0 4px 0; font-size:13px; font-weight:700; color:#ea580c;">👤 User</p>
          <p style="margin:0 0 0 0; font-size:14px; line-height:1.6; color:#333;">{article.user}</p>
        </div>
        """

    return f"""
    <html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                       max-width:680px; margin:0 auto; padding:32px 24px; color:#1a1a1a;">
      <h1 style="font-size:24px; margin:0 0 4px 0;">AI News Briefing</h1>
      <p style="color:#888; font-size:14px; margin:0 0 32px 0;">
        Four perspectives on today's AI news. You decide what matters. · {briefing.date}
      </p>
      {articles_html}
      <hr style="border:none; border-top:1px solid #e0e0e0; margin:32px 0 16px 0;">
      <p style="color:#aaa; font-size:12px; margin:0;">
        AI News Briefing · {briefing.article_count} articles · {briefing.date}
      </p>
    </body></html>
    """


def send_briefing() -> None:
    briefing = load_latest_briefing()
    if briefing is None:
        raise RuntimeError("No briefing found. Run the pipeline first.")

    resend.api_key = os.environ["RESEND_API_KEY"]
    email_to = os.environ["EMAIL_TO"]
    email_from = os.getenv("EMAIL_FROM") or "onboarding@resend.dev"

    params: resend.Emails.SendParams = {
        "from": email_from,
        "to": [email_to],
        "subject": f"AI News Briefing · {briefing.date}",
        "html": _build_html(briefing),
    }

    response = resend.Emails.send(params)
    print(f"Email sent. ID: {response['id']}")


if __name__ == "__main__":
    send_briefing()
