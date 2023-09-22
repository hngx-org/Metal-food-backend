'''
Unit tests for the django application urls
this tests validates that the url is linked with the appropriate views

to run tests use the command "python manage.py test tests"
'''
from django.test import SimpleTestCase
from django.urls import reverse, resolve 
from transaction.views import (
  WithdrawalRequestCreateView,
  ListLunchHistory,
  RedeemLunch,
  GetALunch,
  SendLunchView,
   WithdrawalRequestCreateView,
   LunchDetailView,
   WithdrawalRequestGetView,
   ListLunchHistory,
   WithdrawalRequestListView,
   WithdrawalRequestRetrieveView,
   WithdrawalCountView,

)
from users.views import (
CreateInviteView,
CreateOrganization,
UsersListView,
TokenObtainPairView,
TokenRefreshView,
TokenVerifyView,
LoginView,
RegisterUserView,
UsersView,
OrganizationCreateAPIView,
UsersListAPIView,
UserRetrieveView,
UserSearchView,
 RegisterUserView,

)


class TestUrls(SimpleTestCase):
    def test_withdrawcreate__request_url(self):
        url=reverse('withdrawal_request')
        self.assertEquals(resolve(url).func.view_class,WithdrawalRequestCreateView)

    def test_user_list_request_url(self):
        url=reverse('users-list')
        self.assertEquals(resolve(url).func.view_class,UsersListView)

    def test_lunch_history_request_url(self):
        url=reverse('list-lunch-history')
        self.assertEquals(resolve(url).func.view_class,ListLunchHistory)

    def test_redeem_lunch_request_url(self):
        url=reverse('redem-api-view')
        self.assertEquals(resolve(url).func.view_class,RedeemLunch)

    def test_get_lunch_request_url(self):
        url=reverse('getalunch')
        self.assertEquals(resolve(url).func.view_class,GetALunch)

    def test_create_org_request_url(self):
        url=reverse('create-organization')
        self.assertEquals(resolve(url).func.view_class,CreateOrganization)

    def test_obtain_token_request_url(self):
        url=reverse('jwt_create')
        self.assertEquals(resolve(url).func.view_class,TokenObtainPairView)

    def test_token_refresh_request_url(self):
        url=reverse('refresh_view')
        self.assertEquals(resolve(url).func.view_class,TokenRefreshView)

    def test_token_verify_request_url(self):
        url=reverse('token_verify')
        self.assertEquals(resolve(url).func.view_class,TokenVerifyView)

    def test_create_invite_request_url(self):
        url=reverse('invite')
        self.assertEquals(resolve(url).func.view_class,CreateInviteView)

    def test_login_request_url(self):
        url=reverse('login')
        self.assertEquals(resolve(url).func.view_class,LoginView)

    def test_register_user_request_url(self):
        url=reverse('sign-up')
        self.assertEquals(resolve(url).func.view_class,RegisterUserView)

    def test_user_view_request_url(self):
        url=reverse('users_signup')
        self.assertEquals(resolve(url).func.view_class,UsersView)

    def test_cretae_org_request_url(self):
        url=reverse('create-organization')
        self.assertEquals(resolve(url).func.view_class,OrganizationCreateAPIView)

    def test_user_list_request_url(self):
        url=reverse('all_org_users_list')
        self.assertEquals(resolve(url).func.view_class,UsersListAPIView)

    def test_retrieve_user_request_url(self):
        url=reverse('user_detail')
        self.assertEquals(resolve(url).func.view_class,UserRetrieveView)


    def test_user_search_request_url(self):
        url=reverse('user_search')
        self.assertEquals(resolve(url).func.view_class,UserSearchView)

    def test_register_user_request_url(self):
        url=reverse('send-a-lunch')
        self.assertEquals(resolve(url).func.view_class, RegisterUserView)

    def test_send_lunch_request_url(self):
        url=reverse('invite')
        self.assertEquals(resolve(url).func.view_class,SendLunchView)

    def test_request_withdraw_url(self):
        url=reverse('withdrawal_request')
        self.assertEquals(resolve(url).func.view_class, WithdrawalRequestCreateView)

    def test_lunch_detail_request_url(self):
        url=reverse('lunch-detail')
        self.assertEquals(resolve(url).func.view_class,LunchDetailView)

    def test_lunch_list_request_url(self):
        url=reverse('list-lunch-history')
        self.assertEquals(resolve(url).func.view_class,ListLunchHistory)

    def test_get_withdraw_request_request_url(self):
        url=reverse('withdrawal_request')
        self.assertEquals(resolve(url).func.view_class,WithdrawalRequestGetView)

    def test_list_withdraw_request_url(self):
        url=reverse('withdrawal_request_get_by_user')
        self.assertEquals(resolve(url).func.view_class,WithdrawalRequestListView)

    def test_retireve_withdraw_request_url(self):
        url=reverse('withdrawal_request_detail_get_by_user')
        self.assertEquals(resolve(url).func.view_class,WithdrawalRequestRetrieveView)

    def test_count_withdrawal_request_url(self):
        url=reverse('withdrawal_count')
        self.assertEquals(resolve(url).func.view_class,WithdrawalCountView)



