from collections import defaultdict, deque
from datetime import datetime, timedelta

from django.shortcuts import render


class UserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("---------USERS INFO---------")
        print("BROWSER INFO:")
        print(f"Ip Address: {request.META.get('REMOTE_ADDR', 'Unknown')}")
        print(f"Browser Name: {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
        print(f"Request Method: {request.method}")

        response = self.get_response(request)

        return response

class RequestInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("---------NEW REQUEST---------")
        print(f"URL: {request.build_absolute_uri()}")
        print(f"Method: {request.method}")
        print(f"Request Time: {datetime.now()}")

        response = self.get_response(request)
        print(f"Status Code: {response.status_code}")
        return response

class RequestIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        blocked_ips = ['192.168.1.100', '10.0.0.1']

        if ip in blocked_ips:
            return render(request, "blocked.html", status=403)

        response = self.get_response(request)
        return response

class RequestTrackingNumberMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        print(f"Request Path: {path}")
        track_number = request.GET.get('tracking_number')
        if track_number:
            if 10 < len(track_number) < 15:
                print(f"Tracking Number: {track_number}")
            else:
                return render(request, "invalid_tracking_number.html", status=400)
        return self.get_response(request)


class RequestTrackingReqMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.time_dict = {}

    def __call__(self, request):
        now = datetime.now()
        expired_keys = [key for key in self.time_dict if key < (now - timedelta(minutes=1))]
        for key in expired_keys:
            self.time_dict.pop(key)
        if len(self.time_dict) >= 10:
            return render(request, "too_many_requests.html", status=429)
        self.time_dict[now] = request.path
        return self.get_response(request)