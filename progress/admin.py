from django.contrib import admin
from progress.models import Part, Chapter, Judge, Problem, UserProfile


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter', 'part')
    list_filter = ('chapter', 'part')
    search_fields = ('name', )
    list_per_page = 50


admin.site.register(Part)
admin.site.register(Chapter)
admin.site.register(Judge)
admin.site.register(UserProfile)
