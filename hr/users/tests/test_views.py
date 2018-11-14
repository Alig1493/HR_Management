import pytest
import factory
from django.urls import reverse

from hr.users.config import Config, Status, ReviewType
from hr.users.models import Log
from .factories import fake, User, UserFactory


class TestRegistration:
    url = reverse("v1:users:rest_register")
    test_password = "test_pass"

    @pytest.fixture
    def register_data(self, db):
        user = UserFactory()
        email = "email@misfit.tech"

        data = {
            'email': email,
            'name': factory.Faker("name"),
            'profile_image': user.profile_image,
            'role': Config.REGULAR,
            'password1': self.test_password,
            'password2': self.test_password,
        }
        return data

    def test_user_registration_success(self, client, register_data, db):
        request = client.post(self.url, register_data)

        assert request.status_code == 201

        user = User.objects.filter(id=request.data["user"]["id"], is_active=True)

        assert user.exists()

        user = user[0]
        assert user.status == Status.OPEN
        assert not user.manager_approved
        assert user.role == Config.REGULAR
        assert user.check_password(self.test_password)

    def test_invalid_domain(self, client, register_data, db):
        register_data["email"] = "email@gmail.com"

        request = client.post(self.url, register_data)

        assert request.status_code == 400

    def test_password_mismatch(self, client, register_data, db):
        register_data["password2"] = fake.word()

        request = client.post(self.url, register_data)

        assert request.status_code == 400

    def test_unique_email(self, client, register_data, db):
        UserFactory(email=register_data["email"])

        request = client.post(self.url, register_data)

        assert request.status_code == 400

    def test_no_name(self, client, register_data, db):
        del register_data["name"]

        request = client.post(self.url, register_data)

        assert request.status_code == 400

    def test_no_image(self, client, register_data, db):
        del register_data["profile_image"]

        request = client.post(self.url, register_data)

        assert request.status_code == 400

    def test_no_role(self, client, register_data, db):
        del register_data["role"]

        request = client.post(self.url, register_data)

        assert request.status_code == 400


class TestLogin:

    url = reverse("v1:users:rest_login")
    password = "test_pass"

    def test_login(self, user, client):

        assert user.check_password(self.password)

        data = {
            "email": user.email,
            "password": self.password
        }

        request = client.post(self.url, data)

        assert request.status_code == 200
        assert request.data["user"]["email"] in user.email

    def test_wrong_email_login(self, user, client):

        data = {
            "email": fake.email(),
            "password": self.password
        }

        request = client.post(self.url, data)

        assert request.status_code == 404

    def test_wrong_password_login(self, user, client):

        data = {
            "email": user.email,
            "password": fake.word()
        }

        request = client.post(self.url, data)

        assert request.status_code == 400


class TestUpdate:

    url = reverse("v1:users:rest_user_details")

    def test_get_user_details(self, user, auth_client):

        request = auth_client.get(self.url)

        assert request.status_code == 200
        assert request.data["email"] == user.email

    def test_update_user_email(self, user, auth_client):
        email = "something.else@misfit.tech"

        data = {
            "email": email
        }

        request = auth_client.patch(self.url, data=data)

        assert request.status_code == 200
        assert request.data["email"] == email
        assert User.objects.get(id=request.data["id"]).email == email

    def test_update_invalid_user_email(self, user, auth_client):
        email = "something.else@misfit.com"

        data = {
            "email": email
        }

        request = auth_client.patch(self.url, data=data)

        assert request.status_code == 400

        user.refresh_from_db()

        assert not user.email == email


class TestLogout:

    url = reverse("v1:users:rest_logout")

    def test_logout(self, auth_client):

        request = auth_client.post(self.url)

        assert request.status_code == 200


class TestHR:

    url = reverse("v1:hr:user-requests")

    def test_non_hr_approve_view(self, user, auth_client):
        user.role = Config.REGULAR
        user.save()

        request = auth_client.get(self.url)

        assert request.status_code == 403

    def test_see_list_of_unapproved_users(self, user, auth_client):
        UserFactory(role=Config.REGULAR)

        user.role = Config.HR
        user.save()

        request = auth_client.get(self.url)

        assert request.status_code == 200

    def test_approve_user(self, user, auth_client):

        new_user = UserFactory(role=Config.REGULAR)

        assert new_user.status == Status.OPEN
        assert not new_user.manager_approved

        self.url = reverse("v1:hr:user-requests-approve", args=[new_user.id])

        data = {
            "status": Status.HR_REVIEWED
        }

        request = auth_client.get(self.url)

        assert request.status_code == 200

        request = auth_client.put(self.url, data=data)

        new_user.refresh_from_db()

        assert request.status_code == 200
        assert new_user.status == Status.HR_REVIEWED
        assert not new_user.manager_approved
        assert new_user.hr_reviewed_by == user

        log = Log.objects.filter(
            reviewed_by=user,
            reviewed_by_role=user.role,
            reviewed_on=new_user,
            reviewed_on_role=new_user.role,
            review_type=ReviewType.HR_REVIEW,
            changed_from=f"{Status.OPEN}",
            changed_to=f"{Status.HR_REVIEWED}"
        )

        assert log.exists()


class TestManager:

    url = reverse("v1:manager:user-requests")

    def test_non_hr_approve_view(self, user, auth_client):
        user.role = Config.REGULAR
        user.save()

        request = auth_client.get(self.url)

        assert request.status_code == 403

    def test_see_list_of_approved_users(self, user, auth_client):
        UserFactory(role=Config.REGULAR, status=Status.HR_REVIEWED)

        user.role = Config.MANAGER
        user.save()

        request = auth_client.get(self.url)

        assert request.status_code == 200

    def test_verify_approve_user(self, user, auth_client):
        user.role = Config.MANAGER
        user.save()

        new_user = UserFactory(role=Config.REGULAR, status=Status.HR_REVIEWED)

        assert new_user.status == Status.HR_REVIEWED
        assert not new_user.manager_approved

        self.url = reverse("v1:manager:user-requests-approve", args=[new_user.id])

        data = {
            "manager_approved": True
        }

        request = auth_client.get(self.url)

        assert request.status_code == 200

        request = auth_client.put(self.url, data=data)

        new_user.refresh_from_db()

        assert request.status_code == 200
        assert new_user.manager_approved
        assert new_user.manager_approved_by == user

        log = Log.objects.filter(
            reviewed_by=user,
            reviewed_by_role=user.role,
            reviewed_on=new_user,
            reviewed_on_role=new_user.role,
            review_type=ReviewType.MANAGER_APPROVAL,
            changed_from="False",
            changed_to="True"
        )

        assert log.exists()


class TestLogs:

    url = reverse("v1:logs:list")
    test_hr = TestHR()

    def test_get_requests_logs(self, auth_client, user):

        request = auth_client.get(self.url)

        assert request.status_code == 200
        assert not request.data["count"]

        self.test_hr.test_approve_user(user, auth_client)

        request = auth_client.get(self.url)

        assert request.status_code == 200
        assert request.data["count"] == 1
