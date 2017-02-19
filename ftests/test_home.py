from .base import FunctionalTest

class BasePageLayoutTests(FunctionalTest):

    def test_base_layout_order(self):
        self.browser.get(self.live_server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(
         [element.tag_name for element in body.find_elements_by_xpath("./*")],
         ["header", "nav", "main", "footer"]
        )


    def test_name_in_header(self):
        self.browser.get(self.live_server_url + "/")
        header = self.browser.find_element_by_tag_name("header")
        self.assertIn("Sam Ireland", header.text)


    def test_nav_is_unordered_list_of_links(self):
        self.browser.get(self.live_server_url + "/")
        nav = self.browser.find_element_by_tag_name("nav")

        # The only child of the nav is a <ul>
        children = nav.find_elements_by_xpath("./*")
        self.assertEqual(len(children), 1)
        ul = children[0]
        self.assertEqual(ul.tag_name, "ul")

        # ul has list of links
        children = ul.find_elements_by_xpath("./*")
        self.assertTrue(3 <= len(children) <= 8)
        for child in children:
            self.assertEqual(child.tag_name, "li")
            self.assertEqual(len(child.find_elements_by_tag_name("a")), 1)


    def test_footer_is_unordered_list_of_img_links(self):
        self.browser.get(self.live_server_url + "/")
        footer = self.browser.find_element_by_tag_name("footer")

        # The only child of the footer is a <ul>
        children = footer.find_elements_by_xpath("./*")
        self.assertEqual(len(children), 1)
        ul = children[0]
        self.assertEqual(ul.tag_name, "ul")

        # ul has list of links
        children = ul.find_elements_by_xpath("./*")
        self.assertTrue(2 <= len(children) <= 15)
        for child in children:
            self.assertEqual(child.tag_name, "li")
            links = child.find_elements_by_tag_name("a")
            self.assertEqual(len(links), 1)
            self.assertIsNot(links[0].find_element_by_tag_name("img"), None)



class BasePageStyleTests(FunctionalTest):

    def test_body_detaches_above_1024px(self):
        # On mobile screens the body has no margins
        self.browser.get(self.live_server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        self.assertEqual(body.value_of_css_property("margin"), "0px")

        # As high as 1020px, this is still the case
        self.browser.set_window_size(1020, 800)
        self.assertEqual(body.value_of_css_property("margin"), "0px")

        # But at 1025px, the body detatches
        self.browser.set_window_size(1035, 800) # Subtract 10px for window frame
        self.assertEqual(body.value_of_css_property("width"), "1024px")
        self.assertEqual(
         body.value_of_css_property("margin-left"),
         body.value_of_css_property("margin-right")
        )
        self.assertNotEqual(body.value_of_css_property("margin-left"), "0px")
        self.assertNotEqual(body.value_of_css_property("margin-top"), "0px")
        self.assertNotEqual(body.value_of_css_property("margin-bottom"), "0px")


    def test_body_has_different_background_to_backdrop(self):
        self.browser.get(self.live_server_url + "/")
        body = self.browser.find_element_by_tag_name("body")
        backdrop = self.browser.find_element_by_tag_name("html")
        self.assertNotEqual(
         body.value_of_css_property("background-color"),
         backdrop.value_of_css_property("background-color")
        )



class HomePageTests(FunctionalTest):

    def test_home_page_has_image_and_brief_summary(self):
        self.browser.get(self.live_server_url + "/")
        main = self.browser.find_element_by_tag_name("main")

        # There are two children elements of main
        children = main.find_elements_by_xpath("./*")
        self.assertEqual(len(children), 2)

        # They are both divs, and one has an image
        self.assertEqual(children[0].tag_name, "div")
        self.assertEqual(children[0].get_property("id"), "me-image")
        self.assertIsNot(children[0].find_element_by_tag_name("img"), None)
        self.assertEqual(children[1].tag_name, "div")
        self.assertEqual(children[1].get_property("id"), "brief-summary")
