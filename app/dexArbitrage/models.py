from django.db import models


class Pair(models.Model):
    
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    baseAsset = models.CharField(max_length=20)
    quoteAsset = models.CharField(max_length=20)
    exchange = models.CharField(max_length=20)
    network = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=30, decimal_places=18)
    priceUSD = models.DecimalField(max_digits=30, decimal_places=10,blank=True,null=True)
    liquidity = models.DecimalField(max_digits=30, decimal_places=2, default=0,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} | {self.symbol} | {self.exchange} | {self.priceUSD}"

class Deals(models.Model):
    dealPair1 = models.ForeignKey(Pair, related_name="pair_1", on_delete=models.CASCADE)
    dealPair2 = models.ForeignKey(Pair, related_name="pair_2", on_delete=models.CASCADE)
    percentChange = models.DecimalField(max_digits=30, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.dealPair1.symbol}-{self.dealPair1.exchange}|{self.dealPair2.symbol}-{self.dealPair2.exchange} | {self.percentChange}"
