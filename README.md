## Task 2
стянул данные почти со всех ссылок с этой страницы https://dota2.fandom.com/ru/wiki/%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F
## Task 3
### Какая модель использовалась. 

paraphrase-multilingual-mpnet-base-v2
### Какая база знаний. 

https://docs.trychroma.com/docs/overview/introduction
https://www.sbert.net/docs/quickstart.html
https://python.langchain.com/docs/tutorials/
### Сколько чанков в индексе.
364
### Сколько времени заняла генерация.
секунд 10
## Task 4
в качестве LLM модели использовал `cran-may/apollo2-9b-q5_k_m-gguf` (https://huggingface.co/Cran-May/Apollo2-9B-Q5_K_M-GGUF), запускал локально через `docker-model-plugin` (https://docs.docker.com/ai/model-runner/get-started/)

на скрине пара примеров удачного поиска и один неудачный
