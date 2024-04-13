from django.contrib import admin

from .models import User, Veiculo, Pedido


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')

@admin.register(Pedido)
class ListAdmin(admin.ModelAdmin):
    list_display = ('user', 'data_inicio', 'data_fim', 'local',
                    'kilometro_inicial','kilometro_final', 'combustivel_inicial','combustivel_fim' )
@admin.register(Veiculo)
class ListAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'marca', 'tipo_combustivel', 'description', 'image')