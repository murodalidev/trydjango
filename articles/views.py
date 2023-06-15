from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages
from .models import Article, Category, Tag
from .forms import ArticleForm


def article_list(request):
    object_list = Article.objects.order_by('-id')
    object_list_count = object_list.count()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    q = request.GET.get('q')
    cat = request.GET.get('cat')
    tag = request.GET.get('tag')
    if cat:
        object_list = object_list.filter(category__title__exact=cat)
    if tag:
        object_list = object_list.filter(tags__title__exact=tag)
    if q:
        object_list = object_list.filter(title__icontains=q)


    paginator = Paginator(object_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    ctx = {
        'object_list': page_obj,
        'object_list_count': object_list_count,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'articles/index.html', ctx)


def article_detail(request, slug):
    if slug == "None":
        return HttpResponseForbidden('The object has no attribute "slug"')
    obj = Article.objects.get(slug=slug)

    ctx = {
        "object": obj
    }
    return render(request, 'articles/detail.html', ctx)


def article_create_view(request):
    # print(request.POST)
    ctx = {"created": False}
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        image = request.FILES.get('image')
        # print(title)
        # print(body)
        obj = Article.objects.create(title=title, body=body, image=image)
        if obj:
            # ctx['created'] = True
            messages.success(request, f'The article "{obj.title}" was successfully created')
            ctx['obj'] = obj
            return redirect(reverse('articles:detail', kwargs={"pk": obj.id}))

    return render(request, 'articles/create.html', ctx)


def article_create_form_view(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'The article "{obj.title}" was successfully created')
            return redirect(reverse("articles:detail", kwargs={"pk": obj.id}))
    ctx = {
        "form": form
    }
    return render(request, 'articles/create_form.html', ctx)


def _article_create_form_view(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save()
        messages.success(request, f'The article "{obj.title}" was successfully created')
        return redirect(reverse("articles:detail", kwargs={"pk": obj.id}))
    ctx = {
        "form": form
    }
    return render(request, 'articles/create_form.html', ctx)


def article_edit_form(request, pk):
    try:
        obj = Article.objects.get(id=pk)
    except Article.DoesNotExist:
        raise Http404

    form = ArticleForm(instance=obj)

    if request.method == "POST":
        form = ArticleForm(data=request.POST, instance=obj, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'The article "{obj.title}" was successfully changed')
            return redirect(reverse("articles:detail", kwargs={"pk": pk}))

    ctx = {
        "form": form,
        "obj": obj,
    }

    return render(request, 'articles/edit.html', ctx)


def article_delete_view(request, pk):
    obj = get_object_or_404(Article, id=pk)
    if request.method == "POST":
        obj.delete()
        messages.error(request, f'The article "{obj.title}" was successfully deleted')
        return redirect('articles:list')
    ctx = {
        "object": obj
    }
    return render(request, 'articles/delete.html', ctx)
