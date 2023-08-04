from django.core.management import BaseCommand

from mainapp.models import News


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('Привет терминал')

        # В таком способе для каждой новости отдельное подключение к БД

        for i in range(10):
            News.objects.create(
                title=f'title#{i}',
                preamble=f'preamble#{i}',
                body=f'body#{i}'
            )

        # Можно создать пакетом в оперативке и потом одним пакетом в БД отправить

        news_list = []
        for i in range(5):
            news_list.append(News(
                title=f'title#{i}',
                preamble=f'preamble#{i}',
                body=f'body#{i}'
            ))
        News.objects.bulk_create(news_list)
