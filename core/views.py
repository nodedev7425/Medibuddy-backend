from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from api.models import Device, Box, Schedule, User


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
    box = get_object_or_404(Box, box_id=box_id)
    schedules = [
        {
            "schedule": s,
            "formatted": format_rule_string(s.rule_string)
        }
        for s in box.schedules.all()
    ]
    return render(request, "box.html", {
        "box": box,
        "schedules": schedules,
        "device_id": device_id,
        "weekdays": [
            ("MO", "Mo"), ("TU", "Di"), ("WE", "Mi"),
            ("TH", "Do"), ("FR", "Fr"), ("SA", "Sa"), ("SU", "So"),
        ],
    })

@login_required
def schedule_create(request, device_id, box_id):
    if request.method == "POST":
        box = get_object_or_404(Box, box_id=box_id)
        days = request.POST.getlist("days")
        time = request.POST.get("time")
        display_name = request.POST.get("display_name", "")

        if days and time:
            hour, minute = time.split(":")
            byday = ",".join(days)
            rule_string = f"RRULE:FREQ=WEEKLY;BYDAY={byday};BYHOUR={int(hour)};BYMINUTE={int(minute)}"
            Schedule.objects.create(
                box=box,
                display_name=display_name,
                rule_string=rule_string
            )

    return redirect("box-detail", device_id=device_id, box_id=box_id)

@login_required
def schedule_delete(request, device_id, box_id, schedule_id):
    schedule = get_object_or_404(Schedule, schedule_id=schedule_id)
    schedule.delete()
    return redirect("box-detail", device_id=device_id, box_id=box_id)

def format_rule_string(rule_string):
    days_map = {
        "MO": "Mo", "TU": "Di", "WE": "Mi",
        "TH": "Do", "FR": "Fr", "SA": "Sa", "SU": "So"
    }

    try:
        byday = ""
        byhour = ""
        byminute = "00"

        for part in rule_string.replace("RRULE:", "").split(";"):
            key, value = part.split("=")
            if key == "BYDAY":
                byday = ", ".join(days_map.get(d, d) for d in value.split(","))
            elif key == "BYHOUR":
                byhour = value.zfill(2)
            elif key == "BYMINUTE":
                byminute = value.zfill(2)

        return f"{byday} um {byhour}:{byminute} Uhr"
    except:
        return rule_string