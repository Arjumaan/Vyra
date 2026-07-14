from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock
from django import forms

class StockForm(forms.ModelForm):
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Stock
        fields = ['company_name', 'stock_symbol', 'exchange', 'quantity', 'buy_price', 'current_price', 'purchase_date', 'notes']

@login_required
def stock_list(request):
    stocks = Stock.objects.filter(user=request.user)
    total_invested = sum(s.invested_amount() for s in stocks)
    total_current = sum(s.current_value() for s in stocks)
    total_pl = total_current - total_invested
    return render(request, 'stocks/stock_list.html', {
        'stocks': stocks,
        'total_invested': round(total_invested, 2),
        'total_current': round(total_current, 2),
        'total_pl': round(total_pl, 2),
    })

@login_required
def stock_create(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, 'Stock added to portfolio.')
            return redirect('stock_list')
    else:
        form = StockForm()
    return render(request, 'stocks/stock_form.html', {'form': form, 'title': 'Add Stock'})

@login_required
def stock_update(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock updated.')
            return redirect('stock_list')
    else:
        form = StockForm(instance=stock)
    return render(request, 'stocks/stock_form.html', {'form': form, 'title': 'Edit Stock'})

@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, 'Stock removed.')
    return redirect('stock_list')
