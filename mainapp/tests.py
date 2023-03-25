#from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, MainCategory, SubCategory, Brand, Seller, Buyer, WishList

#from mainapp.models import MainCategory, SubCategory, Brand, Product,Seller, Buyer,WishList
from django.contrib import auth
from django.contrib.messages import get_messages

class SignupViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_seller(self):
        data = {
            'name': 'John Smith',
            'username': 'john_smith',
            'email': 'john.smith@example.com',
            'mobile': '1234567890',
            'password': 'password123',
            'accountType': 'seller',
        }
        response = self.client.post(reverse('signup'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Seller.objects.filter(username='john_smith').exists())

    def test_signup_buyer(self):
        data = {
            'name': 'Jane Doe',
            'username': 'jane_doe',
            'email': 'jane.doe@example.com',
            'mobile': '0987654321',
            'password': 'password123',
            'accountType': 'buyer',
        }
        response = self.client.post(reverse('signup'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Buyer.objects.filter(username='jane_doe').exists())
class LoginPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_valid_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/')
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_invalid_login(self):
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username or password wrong")
        self.assertFalse('_auth_user_id' in self.client.session)

    def tearDown(self):
        self.user.delete()
class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.seller = Seller.objects.create(
            username='testuser', name='Test Seller',
            email='testemail@example.com', phone='1234567890'
        )
        self.buyer = Buyer.objects.create(
            username='testuser', name='Test Buyer',
            email='testemail@example.com', phone='1234567890'
        )

    def test_profile_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302) # Redirects to seller/buyer profile based on user type

    def test_profile_view_with_unauthenticated_user(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/profile/') # Redirects to login page with next parameter set to profile

    def test_seller_profile_view_with_authenticated_seller(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('sellerprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sellerprofile.html')

    def test_seller_profile_view_with_unauthenticated_user(self):
        response = self.client.get(reverse('sellerprofile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/sellerprofile/')

    def test_buyer_profile_view_with_authenticated_buyer(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('buyerprofile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'buyerprofile.html')

    def test_buyer_profile_view_with_unauthenticated_user(self):
        response = self.client.get(reverse('buyerprofile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/buyerprofile/')
class ProductDetailsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Test Product", price=10.0, description="Test Description")
        self.url = reverse('product-details', args=[self.product.pid])

    def test_product_details_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'single-product.html')
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)
        self.assertContains(response, self.product.price)

    def test_product_details_view_post(self):
        data = {'qty': 2}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cart/')
        self.assertIn('cart', self.client.session)
        cart = self.client.session['cart']
        self.assertIn(str(self.product.pid), cart)
        self.assertEqual(cart[str(self.product.pid)], 2)
class ShopPageTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.mc = MainCategory.objects.create(name="Main Category")
        self.sc = SubCategory.objects.create(name="Sub Category", mainCat=self.mc)
        self.br = Brand.objects.create(name="Brand")
        self.product = Product.objects.create(name="Product", mainCat=self.mc, subCat=self.sc, brand=self.br)

    def test_shop_page_without_filter(self):
        url = reverse('shop-page', kwargs={'mc': 'None', 'sc': 'None', 'br': 'None'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
        self.assertContains(response, 'Main Category')
        self.assertContains(response, 'Sub Category')
        self.assertContains(response, 'Brand')
        self.assertContains(response, 'Product')

    def test_shop_page_with_main_category_filter(self):
        url = reverse('shop-page', kwargs={'mc': self.mc.pk, 'sc': 'None', 'br': 'None'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
        self.assertContains(response, 'Main Category')
        self.assertContains(response, 'Sub Category')
        self.assertContains(response, 'Brand')
        self.assertContains(response, 'Product')

    def test_shop_page_with_sub_category_filter(self):
        url = reverse('shop-page', kwargs={'mc': 'None', 'sc': self.sc.pk, 'br': 'None'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
        self.assertContains(response, 'Main Category')
        self.assertContains(response, 'Sub Category')
        self.assertContains(response, 'Brand')
        self.assertContains(response, 'Product')

    def test_shop_page_with_brand_filter(self):
        url = reverse('shop-page', kwargs={'mc': 'None', 'sc': 'None', 'br': self.br.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
        self.assertContains(response, 'Main Category')
        self.assertContains(response, 'Sub Category')
        self.assertContains(response, 'Brand')
        self.assertContains(response, 'Product')

    def test_shop_page_with_multiple_filters(self):
        url = reverse('shop-page', kwargs={'mc': self.mc.pk, 'sc': self.sc.pk, 'br': 'None'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop.html')
        self.assertContains(response, 'Main Category')
        self.assertContains(response, 'Sub Category')
        self.assertContains(response, 'Brand')
        self.assertContains(response, 'Product')

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpass')
        self.mainCat = MainCategory.objects.create(name='testMainCat')
        self.subCat = SubCategory.objects.create(name='testSubCat')
        self.brand = Brand.objects.create(name='testBrand')
        self.seller = Seller.objects.create(username=self.user, name='testSeller', email='testseller@test.com', phone='1234567890')
        self.buyer = Buyer.objects.create(username=self.user, name='testBuyer', email='testbuyer@test.com', phone='1234567890', address1='testAddress1', address2='testAddress2', pin='123456', city='testCity', state='testState')
        self.product = Product.objects.create(name='testProduct', baseprice=100, discount=10, finalprice=90, mainCat=self.mainCat, subCat=self.subCat, brand=self.brand, seller=self.seller, stock=True, desc='testDescription', specification='testSpecification', color='testColor', number='testNumber', pic1='testPic1.jpg', pic2='testPic2.jpg', pic3='testPic3.jpg', pic4='testPic4.jpg', pic5='testPic5.jpg')

    def test_addProduct_view_POST(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('add-product')
        response = self.client.post(url, {
            'productname': 'testProduct2',
            'baseprice': 200,
            'discount': 20,
            'mc': self.mainCat.id,
            'sc': self.subCat.id,
            'brand': self.brand.id,
            'stock': True,
            'description': 'testDescription2',
            'specification': 'testSpecification2',
            'color': 'testColor2',
            'size': 'testSize2',
            'pic1': 'testPic1.jpg',
            'pic2': 'testPic2.jpg',
            'pic3': 'testPic3.jpg',
            'pic4': 'testPic4.jpg',
            'pic5': 'testPic5.jpg'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(pk=2).name, 'testProduct2')
    
    def test_addProduct_view_GET(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('add-product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addproduct.html')
    
    def test_editProduct_view_POST(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('edit-product', args=[self.product.pk])
        response = self.client.post(url, {
            'productname': 'testProductEdited',
            'baseprice': 200,
            'discount': 20,
            'mc': self.mainCat.id,
            'sc': self.subCat.id,
            'brand': self.brand.id,
            'stock': True,
            'description': 'testDescriptionEdited',
            'specification': 'testSpecificationEdited',
            'color': 'testColorEdited',
            'size': 'testsizeEdited',
        }
        )
        

