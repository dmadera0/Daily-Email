from datetime import datetime


WEATHER_ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
}


def get_weather_icon(icon_key: str) -> str:
    return WEATHER_ICONS.get(icon_key, "🌡️")


def build_email_html(weather: dict, news: list[dict], quote: dict) -> str:
    """
    Builds a fully styled HTML email string.

    IMPORTANT: All CSS must be inline — most email clients strip <style> blocks.

    Args:
        weather: dict from weather.get_weather()
        news: list of dicts from news.get_top_news()
        quote: dict from quotes.get_motivational_quote()

    Returns:
        HTML string ready to pass to SES
    """
    today = datetime.now().strftime("%A, %B %d, %Y")
    weather_icon = get_weather_icon(weather["icon"])

    # Build news rows
    news_rows = ""
    for article in news:
        news_rows += f"""
        <tr>
            <td style="padding:10px 0;border-bottom:1px solid #f0f0f0;">
                <a href="{article['url']}"
                   style="color:#2563eb;text-decoration:none;font-weight:600;
                          font-size:15px;line-height:1.4;">
                    {article['title']}
                </a>
                <div style="color:#6b7280;font-size:12px;margin-top:4px;">
                    {article['source']}
                </div>
            </td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<body style="margin:0;padding:0;background-color:#f3f4f6;
             font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;">

  <div style="max-width:600px;margin:0 auto;padding:24px;">

    <!-- Header -->
    <div style="background:linear-gradient(135deg,#1e3a5f 0%,#2563eb 100%);
                border-radius:14px;padding:32px;margin-bottom:18px;color:#ffffff;">
      <div style="font-size:12px;opacity:0.75;letter-spacing:1px;
                  text-transform:uppercase;margin-bottom:6px;">
        {today}
      </div>
      <div style="font-size:28px;font-weight:700;line-height:1.2;">
        Good Morning! 👋
      </div>
      <div style="font-size:14px;opacity:0.85;margin-top:10px;">
        Here's everything you need to start your day.
      </div>
    </div>

    <!-- Weather -->
    <div style="background:#ffffff;border-radius:14px;padding:24px;
                margin-bottom:14px;border:1px solid #e5e7eb;">
      <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;
                  color:#9ca3af;margin-bottom:14px;font-weight:600;">
        🌤 Weather — {weather['city']}
      </div>
      <table style="width:100%;border-collapse:collapse;">
        <tr>
          <td style="width:70px;vertical-align:middle;">
            <span style="font-size:52px;line-height:1;">{weather_icon}</span>
          </td>
          <td style="vertical-align:middle;">
            <div style="font-size:40px;font-weight:700;color:#111827;line-height:1;">
              {weather['temp_current']}°F
            </div>
            <div style="color:#6b7280;margin-top:4px;font-size:14px;">
              {weather['description']} &nbsp;·&nbsp;
              H: {weather['temp_high']}° &nbsp; L: {weather['temp_low']}°
            </div>
            <div style="color:#9ca3af;font-size:13px;margin-top:2px;">
              Humidity: {weather['humidity']}%
            </div>
          </td>
        </tr>
      </table>
    </div>

    <!-- News -->
    <div style="background:#ffffff;border-radius:14px;padding:24px;
                margin-bottom:14px;border:1px solid #e5e7eb;">
      <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;
                  color:#9ca3af;margin-bottom:14px;font-weight:600;">
        📰 Today's Top Stories
      </div>
      <table style="width:100%;border-collapse:collapse;">
        {news_rows}
      </table>
    </div>

    <!-- Quote -->
    <div style="background:#eff6ff;border-left:4px solid #2563eb;
                border-radius:0 14px 14px 0;padding:22px;margin-bottom:14px;">
      <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.2px;
                  color:#9ca3af;margin-bottom:12px;font-weight:600;">
        ✨ Daily Motivation
      </div>
      <div style="font-size:17px;line-height:1.65;color:#1e3a5f;
                  font-style:italic;font-weight:400;">
        "{quote['quote']}"
      </div>
      <div style="margin-top:12px;color:#6b7280;font-size:14px;font-weight:500;">
        — {quote['author']}
      </div>
    </div>

    <!-- Footer -->
    <div style="text-align:center;color:#d1d5db;font-size:12px;padding-top:10px;">
      Sent with ❤️ from your Daily Emailer &nbsp;·&nbsp; Built on AWS Lambda
    </div>

  </div>
</body>
</html>"""
