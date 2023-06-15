from django.db import models



class Category(models.Model):
    title = models.CharField(max_length=221)


    def __str__(self):
        return self.title

    # article_set
    @property
    def articles_count(self):
        return self.articles.count()


class Tag(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    title = models.CharField(max_length=221)
    slug = models.SlugField(max_length=221, unique=True, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='articles/')
    body = models.TextField()
    tags = models.ManyToManyField(Tag)
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title





