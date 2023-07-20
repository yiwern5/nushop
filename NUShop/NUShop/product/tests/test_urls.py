from django.test import SimpleTestCase
from django.urls import reverse, resolve
from . import views

class TestUrls(SimpleTestCase):

    def test_products_url_resolves(self):
        url = reverse('product:products')
        self.assertEquals(resolve(url).func, views.products)

    def test_new_url_resolves(self):
        url = reverse('product:new')
        self.assertEquals(resolve(url).func, views.new)

    def test_detail_url_resolves(self):
        url = reverse('product:detail', args=[1])
        self.assertEquals(resolve(url).func, views.detail)

    def test_delete_url_resolves(self):
        url = reverse('product:delete', args=[1])
        self.assertEquals(resolve(url).func, views.delete)

    def test_edit_url_resolves(self):
        url = reverse('product:edit', args=[1])
        self.assertEquals(resolve(url).func, views.edit)

    def test_add_image_url_resolves(self):
        url = reverse('product:add_image', args=[1])
        self.assertEquals(resolve(url).func, views.add_image)

    def test_delete_image_url_resolves(self):
        url = reverse('product:delete_image', args=[1, 1])
        self.assertEquals(resolve(url).func, views.delete_image)

    def test_change_image_url_resolves(self):
        url = reverse('product:change_image', args=[1, 1])
        self.assertEquals(resolve(url).func, views.change_image)

    def test_add_variation_url_resolves(self):
        url = reverse('product:add_variation', args=[1])
        self.assertEqual(resolve(url).func, views.add_variation)
    
    def test_change_variation_url_resolves(self):
        url = reverse('product:change_variation', args=[1, 2])
        self.assertEqual(resolve(url).func, views.change_variation)
    
    def test_delete_variation_url_resolves(self):
        url = reverse('product:delete_variation', args=[1, 2])
        self.assertEqual(resolve(url).func, views.delete_variation)
    
    def test_add_subvariation_url_resolves(self):
        url = reverse('product:add_subvariation', args=[1, 2])
        self.assertEqual(resolve(url).func, views.add_subvariation)
    
    def test_change_subvariation_url_resolves(self):
        url = reverse('product:change_subvariation', args=[1, 2])
        self.assertEqual(resolve(url).func, views.change_subvariation)
    
    def test_delete_subvariation_url_resolves(self):
        url = reverse('product:delete_subvariation', args=[1, 2])
        self.assertEqual(resolve(url).func, views.delete_subvariation)
    
    def test_add_review_url_resolves(self):
        url = reverse('product:add_review', args=[1])
        self.assertEqual(resolve(url).func, views.add_review)
    
    def test_delete_review_url_resolves(self):
        url = reverse('product:delete_review', args=[1, 2])
        self.assertEqual(resolve(url).func, views.delete_review)
    
    def test_add_subvariation_duplicate_url_resolves(self):
        url = reverse('product:add_subvariation', args=[1, 2])
        self.assertEqual(resolve(url).func, views.add_subvariation)
