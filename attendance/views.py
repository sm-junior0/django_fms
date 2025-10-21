from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Farmer
from .forms import FarmerForm

def farmer_list(request):
    """Display all farmers"""
    farmers = Farmer.objects.all()
    return render(request, 'attendance/farmer_list.html', {'farmers': farmers})

def farmer_create(request):
    """Create a new farmer using Django forms"""
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmer added successfully!')
            return redirect('farmer_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FarmerForm()
    
    return render(request, 'attendance/farmer_form.html', {
        'form': form,
        'action': 'Create'
    })

def farmer_update(request, farmer_id):
    """Update an existing farmer using Django forms"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    if request.method == 'POST':
        form = FarmerForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmer updated successfully!')
            return redirect('farmer_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FarmerForm(instance=farmer)
    
    return render(request, 'attendance/farmer_form.html', {
        'form': form,
        'farmer': farmer,
        'action': 'Update'
    })

def farmer_delete(request, farmer_id):
    """Delete a farmer"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    if request.method == 'POST':
        farmer.delete()
        messages.success(request, 'Farmer deleted successfully!')
        return redirect('farmer_list')
    
    return render(request, 'attendance/farmer_confirm_delete.html', {'farmer': farmer})

def farmer_detail(request, farmer_id):
    """View farmer details"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    return render(request, 'attendance/farmer_detail.html', {'farmer': farmer})

def mark_attendance(request):
    """Mark attendance for farmers"""
    from django.utils import timezone
    from .models import Attendance
    
    farmers = Farmer.objects.all()
    today = timezone.now().date()
    
    # Get today's attendance records
    today_attendance = Attendance.objects.filter(date=today)
    attended_farmer_ids = list(today_attendance.values_list('farmer_id', flat=True))
    
    if request.method == 'POST':
        # Clear today's attendance first
        Attendance.objects.filter(date=today).delete()
        
        # Get selected farmer IDs from form
        selected_farmers = request.POST.getlist('farmers')
        
        # Create attendance records for selected farmers
        for farmer_id in selected_farmers:
            farmer = get_object_or_404(Farmer, id=farmer_id)
            Attendance.objects.create(
                farmer=farmer,
                date=today,
                is_present=True
            )
        
        messages.success(request, f'Attendance marked successfully for {len(selected_farmers)} farmers!')
        return redirect('mark_attendance')
    
    return render(request, 'attendance/mark_attendance.html', {
        'farmers': farmers,
        'attended_farmer_ids': attended_farmer_ids,
        'today': today
    })

def attendance_list(request):
    """Display attendance records"""
    from django.utils import timezone
    from .models import Attendance
    from django.db.models import Q
    
    # Get date filter from request
    date_filter = request.GET.get('date')
    
    if date_filter:
        try:
            from datetime import datetime
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            attendance_records = Attendance.objects.filter(date=filter_date).select_related('farmer')
        except ValueError:
            attendance_records = Attendance.objects.none()
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
    else:
        # Show last 7 days by default
        from datetime import timedelta
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        attendance_records = Attendance.objects.filter(
            date__gte=week_ago
        ).select_related('farmer').order_by('-date', 'farmer__name')
    
    # Group attendance by date
    attendance_by_date = {}
    for record in attendance_records:
        date_str = record.date.strftime('%Y-%m-%d')
        if date_str not in attendance_by_date:
            attendance_by_date[date_str] = []
        attendance_by_date[date_str].append(record)
    
    return render(request, 'attendance/attendance_list.html', {
        'attendance_by_date': attendance_by_date,
        'date_filter': date_filter,
        'total_records': attendance_records.count()
    })

def farmer_list_api(request):
 
    from django.http import JsonResponse
    
    farmers = Farmer.objects.all()
    farmers_data = []
    
    for farmer in farmers:
        farmers_data.append({
            'id': farmer.id,
            'name': farmer.name,
            'farm': farmer.farm,
            'phone': farmer.phone,
            'email': farmer.email,
            'gender': farmer.gender,
            'employment_type': farmer.employment_type,
        })
    
    return JsonResponse({
        'farmers': farmers_data,
        'total_count': len(farmers_data)
    })
