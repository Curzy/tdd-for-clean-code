import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # 웹 사이트 접속
        self.browser.get('http://localhost:8000')

        # 웹 페이지 타이틀, 헤더 'To-Do'
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # 작업 추가

        # `공작깃털 사기` 텍스트 박스에 입력

        # 엔터 입력시 페이지 갱신, 작업목록에
        # '1: 공작깃털 사기' 아이템 추가

        # 추가 아이템 입력 가능한 여분의 텍스트 박스
        # 다시 '공작깃털을 이용해서 그물 만들기' 입력

        # 페이지 갱신, 두개 아이템 보임
        # 사이트는 리스트에 대한 특정 url, url에 대한 설명 제공

        # 해당 url 접속시 작업목록 유지


if __name__ == '__main__':
    unittest.main(warnings='ignore')
