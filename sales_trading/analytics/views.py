import csv
import weasyprint
from django.http import HttpResponse
from .models import TradeAnalytics
from django.http import HttpResponse
from django.template.loader import render_to_string

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="trade_analytics.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Total Trades', 'Total Revenue', 'Profit/Loss', 'Trading Volume'])

    for analytics in TradeAnalytics.objects.all():
        writer.writerow([analytics.date, analytics.total_trades, analytics.total_revenue, analytics.profit_loss, analytics.trading_volume])

    return response

def export_pdf(request):
    analytics = TradeAnalytics.objects.all()
    html_string = render_to_string('analytics/pdf_template.html', {'analytics': analytics})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="trade_analytics.pdf"'
    
    pdf = weasyprint.HTML(string=html_string).write_pdf()
    response.write(pdf)
    return response

def generate_report(request):
    analytics = TradeAnalytics.objects.first()  # Берем первые данные (или фильтруем по дате)
    
    # Рендерим HTML-шаблон с данными
    html_string = render_to_string("analytics/report.html", {"analytics": analytics})
    
    # Генерируем PDF из HTML
    pdf_file = weasyprint.HTML(string=html_string).write_pdf()

    # Возвращаем PDF как HTTP-ответ
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=report.pdf"
    return response