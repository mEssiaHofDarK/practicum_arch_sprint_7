import json
import aiohttp
from aiohttp import web
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

url = "http://localhost:12434/engines/llama.cpp/v1/chat/completions"  # url for local llm (look DRM)
model = "hf.co/cran-may/apollo2-9b-q5_k_m-gguf:latest"


class RagHandler(web.View):
    def prepare_prompt(self, context: list, question: str) -> dict:
        messages = [
            {
                "role": "system",
                "content": "You are an assistant, who thinks first and then responds. Always write down your steps. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. In answer use five sentences maximum and keep the answer concise. Speak on russian language. In your answer, indicate the sources from which you got the information.\n\ncontext:\n" + "\n".join([f'source: {doc.metadata['source']}, source_data: {doc.page_content}' for doc in context]),
            },
            {
                "role": "user",
                "content": question,
            }
        ]
        prompt = {
            'model': model,
            "messages": messages
        }
        return prompt

    async def post(self):
        data = await self.request.post()
        question = data['question']
        context = app['vector_storage'].similarity_search(question)
        print(f"{context = }")
        prepared_data = self.prepare_prompt(context=context, question=question)
        print(f"{prepared_data = }")
        async with aiohttp.ClientSession() as session, session.post(url=url, json=prepared_data) as response:
            res = await response.json()
        print(res)
        answer = res['choices'][0]['message']['content']
        payload = {"answer": answer}
        return web.Response(body=json.dumps(payload), content_type='application/json')


class TestPingHandler(web.View):
    async def get(self):
        return web.Response(text="pong")


def add_routes(app: web.Application):
    routes = [
        ('*', r'/test', TestPingHandler),
        ('*', r'/rag', RagHandler),
    ]

    for method, path, handler in routes:
        app.router.add_route(method=method, path=path, handler=handler)


if __name__ == "__main__":
    app = web.Application()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2", show_progress=True)
    vector_storage = Chroma(
        collection_name="my_d2_collection",
        embedding_function=embeddings,
        persist_directory="../task_3/chroma_langchain_my_d2_collection_db",
    )
    app['embeddings'] = embeddings
    app['vector_storage'] = vector_storage
    add_routes(app=app)
    web.run_app(app, port=8080)
