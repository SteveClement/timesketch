# Copyright 2017 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for the Timesketch API client"""

import mock
import unittest

from . import client


def mock_session():

    class MockHeaders:
        def update(self, *args, **kwargs):
            return

    class MockSession:
        def __init__(self):
            self.verify = False
            self.headers = self.mock_headers()

        def get(self, *args, **kwargs):
            return mock_response(*args, **kwargs)

        def post(self, *args, **kwargs):
            return

        def mock_headers(self):
            return MockHeaders()

    return MockSession()


def mock_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data=None, text_data=None, status_code=200):
            self.json_data = json_data
            self.text = text_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    auth_text_data = u'<input id="csrf_token" name="csrf_token" value="test">'
    sketch_data = {
        u'meta': {
            u'views': [
                {
                    u'id': 1,
                    u'name': u'test'
                },
                {
                    u'id': 2,
                    u'name': u'test'
                }
            ]
        },
        u'objects': [
            {
                u'id': 1,
                u'name': u'test',
                u'description': u'test',
                u'timelines': [
                    {
                        u'id': 1,
                        u'name': u'test',
                        u'searchindex': {
                            u'index_name': u'test'
                        }
                    },
                    {
                        u'id': 2,
                        u'name': u'test',
                        u'searchindex': {
                            u'index_name': u'test'
                        }
                    }
                ]
            }
        ]}

    sketch_list_data = {
        u'objects': [sketch_data[u'objects']]
    }

    timeline_data = {
        u'objects': [
            {
                u'id': 1,
                u'name': u'test',
                u'searchindex': {
                    u'index_name': u'test'
                }
            }
        ]
    }

    url_router = {
        u'http://127.0.0.1': MockResponse(text_data=auth_text_data),
        u'http://127.0.0.1/api/v1/sketches/': MockResponse(
            json_data=sketch_list_data),
        u'http://127.0.0.1/api/v1/sketches/1': MockResponse(
            json_data=sketch_data),
        u'http://127.0.0.1/api/v1/sketches/1/timelines/1': MockResponse(
            json_data=timeline_data),

    }

    try:
        req_obj = url_router.get(args[0])
    except KeyError:
        req_obj = MockResponse(None, 404)

    return req_obj


class TimesketchApiTest(unittest.TestCase):
    """Test TimesketchApi"""

    @mock.patch(u'requests.Session', mock_session)
    def setUp(self):
        self.api_client = client.TimesketchApi(
            u'http://127.0.0.1', u'test', u'test')

    # TODO: Add test for create_sketch()

    def test_fetch_resource_data(self):
        response = self.api_client.fetch_resource_data(u'sketches/')
        self.assertIsInstance(response, dict)

    def test_get_sketch(self):
        sketch = self.api_client.get_sketch(1)
        self.assertIsInstance(sketch, client.Sketch)
        self.assertEqual(sketch.id, 1)
        self.assertEqual(sketch.name, u'test')
        self.assertEqual(sketch.description, u'test')

    def test_get_sketches(self):
        sketches = self.api_client.list_sketches()
        self.assertIsInstance(sketches, list)
        self.assertEqual(len(sketches), 1)
        self.assertIsInstance(sketches[0], client.Sketch)


class SketchTest(unittest.TestCase):

    @mock.patch(u'requests.Session', mock_session)
    def setUp(self):
        self.api_client = client.TimesketchApi(
            u'http://127.0.0.1', u'test', u'test')
        self.sketch = self.api_client.get_sketch(1)

    # TODO: Add test for upload()
    # TODO: Add test for explore()

    def test_get_views(self):
        views = self.sketch.list_views()
        self.assertIsInstance(views, list)
        self.assertEqual(len(views), 2)
        self.assertIsInstance(views[0], client.View)

    def test_get_timelines(self):
        timelines = self.sketch.list_timelines()
        self.assertIsInstance(timelines, list)
        self.assertEqual(len(timelines), 2)
        self.assertIsInstance(timelines[0], client.Timeline)


class ViewTest(unittest.TestCase):

    @mock.patch(u'requests.Session', mock_session)
    def setUp(self):
        self.api_client = client.TimesketchApi(
            u'http://127.0.0.1', u'test', u'test')
        self.sketch = self.api_client.get_sketch(1)

    def test_view(self):
        view = self.sketch.list_views()[0]
        self.assertIsInstance(view, client.View)
        self.assertEqual(view.id, 1)
        self.assertEqual(view.name, u'test')


class TimelineTest(unittest.TestCase):

    @mock.patch(u'requests.Session', mock_session)
    def setUp(self):
        self.api_client = client.TimesketchApi(
            u'http://127.0.0.1', u'test', u'test')
        self.sketch = self.api_client.get_sketch(1)

    def test_timeline(self):
        timeline = self.sketch.list_timelines()[0]
        self.assertIsInstance(timeline, client.Timeline)
        self.assertEqual(timeline.id, 1)
        self.assertEqual(timeline.name, u'test')
        self.assertEqual(timeline.index, u'test')
