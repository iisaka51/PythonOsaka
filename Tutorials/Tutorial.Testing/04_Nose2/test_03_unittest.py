import unittest
import requests

class DemoTest(unittest.TestCase):
    status = 200
    def setUp(self):
        self.url = 'https://www.facebook.com/iisaka51/'

    @unittest.skip('無条件にスキップ')
    def test_request1(self):
        r1 = requests.get(self.url)

    @unittest.skipIf(status > 200, 'status が 200より大きい時はスキップ')
    def test_request2(self):
        # アサーションの結果が真であれば続行し、
        # そうでなければテストをスキップします。
        r2 = requests.get(self.url)
        status2 = r2.status_code
        self.assertTrue(status2 > self.status)

    @unittest.skipUnless(status == 404, 'status が 404 でなければスキップ')
    def test_request3(self):
        # 結果が真でない限り、このテストをスキップします。
        r3 = requests.get(self.url)
        status3 = r3.status_code
        self.assertTrue(status3 > self.status)

    @unittest.expectedFailure
    def test_request4(self):
        # テストケースは "expected failed"(予想される失敗)と表示されます。
        # テストが実行された場合、テスト結果は失敗ではないと判断します。
        r4 = requests.get(self.url+'/posts%2F4331797390207884')
        status4 = r4.status_code
        self.assertTrue(status4 ==self.status)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
