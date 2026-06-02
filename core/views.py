from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from api.models import Device, Box


@login_required
def devices(request):
    devices_qs = request.user.devices.all()
    print("USER:", request.user)
    print("DEVICES:", list(devices_qs))
    return render(request, "devices.html", {"devices": devices_qs})

@login_required
def device_detail(request, device_id):
    device = Device.objects.get(device_id=device_id)
    boxes = device.boxes.all()

    return render(request, "device.html", {
        "device": device,
        "boxes": boxes
    })


@login_required
def box_detail(request, device_id, box_id):
    box = Box.objects.get(box_id=box_id)
    schedules = box.schedules.all()

    return render(request, "box.html", {
        "box": box,
        "schedules": schedules
    })