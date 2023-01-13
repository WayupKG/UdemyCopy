from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, FileExtensionValidator

from apps.course.managers import ActiveManager

User = get_user_model()


class Category(models.Model):
    """Категория курсов"""
    title = models.CharField(verbose_name="Название", max_length=255)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    is_publish = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        db_table = 'course_category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return str(self.title)


class Course(models.Model):
    """Курсы"""
    LEVEL = (
        ('start', 'начальный'),
        ('medium', 'средний'),
        ('pro', 'профессиональный'),
        ('all', 'все уровни'),
    )

    user = models.ForeignKey(to=User, verbose_name="Автор", on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category, verbose_name="категория", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Название", max_length=60)
    sub_title = models.CharField(verbose_name="__", max_length=60)
    description = models.TextField(verbose_name="Описание", validators=[MinLengthValidator(limit_value="200")])
    lang = models.CharField(verbose_name="Язык курса", max_length=50)
    level = models.CharField(verbose_name="Уровень", max_length=20, choices=LEVEL)
    sub_category = models.CharField(verbose_name="__", max_length=10)
    image = models.ImageField(verbose_name="Изображение", upload_to='image/')
    ad_video = models.FileField(verbose_name="Видео файл", upload_to='video/', blank=True, null=True,
                                validators=[FileExtensionValidator(['mp4'])])

    is_publish = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        db_table = 'course'
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self) -> str:
        return str(self.title)


class CoursePrice(models.Model):
    """Цена курса"""
    course = models.OneToOneField(to=Course, verbose_name="Курс", on_delete=models.CASCADE, related_name='price')
    currency = models.CharField(verbose_name="Валюта", max_length=5)
    amount = models.DecimalField(verbose_name="Сумма", max_digits=6, decimal_places=2)

    class Meta:
        db_table = 'course_price'
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'

    def __str__(self) -> str:
        return f"{self.amount} - {self.currency}"


class CoursePart(models.Model):
    """Содержание курса"""
    course = models.ForeignKey(to=Course, verbose_name="Курс", on_delete=models.CASCADE, related_name='parts')
    title = models.CharField(verbose_name="Название", max_length=60)
    description = models.TextField(verbose_name="Описание", validators=[MinLengthValidator(limit_value="100")])

    class Meta:
        db_table = 'course_part'
        verbose_name = 'Содержание курса'
        verbose_name_plural = 'Содержании курсов'

    def __str__(self) -> str:
        return str(self.title)


class CoursePartFile(models.Model):
    """Файлы для содержание курса"""
    course_part = models.ForeignKey(to=CoursePart, verbose_name="Cодержание курса",
                                    on_delete=models.CASCADE, related_name='files')
    file = models.FileField(verbose_name="Файл", upload_to='',
                            validators=[FileExtensionValidator(['mp4', 'pdf', 'docx'])])

    class Meta:
        db_table = 'course_part_file'
        verbose_name = 'Файлы для содержание курса'
        verbose_name_plural = 'Файлы для содержании курсов'

    def __str__(self) -> str:
        return f"{self.course_part} - {self.file.name}"
