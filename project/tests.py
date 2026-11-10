from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from .middleware import RequestIPMiddleware, RequestTrackingNumberMiddleware, RequestTrackingReqMiddleware
from .models import Parcel


class ParcelPageTests(TestCase):
    def setUp(self):
        self.parcel = Parcel.objects.create(
            name="Books",
            description="A parcel of books",
            weight="2.50",
            tracking_number="TRACK123456",
        )

    def test_home_and_parcel_list_render(self):
        self.assertEqual(self.client.get("/").status_code, 200)

        response = self.client.get("/parcels/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.parcel.tracking_number)

    def test_parcel_detail_renders_and_missing_parcel_is_not_found(self):
        response = self.client.get(f"/parcels/{self.parcel.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.parcel.description)
        self.assertEqual(self.client.get("/parcels/99999/").status_code, 404)


class MiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_blocked_ip_gets_forbidden_page(self):
        middleware = RequestIPMiddleware(lambda request: HttpResponse())
        request = self.factory.get("/")
        request.META["REMOTE_ADDR"] = "192.168.1.100"

        response = middleware(request)

        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Access denied", status_code=403)

    def test_tracking_number_validation_returns_bad_request(self):
        middleware = RequestTrackingNumberMiddleware(lambda request: HttpResponse())

        response = middleware(self.factory.get("/parcels/", {"tracking_number": "short"}))

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Invalid tracking number", status_code=400)

    def test_rate_limit_is_per_client_ip(self):
        middleware = RequestTrackingReqMiddleware(lambda request: HttpResponse())
        first_client = self.factory.get("/")
        first_client.META["REMOTE_ADDR"] = "192.0.2.1"

        for _ in range(10):
            self.assertEqual(middleware(first_client).status_code, 200)
        self.assertEqual(middleware(first_client).status_code, 429)

        second_client = self.factory.get("/")
        second_client.META["REMOTE_ADDR"] = "192.0.2.2"
        self.assertEqual(middleware(second_client).status_code, 200)
