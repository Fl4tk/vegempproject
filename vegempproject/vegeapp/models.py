from django.db import models

class vegemodel(models.Model):
    vegename = models.CharField(verbose_name='野菜名',max_length=50)
    latestdate = models.CharField(verbose_name='最終更新日',max_length=50)
    price = models.CharField(verbose_name='価格',max_length=50)
    imgurl = models.CharField(verbose_name='画像url',max_length=50,null=True)
    weight = models.CharField(verbose_name='重さ',max_length=50,null=True)
    unit = models.CharField(verbose_name='単位',max_length=50,null=True)

    def __str__(self):
        return self.vegename