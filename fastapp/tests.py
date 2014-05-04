from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from fastapp.models import Base, Apy, Executor
import json

class BaseTestCase(TransactionTestCase):
	def setUp(self):
		self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass')
		self.user1.save()
		self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass')
		self.user2.save()
		self.base1 = Base.objects.create(name="base1", user=self.user1)
		self.base1_apy1 = Apy.objects.create(name="base1_apy1", base=self.base1)
		self.base1_apy1.save()

		self.client1 = Client()  # logged in with objects
		self.client2 = Client()  # logged in without objects
		self.client3 = Client()  # not logged in 

	#def tearDown(self):
	#	try:
	#		self.base1_apy1.delete()
	#		self.base1.delete()
	#		self.user1.delete()
	#		self.user2.delete()
	#	except Exception:
	#		pass

class ApiTestCase(BaseTestCase):

	def test_base_get_403_when_not_logged_in(self):
		response = self.client3.get(reverse('base-list'))
		self.assertEqual(403, response.status_code)

	def test_base_empty_response_without_objects(self):
		self.client2.login(username='user2', password='pass')
		response = self.client2.get(reverse('base-list'))
		self.assertEqual(200, response.status_code)
		self.assertJSONEqual(response.content, [])

	def test_base_response_base_list(self):
		self.client1.login(username='user1', password='pass')
		json_data = [{
			u'id': self.base1.id,
			u'name': u'base1',
			u'uuid': self.base1.uuid
		}]
		response = self.client1.get(reverse('base-list'))
		self.assertJSONEqual(response.content, json_data)

	def test_get_all_apys_for_base(self):
		self.client1.login(username='user1', password='pass')
		#response = self.client1.get(reverse('apy-list'))
		response = self.client1.get("/fastapp/api/base/%s/apy/" % self.base1.id)
		json_data = [{u'id': 6, u'module': u'def func(self):\n    pass', u'name': u'base1_apy1'}]
		self.assertEqual(200, response.status_code)
		self.assertJSONEqual(response.content, json_data)

	def test_get_one_apy_for_base(self):
		self.client1.login(username='user1', password='pass')
		#response = self.client1.get(reverse('apy-list'))
		response = self.client1.get("/fastapp/api/base/%s/apy/%s/" % (self.base1.id, self.base1_apy1.id))
		json_data = {u'id': 7, u'module': u'def func(self):\n    pass', u'name': u'base1_apy1'}
		self.assertEqual(200, response.status_code)
		self.assertJSONEqual(response.content, json_data)

	def test_clone_apy_for_base_and_delete(self):
		self.client1.login(username='user1', password='pass')
		response = self.client1.post("/fastapp/api/base/%s/apy/%s/clone/" % (self.base1.id, self.base1_apy1.id))
		self.assertEqual(200, response.status_code)
		#json_response = {"id": 2, "name": "1_clone_1"}
		json_response = {u'id': 5, u'module': u'def func(self):\n    pass', u'name': u'4_clone_1'}
		self.assertJSONEqual(response.content, json_response)

		# delete
		response = self.client1.delete("/fastapp/api/base/%s/apy/%s/" % (self.base1.id, json_response['id']))
		self.assertEqual(204, response.status_code)

class BaseExecutorStateTestCase(BaseTestCase):

	def test_base_has_executor_instance(self):
		base = self.base1
		self.assertIs(base.executor.__class__, Executor)
		self.assertIs(base.executor.id, 1)

		# check if created second
		self.base1.save()
		self.base1.save()
		self.base1.save()
		self.assertIs(Executor.objects.count(), 1)

	def test_get_all_apys_for_base(self):
		self.client1.login(username='user1', password='pass')
		response = self.client1.get("/fastapp/api/base/%s/" % self.base1.id)
		self.assertEqual(200, response.status_code)
		self.assertJSONEqual(response.content, json.loads('{"id": 2, "name": "base1", "state": false}'))

	def test_generate_vhost_configuration(self):
		from fastapp.queue import generate_vhost_configuration
		vhost = generate_vhost_configuration('username', 'base1')
		self.assertEquals(vhost, "username-base1")

class ApyExecutionTestCase(BaseTestCase):

	def test_execute_apy_logged_in(self):
		self.client1.login(username='user1', password='pass')
		response = self.client1.get(self.base1_apy1.get_exec_url())
		self.assertEqual(200, response.status_code)
		self.assertEqual(response.content, '{"status": "OK", "exception": null, "returned": null, "id": "base1_apy1"}')

	def test_execute_apy_with_shared_key(self):
		url = self.base1_apy1.get_exec_url()+"&shared_key=%s" % (self.base1.uuid)
		response = self.client3.get(url)
		self.assertEqual(200, response.status_code)
		self.assertEqual(response.content, '{"status": "OK", "exception": null, "returned": null, "id": "base1_apy1"}')

class SettingTestCase(BaseTestCase):
	def test_create_and_change_setting_for_base(self):
		self.client1.login(username='user1', password='pass')
		json_data = {u'key': u'key', 'value': 'value'}
		response = self.client1.post("/fastapp/api/base/%s/setting/" % self.base1.id, json_data)
		self.assertEqual(201, response.status_code)
		json_data_response = {"id": 1, "key": "key", "value": "value"}
		self.assertJSONEqual(response.content, json_data_response)

		# change
		setting_id = json_data_response['id']
		response = self.client1.put("/fastapp/api/base/%s/setting/%s/" % (self.base1.id, setting_id), json.dumps(json_data), content_type="application/json")
		self.assertEqual(200, response.status_code)

		# partial update
		response = self.client1.patch("/fastapp/api/base/%s/setting/%s/" % (self.base1.id, setting_id), json.dumps(json_data), content_type="application/json")
		self.assertEqual(200, response.status_code)

		# delete
		response = self.client1.delete("/fastapp/api/base/%s/setting/%s/" % (self.base1.id, setting_id), content_type="application/json")
		self.assertEqual(204, response.status_code)

class CounterTestCase(BaseTestCase):
	def test_create_counter_on_apy_save(self):
		#counter = Counter(apy=self.base1_apy1)
		#counter.save()
		self.assertEqual(Apy.objects.get(id=self.base1_apy1.id).counter.executed, 0)
		self.base1_apy1.mark_executed()
		self.assertEqual(Apy.objects.get(id=self.base1_apy1.id).counter.executed, 1)
		self.base1_apy1.mark_failed()
		self.assertEqual(Apy.objects.get(id=self.base1_apy1.id).counter.failed, 1)