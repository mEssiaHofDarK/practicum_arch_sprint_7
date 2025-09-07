import json
from aiohttp import web
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain import hub


class RagHandler(web.View):
    async def post(self):
        data = await self.request.post()
        prompt_invoke_data = {
            "question": data['question']
        }
        prompt_invoke_data["context"] = app['vector_storage'].search(prompt_invoke_data['question'], search_type='similarity')
        message = app['prompt'].invoke(prompt_invoke_data)
        print(message)
        resp = ...  # response from llm
        payload = {"answer": "hui"}
        return web.Response(body=json.dumps(payload), content_type='application/json')


class TestPingHandler(web.View):
    async def get(self):
        return web.Response(text="i'm fucking pong")


def add_routes(app: web.Application):
    routes = [
        ('*', r'/test', TestPingHandler),
        ('*', r'/rag', RagHandler),
    ]

    for method, path, handler in routes:
        app.router.add_route(method=method, path=path, handler=handler)


if __name__ == "__main__":
    # add connect to llm
    app = web.Application()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", show_progress=True)
    vector_storage = Chroma(
        collection_name="my_d2_collection",
        embedding_function=embeddings,
        persist_directory="../task_3/chroma_langchain_my_d2_collection_db",
    )
    app['prompt'] = hub.pull("rlm/rag-prompt")
    app['embeddings'] = embeddings
    app['vector_storage'] = vector_storage
    add_routes(app=app)
    web.run_app(app, port=8080)
