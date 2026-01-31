from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='academia_home'),

    # Listado de cursos
    path('cursos/', views.CourseListView.as_view(), name='academia_listado'),

    # Detalle de curso
    path('curso/<slug:slug>/', views.CourseDetailView.as_view(), name='academia_curso_detalle'),

    # Inscripción a curso
    path('curso/<slug:slug>/enroll/', views.enroll_course, name='academia_enroll'),

    # Vista de lección (solo inscritos)
    path('curso/<slug:course_slug>/leccion/<slug:lesson_slug>/', views.lesson_view, name='academia_leccion'),

    # Toggle progreso (AJAX)
    path('progress/<int:pk>/toggle/', views.toggle_progress, name='academia_toggle_progress'),

    # Añadir reseña
    path('curso/<slug:slug>/review/', views.add_review, name='academia_review'),

    # Certificado del curso
    path('curso/<slug:slug>/certificado/', views.certificate_view, name='academia_certificado'),
]
