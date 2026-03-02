## How to run locally (macOS/linux):

Install `uv` (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

Run `uv sync` to install dependencies.

Then create a file called `secrets` -- this file name is added in `.gitignore`
so you don't accidentally commit it -- and fill it something like:
```
export OPENAI_API_KEY="sk-proj-blabla"
```

And from then on you can just run:
```
source secrets && uv run flask --app src/baramind_llama/main run --debug
```


## Demo

Open up `http://127.0.0.1:5000/chatui`.
Then chat... instructions like `Gen and run some python code involving 2 numbers`
will work, and other things will be rejected with a haiku.

This is just to demo tool calling.

Will wire up more things like persistence later.
