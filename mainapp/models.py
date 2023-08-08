from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Edited')
    deleted = models.BooleanField(default=False, verbose_name='Deleted')

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    preamble = models.CharField(max_length=1024, verbose_name='Preamble')
    body = models.TextField(verbose_name='Body')
    body_as_markdown = models.BooleanField(default=False, verbose_name='As markdown')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Edited')
    deleted = models.BooleanField(default=False, verbose_name='Deleted')

    def __str__(self):
        return f'#{self.pk} {self.title}'

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'news'
        verbose_name_plural = 'news'
        ordering = ('-created_at',)


class CoursesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Courses(BaseModel):
    objects = CoursesManager()

    name = models.CharField(max_length=256, verbose_name='Name')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Cost", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="Cover")

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'


class Lessons(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")
    title = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)

    def __str__(self) -> str:
        return f'#{self.course.name} | {self.num} | {self.title}'

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'
        ordering = ('course', 'num',)


class Teachers(models.Model):
    course = models.ManyToManyField(Courses)
    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")
    day_birth = models.DateField(verbose_name="Birth date")

    def __str__(self) -> str:
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second, self.name_first)

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'


class CourseFeedback(models.Model):
    RATING = ((5, "⭐⭐⭐⭐⭐"), (4, "⭐⭐⭐⭐"), (3, "⭐⭐⭐"), (2, "⭐⭐"), (1, "⭐"))
    course = models.ForeignKey(
    Courses, on_delete=models.CASCADE, verbose_name=_("Course"))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("User"))
    feedback = models.TextField(default=_("No feedback"), verbose_name=_("Feedback"))
    rating = models.SmallIntegerField(choices=RATING, default=5, verbose_name=_("Rating"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    deleted_at = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} ({self.user})"
