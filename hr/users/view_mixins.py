from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph


class PDFViewMixin:

    def get(self, request, *args, **kwargs):
        doc = SimpleDocTemplate(f"/tmp/request.pdf")
        styles = getSampleStyleSheet()
        story = [Spacer(1, 2 * inch)]
        style = styles["Normal"]
        queryset = self.get_queryset()

        if queryset:
            for item in queryset:
                bogustext = f"User name: {item.name}"
                bogustext += f"<br/>User role: {item.get_role_display()}"
                bogustext += f"<br/>User status: {item.get_status_display()}"
                p = Paragraph(bogustext, style)
                story.append(p)
                story.append(Spacer(1, 0.2 * inch))
        else:
            bogustext = "There are no user requests."
            p = Paragraph(bogustext, style)
            story.append(p)
            story.append(Spacer(1, 0.2 * inch))
        doc.build(story)

        fs = FileSystemStorage("/tmp")
        with fs.open("request.pdf") as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="request.pdf"'

        return response
