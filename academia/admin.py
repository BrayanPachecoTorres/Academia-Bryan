from django.contrib import admin
from .models import Category, Course, Module, Lesson, Enrollment, LessonProgress, Review, Certificate

# =========================
# Inline para Lecciones dentro de Módulos
# =========================
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ("title", "order", "video_url")
    ordering = ("order",)


# =========================
# Inline para Módulos dentro de Cursos
# =========================
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ("title", "order")
    ordering = ("order",)
    show_change_link = True


# =========================
# Categorías
# =========================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


# =========================
# Cursos
# =========================
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "price", "is_published", "created_at")
    list_filter = ("is_published", "level", "category")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


# =========================
# Módulos
# =========================
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title",)
    ordering = ("course", "order")
    inlines = [LessonInline]


# =========================
# Lecciones
# =========================
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order")
    list_filter = ("module__course",)
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("module", "order")


# =========================
# Inscripciones
# =========================
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "enrolled_at", "active")
    list_filter = ("active", "course")
    search_fields = ("user__username", "user__email", "course__title")
    date_hierarchy = "enrolled_at"
    ordering = ("-enrolled_at",)


# =========================
# Progreso de lecciones
# =========================
@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "lesson", "completed", "completed_at")
    list_filter = ("completed", "lesson__module__course")
    search_fields = ("enrollment__user__username", "lesson__title")
    date_hierarchy = "completed_at"
    ordering = ("lesson",)


# =========================
# Reseñas
# =========================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("course", "user", "rating", "created_at")
    list_filter = ("rating", "course")
    search_fields = ("user__username", "user__email", "course__title", "comment")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


# =========================
# Certificados
# =========================
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("code", "enrollment", "issued_at")
    search_fields = ("code", "enrollment__user__username", "enrollment__course__title")
    date_hierarchy = "issued_at"
    ordering = ("-issued_at",)
