from django.db import models

class Exercise(models.Model):
    title = models.CharField(max_length=100, verbose_name="Hareket Adı")
    description = models.TextField(verbose_name="Açıklama")
    # Resim yükleme alanı (Azure'a gidecek kısım burası)
    image = models.ImageField(upload_to='exercises/', verbose_name="Hareket Görseli", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title