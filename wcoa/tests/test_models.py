from django.test import TestCase
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase
from wcoa import models

class IndicatorCategoryTest(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        root = Page.get_first_root_node()
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
            site_name="testserver",
        )
        
        test_category = models.IndicatorCategory(
            name='Category',
            title='Test Category',
            slug='test-category',
        )
        root.add_child(instance=test_category)

        cls.page = models.IndicatorPage(
            name='indicator-1',
            title='Indicator 1',
            slug='indicator-1',
        )
        test_category.add_child(instance=cls.page)
        
        cls.page_two = models.IndicatorPage(
            name='indicator-2',
            title='Indicator 2',
            slug='indicator-2',
        )
        test_category.add_child(instance=cls.page_two)
        
        cls.page_three = models.IndicatorPage(
            name='indicator-3',
            title='Indicator 3',
            slug='indicator-3',
        )
        test_category.add_child(instance=cls.page_three)

    def test_indicators(self):
        # Retrieve the category from the database
        category = models.Page.objects.get(slug='test-category')
        # Call the indicators() method
        indicators = category.specific.indicators()

        # Assert that the number of indicators is correct
        self.assertEqual(len(indicators), 3)

        # Assert that the titles of the indicators are correct
        self.assertEqual(indicators[0].title, 'Indicator 1')
        self.assertEqual(indicators[1].title, 'Indicator 2')
        self.assertEqual(indicators[2].title, 'Indicator 3')
