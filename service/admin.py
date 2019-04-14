from django.contrib import admin

from .models import Candidate, Jedi, Planet, Orden, Test, Question, Answer


admin.site.register(Candidate)
admin.site.register(Jedi)
admin.site.register(Planet)
admin.site.register(Orden)
admin.site.register(Answer)

class QuestionInstanceInline(admin.TabularInline):
    model = Question

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInstanceInline]
