from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone
from django.template.loader import get_template
from django.http import HttpResponse
import weasyprint

from .models import Course, Module, Lesson, Enrollment, LessonProgress, Review, Certificate

# =========================
# Home
# =========================
class HomeView(TemplateView):
    template_name = "academia/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_courses"] = Course.objects.filter(is_published=True).order_by("-created_at")[:6]
        return context


# =========================
# Listado de cursos
# =========================
class CourseListView(ListView):
    model = Course
    template_name = "academia/listado.html"
    context_object_name = "cursos"
    paginate_by = 9

    def get_queryset(self):
        qs = Course.objects.filter(is_published=True).order_by("-created_at")
        category = self.request.GET.get("categoria")
        if category:
            qs = qs.filter(category__slug=category)
        return qs


# =========================
# Detalle de curso
# =========================
class CourseDetailView(DetailView):
    model = Course
    template_name = "academia/curso_detalle.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        context["modules"] = course.modules.prefetch_related("lessons")
        context["reviews"] = course.reviews.select_related("user")
        if self.request.user.is_authenticated:
            context["enrolled"] = Enrollment.objects.filter(user=self.request.user, course=course).exists()
        return context


# =========================
# Inscripción a curso
# =========================
@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        # Aquí podrías generar certificado futuro o enviar email de bienvenida
        pass
    return redirect("academia_curso_detalle", slug=slug)


# =========================
# Vista de lección
# =========================
@login_required
def lesson_view(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, module__course=course, slug=lesson_slug)
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        return redirect("academia_curso_detalle", slug=course_slug)

    progress, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    context = {
        "course": course,
        "lesson": lesson,
        "progress": progress,
    }
    return render(request, "academia/lesson_detalle.html", context)


# =========================
# Toggle progreso (AJAX)
# =========================
@login_required
def toggle_progress(request, pk):
    progress = get_object_or_404(LessonProgress, pk=pk, enrollment__user=request.user)
    progress.completed = not progress.completed
    progress.completed_at = timezone.now() if progress.completed else None
    progress.save()
    return JsonResponse({"completed": progress.completed})


# =========================
# Añadir reseña
# =========================
@login_required
def add_review(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        comment = request.POST.get("comment", "")
        Review.objects.update_or_create(
            course=course,
            user=request.user,
            defaults={"rating": rating, "comment": comment}
        )
    return redirect("academia_curso_detalle", slug=slug)


# =========================
# Certificado
# =========================
@login_required
def certificate_view(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    certificate = getattr(enrollment, "certificate", None)
    context = {
        "course": course,
        "certificate": certificate,
    }
    return render(request, "academia/certificate.html", context)

@login_required
def certificate_pdf(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    certificate = getattr(enrollment, "certificate", None)

    if not certificate:
        return redirect("academia_curso_detalle", slug=slug)

    # Renderizar HTML
    template = get_template("academia/certificate.html")
    html = template.render({"course": course, "certificate": certificate})

    # Generar PDF
    pdf_file = weasyprint.HTML(string=html).write_pdf()

    # Respuesta HTTP con PDF
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="certificado_{certificate.code}.pdf"'
    return response

