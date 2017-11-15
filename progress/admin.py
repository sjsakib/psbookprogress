from django.contrib import admin
from progress.models import Part, Chapter, Judge, Problem, UserProfile, ProblemAlias


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter', 'part')
    list_filter = ('chapter', 'part', 'judge')
    search_fields = ('name', )
    list_per_page = 50


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'uva_id', 'timus_id', 'loj_id', 'cf_id', 'get_email', )

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'email'


admin.site.register(Part)
admin.site.register(Chapter)
admin.site.register(Judge)
admin.site.register(ProblemAlias)
