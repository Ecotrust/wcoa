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
        
        test_category = models.OHICategory(
            name='Category',
            title='Test Category',
            slug='test-category',
        )
        root.add_child(instance=test_category)

        test_class = models.OHIClass(
            name='Class',
            title='Test Class',
            slug='test-class',
        )
        test_category.add_child(instance=test_class)

        cls.page = models.OHIIndicatorPage(
            name='indicator-1',
            title='Indicator 1',
            slug='indicator-1',
        )
        test_class.add_child(instance=cls.page)
        
        cls.page_two = models.OHIIndicatorPage(
            name='indicator-2',
            title='Indicator 2',
            slug='indicator-2',
        )
        test_class.add_child(instance=cls.page_two)
        
        cls.page_three = models.OHIIndicatorPage(
            name='indicator-3',
            title='Indicator 3',
            slug='indicator-3',
        )
        test_class.add_child(instance=cls.page_three)

    def test_get_page(self):
        response = self.client.get(self.page.url)
        self.assertEqual(response.status_code, 200)

    def test_get_child_classes(self):
        # Retrieve the category from the database
        category = models.Page.objects.get(slug='test-category')
        # Call the get_child_classes() method
        ohi_classes = category.specific.get_child_classes()

        # Assert that the number of classes is correct
        self.assertEqual(len(ohi_classes), 1)

        # Assert that the titles of the classes are correct
        self.assertEqual(ohi_classes[0].title, 'Test Class')

    def test_get_child_indicators(self):
        # Retrieve the class from the database
        ohi_class = models.Page.objects.get(slug='test-class')
        # Call the indicators() method
        indicators = ohi_class.specific.get_child_indicators()

        # Assert that the number of indicators is correct
        self.assertEqual(len(indicators), 3)

        # Assert that the titles of the indicators are correct
        self.assertEqual(indicators[0].title, 'Indicator 1')
        self.assertEqual(indicators[1].title, 'Indicator 2')
        self.assertEqual(indicators[2].title, 'Indicator 3')

class OHIIndicatorClassTest(WagtailPageTestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
            site_name="testserver",
        )
        
        test_category = models.OHICategory(
            name='Category',
            title='Test Category',
            slug='test-category',
        )
        root.add_child(instance=test_category)

    def test_create_class_page(self):
        test_category = models.Page.objects.get(slug='test-category')
        self.page = models.OHIClass(
            name='Class',
            title='Test Class',
            slug='test-class',
        )
        test_category.add_child(instance=self.page)

        response = self.client.get(self.page.url)
        
        self.assertEqual(response.status_code, 200)

class OHIIndicatorPageTest(WagtailPageTestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        Site.objects.create(
            hostname="testserver",
            root_page=root,
            is_default_site=True,
            site_name="testserver",
        )
        
        test_category = models.OHICategory(
            name='Category',
            title='Test Category',
            slug='test-category',
        )
        root.add_child(instance=test_category)

        test_class = models.OHIClass(
            name='Class',
            title='Test Class',
            slug='test-class',
        )
        test_category.add_child(instance=test_class)

    def test_create_indicator_page(self):
        test_class = models.Page.objects.get(slug='test-class')
        self.page = models.OHIIndicatorPage(
            name='indicator-1',
            title='Indicator 1',
            slug='indicator-1',
        )
        test_class.add_child(instance=self.page)

        response = self.client.get(self.page.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Indicator 1')
    

class WcoaModelTest(TestCase):

    def setUp(self):
        self.ohi_dash = OHIDashboard()

    def test_get_ohi_hierarchy_dict(self):
        # Create test data
        cat1 = OHICategory.objects.create(name='Category 1')
        cat2 = OHICategory.objects.create(name='Category 2')
        theme1 = OHIClass.objects.create(name='Theme 1', category=cat1)
        theme2 = OHIClass.objects.create(name='Theme 2', category=cat2)
        indicator1 = Indicator.objects.create(name='Indicator 1', theme=theme1)
        indicator2 = Indicator.objects.create(name='Indicator 2', theme=theme2)

        # Call the method being tested
        result = self.wcoa_model.get_ohi_hierarchy_dict()

        # Assert the expected output
        expected_result = {
            'name': self.wcoa_model.name,
            'dash_dict': {
                cat1.id: {
                    'name': cat1.name,
                    'img': None,  # Replace with the expected image URL for the category
                    'indicators': {
                        indicator1.id: {
                            'name': indicator1.name,
                            'img': None  # Replace with the expected image URL for the indicator
                        }
                    }
                },
                cat2.id: {
                    'name': cat2.name,
                    'img': None,  # Replace with the expected image URL for the category
                    'indicators': {
                        indicator2.id: {
                            'name': indicator2.name,
                            'img': None  # Replace with the expected image URL for the indicator
                        }
                    }
                }
            }
        }
        self.assertEqual(result, expected_result)
