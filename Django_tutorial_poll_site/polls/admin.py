from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title", {"fields": ["question_text"]}),
        ("Date information",
            {"fields": ["pub_date"], "classes": ["collapse"]}),
            # "classes": ["collapse"] で指定したfieldを表示、非表示にできる
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Question, QuestionAdmin)

# admin.site.register(Choice)
