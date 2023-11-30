import time
from datetime import datetime
from urllib.parse import urljoin
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from invokeai_benchmark import constants


class Client:
    def __init__(self, api_url, verbose=2):
        self.url = api_url
        self.session = requests.Session()
        retry = Retry(
            status=0,
            connect=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.hooks['response'].append(lambda r, *args, **kwargs: r.raise_for_status())
        self.verbose = verbose

    def invoke(
        self,
        prompt,
        negative_prompt='',
        width=512,
        height=512,
        seed=0,
        cfg_scale=7.5,
        scheduler='euler',
        steps=50,
        fp32=True,

        queue_id='default',
    ):
        path = f'queue/{queue_id}/enqueue_batch'
        url = urljoin(self.url, path)

        params = constants.DEFAULT_ENQUEUE_PARAMS.copy()
        params['batch']['graph']['nodes']['positive_conditioning']['prompt'] = prompt
        params['batch']['graph']['nodes']['negative_conditioning']['prompt'] = negative_prompt
        params['batch']['graph']['nodes']['noise'].update({
            'width': width,
            'height': height,
            'seed': seed,
        })
        params['batch']['graph']['nodes']['denoise_latents'].update({
            'cfg_scale': cfg_scale,
            'scheduler': scheduler,
            'steps': steps,
        })
        params['batch']['graph']['nodes']['latents_to_image']['fp32'] = fp32
        params['batch']['graph']['nodes']['core_metadata'].update({
            'prompt': prompt,
            'width': width,
            'height': height,
            'seed': seed,
            'cfg_scale': cfg_scale,
            'scheduler': scheduler,
            'steps': steps,
            'fp32': fp32,
        })

        response = self.session.post(url, json=params)
        return response.json()

    def _get_batch_status(self, batch_id, queue_id='default'):
        path = f'queue/{queue_id}/b/{batch_id}/status'
        url = urljoin(self.url, path)
        response = self.session.get(url)
        return response.json()

    def _get_item_status(self, item_id, queue_id='default'):
        path = f'queue/{queue_id}/i/{item_id}'
        url = urljoin(self.url, path)
        response = self.session.get(url)
        return response.json()

    def _get_queue_status(self, queue_id='default'):
        path = f'queue/{queue_id}/status'
        url = urljoin(self.url, path)
        response = self.session.get(url)
        return response.json()

    def _get_queue_items(self, queue_id='default'):
        path = f'queue/{queue_id}/list'
        url = urljoin(self.url, path)
        params = {'limit': 1000}
        response = self.session.get(url, params=params)
        return response.json()

    def _get_session(self, session_id):
        path = f'sessions/{session_id}'
        url = urljoin(self.url, path)
        response = self.session.get(url)
        return response.json()

    def clear_cache(self):
        url = urljoin(self.url, 'app/invocation_cache')
        response = self.session.delete(url)
        return response

    def get_version(self):
        url = urljoin(self.url, 'app/version')
        response = self.session.get(url)
        return response.json()['version']

    def list_images(self):
        url = urljoin(self.url, 'images/')
        params = {'limit': 1000}
        response = self.session.get(url, params=params)
        return response.json()

    def delete_image(self, image_name):
        path = f"images/i/{image_name}"
        url = urljoin(self.url, path)
        response = self.session.delete(url)
        return response

    def clean_images(self):
        for img in self.list_images()['items']:
            self.delete_image(img['image_name'])

    def full_invoke(self, **kwargs):
        invoke_resp = self.invoke(**kwargs)
        batch_id = invoke_resp['batch']['batch_id']

        completed = False
        item_id = None
        while not completed:
            if item_id is None:
                last_queue_status = self._get_queue_status()
                item_id = last_queue_status['queue']['item_id']
            completed = self._get_batch_status(batch_id)['completed']
            time.sleep(1)

        for item in self._get_queue_items()['items']:
            if item['item_id'] == item_id:
                session_id = item['session_id']
                break
        else:
            raise Exception("Cannot find session ID")

        session = self._get_session(session_id)

        image_name = list(session['execution_graph']['nodes'].values())[-1]['image']['image_name']
        image_path = f'images/i/{image_name}/full'
        image_url = urljoin(self.url, image_path)

        result = {
            'batch_id': batch_id,
            'item_id': item_id,
            'session_id': session_id,
            'image_path': image_url,
            'prompt': kwargs['prompt'],
            'width': kwargs['width'],
            'height': kwargs['height'],
            'seed': kwargs['seed'],
            'cfg_scale': kwargs['cfg_scale'],
            'scheduler': kwargs['scheduler'],
            'steps': kwargs['steps'],
            'fp32': kwargs['fp32'],
        }
        item = self._get_item_status(item_id)
        result.update({
            'priority': item['priority'],
            'error': item['error'],
            'created_at': item['created_at'],
            'started_at': item['started_at'],
            'completed_at': item['completed_at'],
        })

        created_at = datetime.strptime(result['created_at'], '%Y-%m-%d %H:%M:%S.%f')
        started_at = datetime.strptime(result['started_at'], '%Y-%m-%d %H:%M:%S.%f')
        completed_at = datetime.strptime(result['completed_at'], '%Y-%m-%d %H:%M:%S.%f')
        queue_elapsed = (started_at - created_at).total_seconds()
        task_elapsed = (completed_at - started_at).total_seconds()
        total_elapsed = (completed_at - created_at).total_seconds()
        pixel_rate = round(kwargs['width'] * kwargs['height'] / task_elapsed, 3)
        result.update({
            'queue_elapsed': queue_elapsed,
            'task_elapsed': task_elapsed,
            'total_elapsed': total_elapsed,
            'pixel_rate': pixel_rate,
        })
        return result
