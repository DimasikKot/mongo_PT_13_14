from django.shortcuts import render, redirect

from .mongo import pizzerias, cookbooks

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from django.http import HttpResponse
from io import BytesIO

from .reports import *

from reportlab.lib.pagesizes import landscape


def reports_page(request):
    result = None
    error = None
    report_type = request.GET.get("type")
    value = request.GET.get("value")

    if report_type and value:
        if not value.isdigit():
            error = "Значение должно быть числом"
        else:
            v = int(value)

            if report_type == "cheap":
                result = list(pizzerias.aggregate(cheap_pizzas_pipeline(v)))
            elif report_type == "expensive":
                result = list(pizzerias.aggregate(expensive_pizzas_pipeline(v)))
            elif report_type == "fast":
                result = list(cookbooks.aggregate(fast_recipes_pipeline(v)))
            elif report_type == "low":
                result = list(cookbooks.aggregate(low_ingredients_pipeline(v)))

    return render(request, "reports.html", {
        "result": result,
        "error": error,
        "type": report_type,
        "value": value
    })


pdfmetrics.registerFont(TTFont('TimesNewRoman', './core/fonts/times.ttf'))

def reports_pdf(request):
    report_type = request.GET.get("type")
    value = request.GET.get("value")

    if not report_type or not value or not value.isdigit():
        return HttpResponse("Неверные параметры", status=400)

    v = int(value)
    result = []
    title = ""

    if report_type == "cheap":
        result = list(pizzerias.aggregate(cheap_pizzas_pipeline(v)))
        title = f"Дешёвые пиццы (цена ≤ {v} руб.)"
    elif report_type == "expensive":
        result = list(pizzerias.aggregate(expensive_pizzas_pipeline(v)))
        title = f"Дорогие пиццы (цена ≥ {v} руб.)"
    elif report_type == "fast":
        result = list(cookbooks.aggregate(fast_recipes_pipeline(v)))
        title = f"Быстрые рецепты (время ≤ {v} мин.)"
    elif report_type == "low":
        result = list(cookbooks.aggregate(low_ingredients_pipeline(v)))
        title = f"Рецепты с малым количеством ингредиентов (≤ {v} шт.)"

    if not result:
        return HttpResponse("По заданным параметрам ничего не найдено", status=404)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=1*cm, rightMargin=1*cm,
                            topMargin=1.5*cm, bottomMargin=1*cm)

    styles = getSampleStyleSheet()

    # Стиль заголовка с русским шрифтом
    title_style = ParagraphStyle(
        name='Title',
        fontName='TimesNewRoman',
        fontSize=18,
        alignment=1,  # центр
        spaceAfter=30,
    )

    # Стиль обычного текста
    normal_style = ParagraphStyle(
        name='Normal',
        fontName='TimesNewRoman',
        fontSize=10,
    )

    elements = []
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.5*cm))

    # Заголовки таблицы
    headers = list(result[0].keys())
    data = [headers]

    # Данные
    for row in result:
        data.append([str(value) for value in row.values()])

    table = Table(data, repeatRows=1)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'TimesNewRoman'),  # ← русский шрифт для заголовков
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dddddd')),
        ('FONTNAME', (0, 1), (-1, -1), 'TimesNewRoman'),  # ← русский шрифт для ячеек
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="отчет_{report_type}_{value}.pdf"'
    response.write(pdf)
    return response