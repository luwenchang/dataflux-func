# -*- coding: utf-8 -*-

import pytest

from . import BaseTestSuit, AssertDesc, gen_rand_string

SCRIPT_SET_ID = f"UnitTest_{gen_rand_string(4)}"

class TestSuitScriptSet(BaseTestSuit):
    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def test_list(self):
        # 测试接口
        code, res = self.API.get('/api/v1/script-sets/do/list')
        assert code == 200, AssertDesc.status_code(res)

    def test_add(self):
        # 数据
        data = {
            'id'         : SCRIPT_SET_ID,
            'title'      : '测试脚本集标题',
            'description': '测试脚本集描述',
        }

        # 测试接口
        body = { 'data': data }
        code, res = self.API.post('/api/v1/script-sets/do/add', body=body)

        assert code == 200,                        AssertDesc.status_code(res)
        assert res['data']['id'] == SCRIPT_SET_ID, AssertDesc.data_value_not_match()

        self.state('test_add', True)

        # 验证数据
        query = { 'id': SCRIPT_SET_ID }
        code, res = self.API.get('/api/v1/script-sets/do/list', query=query)

        assert code == 200,                                          AssertDesc.status_code(res)
        assert len(res['data']) == 1,                                AssertDesc.data_count_not_match()
        assert res['data'][0]['id']          == SCRIPT_SET_ID,       AssertDesc.data_value_not_match()
        assert res['data'][0]['title']       == data['title'],       AssertDesc.data_value_not_match()
        assert res['data'][0]['description'] == data['description'], AssertDesc.data_value_not_match()

    def test_modify(self):
        if not self.state('test_add'):
            pytest.skip(f"No test data to run this case")

        # 数据
        data = {
            'title'      : '测试脚本集标题（修改）',
            'description': '测试脚本集描述（修改）',
        }

        # 测试接口
        params = { 'id': SCRIPT_SET_ID }
        body   = { 'data': data }
        code, res = self.API.post('/api/v1/script-sets/:id/do/modify', params=params, body=body)

        assert code == 200,                        AssertDesc.status_code(res)
        assert res['data']['id'] == SCRIPT_SET_ID, AssertDesc.data_value_not_match()

        # 验证数据
        query = { 'id': SCRIPT_SET_ID }
        code, res = self.API.get('/api/v1/script-sets/do/list', query=query)

        assert code == 200,                                          AssertDesc.status_code(res)
        assert len(res['data']) == 1,                                AssertDesc.data_count_not_match()
        assert res['data'][0]['id']          == SCRIPT_SET_ID,       AssertDesc.data_value_not_match()
        assert res['data'][0]['title']       == data['title'],       AssertDesc.data_value_not_match()
        assert res['data'][0]['description'] == data['description'], AssertDesc.data_value_not_match()

    def test_delete(self):
        if not self.state('test_add'):
            pytest.skip(f"No test data to run this case")

        # 测试接口
        params = { 'id': SCRIPT_SET_ID }
        code, res = self.API.get('/api/v1/script-sets/:id/do/delete', params=params)

        assert code == 200,                        AssertDesc.status_code(res)
        assert res['data']['id'] == SCRIPT_SET_ID, AssertDesc.data_value_not_match()

        # 验证数据
        query = { 'id': SCRIPT_SET_ID }
        code, res = self.API.get('/api/v1/script-sets/do/list', query=query)

        assert code == 200,           AssertDesc.status_code(res)
        assert len(res['data']) == 0, AssertDesc.data_count_not_match()
