import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_layout_and_stlyling(self):
        # Edith는 메인 페이지를 방문한다
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # 그녀는 입력 상자가 가운데 배치된 것을 본다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # 그녀는 새로운 리스트를 시작하고 입력 상자가 가운데 배치된 것을 확인한다
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

    def test_can_start_a_list_and_retrieve_it_later(self):

        # 새로운 사용자 Edith 웹 사이트 접속
        self.browser.get(self.server_url)

        # 웹 페이지 타이틀, 헤더 'To-Do'
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text

        # 작업 추가
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')

        # `공작깃털 사기` 텍스트 박스에 입력
        inputbox.send_keys('공작깃털 사기')

        # 엔터 입력시 페이지 갱신, 작업목록에
        # '1: 공작깃털 사기' 아이템 추가
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 추가 아이템 입력 가능한 여분의 텍스트 박스
        # 다시 '공작깃털을 이용해서 그물 만들기' 입력
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지 갱신, 두개 아이템 보임
        # 사이트는 리스트에 대한 특정 url, url에 대한 설명 제공

        self.check_for_row_in_list_table('1: 공작깃털 사기')
        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')

        # 새로운 사용자 Francis 접속

        ## 새로운 브라우저 세션으로 에디스의 정보가
        ## 쿠키를 통해 유입되는 것을 방지한다

        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis가 홈페이지에 접속
        # Edith의 리스트는 보이지 않는다
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        # Francis가 새로운 작업 아이템을 입력하기 시작한다
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        # Francis가 전용 URL을 얻는다
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Edith가 입력한 흔적이 없는지 확인한다
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)
