import wolframalpha
import aiohttp
import asyncio
from io import BytesIO
from config.wolfram_config import wolfram_api
import os
import hashlib
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from services.storage_serv import GraphStorage

graph_storage = GraphStorage()
WOLFRAM_APP_ID = wolfram_api.wolfram_api_key


class WolframCache:
    def __init__(self):
        self.cache_dir = "wolfram_cache"
        self.cache_ttl = timedelta(days=7)
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, query: str) -> str:
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{query_hash}.cache")

    def get(self, query: str):
        cache_path = self._get_cache_path(query)

        if not os.path.exists(cache_path):
            return None

        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)

            if datetime.now() - data['timestamp'] > self.cache_ttl:
                os.remove(cache_path)
                return None

            return data['result']
        except:
            os.remove(cache_path)
            return None

    def set(self, query: str, result):
        cache_path = self._get_cache_path(query)

        data = {
            'timestamp': datetime.now(),
            'result': result
        }

        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)

    def cleanup(self):
        now = datetime.now()
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            try:
                with open(filepath, 'rb') as f:
                    data = pickle.load(f)
                    if now - data['timestamp'] > self.cache_ttl:
                        os.remove(filepath)
            except:
                os.remove(filepath)

cache = WolframCache()


async def get_wolfram_plot(query):
    stored_path = graph_storage.get_graph_path(query)
    if stored_path and Path(stored_path).exists():
        with open(stored_path, 'rb') as f:
            return BytesIO(f.read())

    cached = cache.get(query)
    if cached:
        graph_storage.save_graph(query, cached.getvalue())
        return BytesIO(cached)

    try:
        client = wolframalpha.Client(WOLFRAM_APP_ID)
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, client.query, query)

        async with aiohttp.ClientSession() as session:
            for pod in res.pods:
                pod_title = pod.title.lower()
                if 'plot' in pod_title or 'graph' in pod_title:
                    for sub in pod.subpods:
                        if sub.img:
                            async with session.get(sub.img.src) as response:
                                if response.status == 200:
                                    image_data = await response.read()
                                    cache.set(query, image_data)
                                    graph_storage.save_graph(query, image_data)
                                    return BytesIO(image_data)

            for pod in res.pods:
                pod_title = pod.title.lower()
                if 'formula' in pod_title or 'expression' in pod_title:
                    continue

                for sub in pod.subpods:
                    if sub.img:
                        async with session.get(sub.img.src) as response:
                            if response.status == 200:
                                image_data = await response.read()
                                cache.set(query, image_data)
                                graph_storage.save_graph(query, image_data)
                                return BytesIO(image_data)

        return None

    except aiohttp.ClientError as e:
        print(f"Image download error: {e}")
    except Exception as e:
        print(f"General error: {e}")

    return None

cache.cleanup()