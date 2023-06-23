from django.test import SimpleTestCase
from django.urls import reverse, resolve
from product.views import products, new, detail, delete, edit, add_image, delete_image, change_image

class TestUrls(SimpleTestCase):

    def test_products_url_resolves(self):
        url = reverse('product:products')
        self.assertEquals(resolve(url).func, products)

    def test_new_url_resolves(self):
        url = reverse('product:new')
        self.assertEquals(resolve(url).func, new)

    def test_detail_url_resolves(self):
        url = reverse('product:detail', args=[1])
        self.assertEquals(resolve(url).func, detail)

    def test_delete_url_resolves(self):
        url = reverse('product:delete', args=[1])
        self.assertEquals(resolve(url).func, delete)

    def test_edit_url_resolves(self):
        url = reverse('product:edit', args=[1])
        self.assertEquals(resolve(url).func, edit)

    def test_add_image_url_resolves(self):
        url = reverse('product:add_image', args=[1])
        self.assertEquals(resolve(url).func, add_image)

    def test_delete_image_url_resolves(self):
        url = reverse('product:delete_image', args=[1, 1])
        self.assertEquals(resolve(url).func, delete_image)

    def test_change_image_url_resolves(self):
        url = reverse('product:change_image', args=[1, 1])
        self.assertEquals(resolve(url).func, change_image)
