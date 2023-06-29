import gradio as gr
import torch
import transformers
from transformers import AutoTokenizer
from transformers import StoppingCriteria, StoppingCriteriaList

model = "Salesforce/xgen-7b-8k-inst"


class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = [50256]
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
)
header = (
    "A chat between a curious human and an artificial intelligence assistant. "
    "The assistant gives helpful, detailed, and polite answers to the human's questions.\n\n"
)

pipeline_kwargs = dict(
    max_length=200,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    stopping_criteria=StoppingCriteriaList([StopOnTokens()]),
    return_full_text=False
)

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")


    def user(user_message, history):
        return "", history + [[user_message, None]]


    def bot(history):
        prompt = ""
        for human, assistant in history:
            if assistant:
                prompt += f"### Human: {human}\n### Assistant: {assistant}\n"
        prompt += f"### Human: {history[-1][0]}\n###"
        sequences = pipeline(
            header + prompt,
            **pipeline_kwargs
        )
        response = sequences[0]["generated_text"]
        history[-1][1] = response.lstrip("Assistant: ").rstrip("<|endoftext|>")
        return history


    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()
