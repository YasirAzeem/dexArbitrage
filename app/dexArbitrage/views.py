from .models import Pair, Deals
import time
from datetime import datetime, timedelta
from django.shortcuts import render
import collections
from django.utils import timezone
import itertools
from .tasks import priceWork




def test_page(request):
    
    time = timezone.now() - timedelta(minutes=1)
    data = Deals.objects.filter(updated__gte=time).distinct().order_by('-percentChange')
    eth_data = []
    bsc_data = []
    cross_data = []
    strs = []
    for deal in data:
        deal_str = f"{deal.dealPair2.exchange}|{deal.dealPair1.exchange}|{deal.dealPair1.symbol}"
        if deal_str not in strs:
            strs.append(deal_str)
            if deal.dealPair1.network==deal.dealPair2.network and deal.dealPair1.network=="ethereum":
                eth_data.append(deal)
            elif deal.dealPair1.network==deal.dealPair2.network and deal.dealPair1.network=="bsc":
                bsc_data.append(deal)
            else:
                cross_data.append(deal)
    data = {'eth_data': eth_data, "bsc_data": bsc_data, "cross_data":cross_data}
    return render(request, 'index.html', {'data':data})

