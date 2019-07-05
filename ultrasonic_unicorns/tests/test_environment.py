from unittest import TestCase


class TestAlwaysPass(TestCase):
    def test_true_is_true(self):
        self.assertTrue(True)


class TestLambda(TestCase):
    def test_lambda_handler_ohio(self):
        from lambda_local.main import call
        from lambda_local.context import Context

        #event = json.loads(open('ohio.json').read())[0]
        json_file = open('ohio.json')
        event = json_file.read()
        context = Context(timeout=5, arn_string="arn.12345", version_name="1.0")
        #context = Context(5)
        call("lambda_handler", event, context)
