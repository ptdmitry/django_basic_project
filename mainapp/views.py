from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from mainapp import models as mainapp_models


class MainPageView(TemplateView):
    template_name = 'mainapp/index.html'


class NewsPageView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_qs"] = mainapp_models.News.objects.all()[:5]
        return context

    def get(self, *args, **kwargs):
        query = self.request.GET.get('q', None)
        if query:
            return HttpResponseRedirect(f'https://google.ru/search?q={query}')
        return super().get(*args, **kwargs)


class NewsPageDetailView(TemplateView):
    template_name = "mainapp/news_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context["news_object"] = get_object_or_404(mainapp_models.News, pk=pk)
        return context


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'

    def get_context_data(self, **kwargs):
        context = super(CoursesListView, self).get_context_data(**kwargs)
        context['objects'] = mainapp_models.Courses.object.all()[:7]
        return context


class CoursesDetailView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView).get_context_data(**kwargs)
        context['course_object'] = get_object_or_404(mainapp_models.Courses, pk=pk)
        context['lessons'] = mainapp_models.Lessons.objects.filter(course=context['course_object'])
        context['teachers'] = mainapp_models.Teachers.objects.filter(course=context['course_object'])
        return context


class ContactsPageView(TemplateView):
    template_name = 'mainapp/contacts.html'


class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginPageView(TemplateView):
    template_name = 'mainapp/login.html'
