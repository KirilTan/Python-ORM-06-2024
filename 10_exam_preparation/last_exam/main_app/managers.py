from django.db import models


class AuthorManager(models.Manager):
    def get_authors_by_article_count(self):
        return (
            self.annotate(num_articles=models.Count('articles'))
            .order_by('-num_articles', 'email')
        )
