from typing import TypedDict

from openai import OpenAI
import json

from baramind_llama import system_prompt as sp

class LocalTools:
    """This "class" is just being used as a logical grouping for tool functions."""
    def gen_code(self, x, y):
        return f"(({x} * {x}) + ({y} * {y})) ** (1 / 2)"

client = OpenAI()

tools = [{
    "type": "function",
    "name": "gen_code",
    "description": "Generate some python code involving 2 numbers.",
    "parameters": {
        "type": "object",
        "properties": {
            "x": {"type": "number"},
            "y": {"type": "number"}
        },
        "required": ["x", "y"],
        "additionalProperties": False
    },
    "strict": True
}]

DEFAULT_SAMPLE_SINGLE_CHAT_INPUT = [{"role": "user", "content": "I have to save 1k a year, with an income of 12k a year. My needs are about 5k a year. Tell me how to do this, make up some examples if need be."}]
class ChatInput(TypedDict):
    role: str
    content: str

def sample_tool_calling_chat(
        model: str="o4-mini",
        chat_input: list[ChatInput] | None = None
) -> str:
    """Read the docs at https://platform.openai.com/docs/guides/function-calling to make sense of this.

    But, tl;dr...

    Basically we send the model structured data and receive structured data.
    When we send it some text that looks like it needs a tool invocation,
    it "responds" with (i.e. completes that "text") by responding with
    information about a tool call.

    When we actually run the tool, we have to send the whole original input
    plus the tool call information, plus our own "completion" which is the
    tool call RESULT, and then the model will "respond" -- complete the text --
    by inserting the appropriate real expected response.

    Then finally, in this conversation we also make OpenAI do the same
    thing on its own server side, where internally it -- presumably --
    does a similar dance, invokes its own code interpreter, and generates
    the final complete text, which we can then display like a nice conversation.
    """
    if chat_input is None:
        chat_input = DEFAULT_SAMPLE_SINGLE_CHAT_INPUT

    # instructions is like the "system prompt" or base context or something.
    instructions = sp.system_prompt_txt

    response = client.responses.create(
        model=model,
        input=chat_input,
        # tools=tools,  # TODO: add this back in when needed .. see `final_response` below as well
        instructions=instructions,
    )
    if len(response.output) == 1 and response.output[0].type == "message":
        return response.output_text
    outputs = {}
    tool_call_was_requested = False
    for x in response.output:
        outputs[x.type] = x
        if x.type == "function_call":
            args = json.loads(x.arguments)
            tool_name = x.name
            tool_instance = getattr(LocalTools(), tool_name)
            tool_call_result = tool_instance(args["x"], args["y"])
            outputs["function_call_output"] = {
                "type": "function_call_output",
                "call_id": x.call_id,
                "output": str(tool_call_result)
            }
            tool_call_was_requested = True
    if not tool_call_was_requested:
        return response.output_text
    chat_input.extend(outputs.values())
    final_response = client.responses.create(
        model=model,
        input=chat_input,
        # tools=tools,  # TODO: add this back in when needed.
        include=["code_interpreter_call.outputs"],  # I added this to look for something but need to dig deeper
        instructions=instructions,
    )
    assert final_response.output_text, "Empty output text after second api call."
    # TODO: fix the above possibility .. i think it can basically sometimes just send through a "reasoning" output that needs to be fed back in again... Or it's a bug, or a stop token issue, or just needs more prompt engineering.
    return final_response.output_text.removeprefix("```html").removesuffix("```")
