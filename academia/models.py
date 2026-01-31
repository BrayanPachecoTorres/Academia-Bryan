from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

# =========================
# Categorías de cursos
# =========================
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# =========================
# Cursos
# =========================
class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    cover_image = models.ImageField(upload_to="courses/covers/", null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    duration_minutes = models.PositiveIntegerField(default=0)
    level = models.CharField(
        max_length=50,
        choices=[("beginner", "Principiante"), ("intermediate", "Intermedio"), ("advanced", "Avanzado")],
        default="beginner"
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.reviews.all().values_list("rating", flat=True)
        return sum(ratings) / len(ratings) if ratings else 0


# =========================
# Módulos dentro de un curso
# =========================
class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# =========================
# Lecciones
# =========================
class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Lección"
        verbose_name_plural = "Lecciones"
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.module.course.title} - {self.title}"


# =========================
# Inscripciones
# =========================
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user} en {self.course}"


# =========================
# Progreso de lecciones
# =========================
class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, related_name="progress", on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Progreso de lección"
        verbose_name_plural = "Progresos de lecciones"
        unique_together = ("enrollment", "lesson")

    def __str__(self):
        return f"{self.enrollment.user} - {self.lesson.title} ({'✔' if self.completed else '✘'})"


# =========================
# Reseñas de cursos
# =========================
class Review(models.Model):
    course = models.ForeignKey(Course, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        unique_together = ("course", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} reseña {self.course.title} ({self.rating}/5)"


# =========================
# Certificados
# =========================
class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name="certificate")
    issued_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"

    def __str__(self):
        return f"Certificado {self.code} - {self.enrollment.user}"
