
# kioskoApp/views.py
from django.views.generic import TemplateView, View
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str
from .models import Curiosidad
import csv
from reportlab.pdfgen import canvas
from io import BytesIO
import openai
import os

# Vistas generales
class InicioView(TemplateView):
    template_name = 'historia/index.html'

class EsteProyectoView(TemplateView):
    template_name = 'historia/este_proyecto.html'

class iPadView(TemplateView):
    template_name = 'historia/iPad.html'

class MacintoshView(TemplateView):
    template_name = 'historia/macintosh.html'

class iPhoneView(TemplateView):
    template_name = 'historia/iphone.html'

class TimelineView(TemplateView):
    template_name = 'historia/timeline.html'

class SteveWozniakView(TemplateView):
    template_name = 'historia/steve_wozniak.html'

class HistoriaView(TemplateView):
    template_name = 'historia/historia.html'

class SteveJobsView(TemplateView):
    template_name = 'historia/steve_jobs.html'

class FundadoresView(TemplateView):
    template_name = 'historia/fundadores.html'

class SoftwareView(TemplateView):
    template_name = 'historia/software.html'

class ProductosView(TemplateView):
    template_name = 'historia/productos.html'

class iPodView(TemplateView):
    template_name = 'historia/ipod.html'

class LegadoView(TemplateView):
    template_name = 'historia/legado.html'

class TecnologiaInnovacionView(TemplateView):
    template_name = 'historia/tecnologia_innovacion.html'

class DiseñoView(TemplateView):
    template_name = 'historia/diseño.html'

class PublicidadView(TemplateView):
    template_name = 'historia/publicidad.html'

# Aqui empieza laVista principal de Curiosidades integreada con la inteligencia artificial de OpenAI
class CuriosidadesListView(View):
    template_name = 'historia/curiosidades.html'

    def get(self, request):
        query = request.GET.get("q")
        formato = request.GET.get("formato")
        respuesta = None

        if query:
            prompt = f"Responde con un solo párrafo como si fueras un experto sobre Apple. Contesta esta duda relacionada con Apple: {query}"

            try:
                openai.api_key = os.getenv("OPENAI_API_KEY")

                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un experto en la historia de Apple."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=300
                )

                respuesta = response.choices[0].message.content.strip()

            except Exception as e:
                respuesta = f"❌ Error al obtener respuesta de la IA: {str(e)}"

        # Exportar si se pide un formato específico y hay respuesta
        if formato and query and respuesta:
            if formato == "json":
                return JsonResponse({
                    "pregunta": query,
                    "respuesta": respuesta
                })

            elif formato == "csv":
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="curiosidad.csv"'
                writer = csv.writer(response)
                writer.writerow(['Pregunta', 'Respuesta'])
                writer.writerow([query, respuesta])
                return response

            elif formato == "pdf":
                buffer = BytesIO()
                p = canvas.Canvas(buffer)
                p.drawString(50, 800, f"Pregunta: {query}")
                y = 780
                for linea in respuesta.split('\n'):
                    p.drawString(60, y, linea[:100])
                    y -= 20
                    if y < 100:
                        p.showPage()
                        y = 800
                p.save()
                buffer.seek(0)
                return HttpResponse(buffer, content_type='application/pdf')

        # Renderizar plantilla con la respuesta
        return render(request, self.template_name, {
            "pregunta": query,
            "respuesta": respuesta
        })