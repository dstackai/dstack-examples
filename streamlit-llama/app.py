import time
import requests
import streamlit as st
import dstack

run_name = "streamlit-llama"

model_ids = [
    "TheBloke/Llama-2-13B-chat-GPTQ",
    "TheBloke/Llama-2-70B-chat-GPTQ",
    "TheBloke/Phind-CodeLlama-34B-v2-GPTQ",
]

if len(st.session_state) == 0:
    st.session_state.deploying = False
    st.session_state.deployed = False
    st.session_state.client = dstack.Client.from_config(".")
    st.session_state.run = None
    st.session_state.error = None
    st.session_state.model_id = None
    try:
        with st.spinner("Connecting to `dstack`..."):
            run = st.session_state.client.runs.get(run_name)
            if run and run.status().is_unfinished():
                st.session_state.run = run
                st.session_state.deploying = True
    except dstack.api.hub.errors.HubClientError:
        st.info("Can't connect to `dstack`", icon="💤")
        st.text("Make sure the `dstack` server is up:")
        st.code(
            """
                dstack start
            """,
            language="shell",
        )
        st.stop()


def trigger_llm_deployment():
    st.session_state.deploying = True
    st.session_state.error = None


def trigget_llm_undeployment():
    st.session_state.run.stop()
    st.session_state.deploying = False
    st.session_state.deployed = False
    st.session_state.run = None


def get_configuration(model_id: str):
    return dstack.Task(
        image="ghcr.io/huggingface/text-generation-inference:latest",
        env={"MODEL_ID": model_id},
        commands=[
            "text-generation-launcher --trust-remote-code --quantize gptq",
        ],
        ports=["8080:80"],
    )


def get_gpu_memory(model_id: str):
    if model_id == "TheBloke/Llama-2-13B-chat-GPTQ":
        return "20GB"
    elif model_id == "TheBloke/Llama-2-70B-chat-GPTQ":
        return "40GB"
    elif model_id == "TheBloke/Phind-CodeLlama-34B-v2-GPTQ":
        return "40GB"


with st.sidebar:
    st.header("Deploy an LLM")
    model_index = (
        model_ids.index(st.session_state.model_id) if st.session_state.model_id else 0
    )
    model_id = st.selectbox(
        "Choose an LLM",
        model_ids,
        index=model_index,
        disabled=st.session_state.deploying or st.session_state.deployed,
    )
    backend_options = ["No preference"]
    for backend in st.session_state.client.backends.list():
        backend_options.append(backend.name)
    st.text_input("vRAM", get_gpu_memory(model_id), disabled=True)
    backend_option = st.selectbox(
        "Choose a backend",
        backend_options,
        disabled=st.session_state.deploying or st.session_state.deployed,
        index=backend_options.index(st.session_state.run.backend)
        if st.session_state.run
        else 0,
    )
    if not st.session_state.deploying and not st.session_state.deployed:
        st.button("Deploy", on_click=trigger_llm_deployment, type="primary")


if st.session_state.error:
    with st.sidebar:
        st.error(st.session_state.error)


if st.session_state.deploying:
    with st.sidebar:
        with st.status(
            "Deploying the LLM..."
            if not st.session_state.run
            else "Attaching to the LLM...",
            expanded=True,
        ) as status:
            if not st.session_state.run:
                st.write("Provisioning...")
                try:
                    run = st.session_state.client.runs.submit(
                        configuration=get_configuration(model_id),
                        run_name=run_name,
                        resources=dstack.Resources(
                            gpu=dstack.GPU(memory=get_gpu_memory(model_id))
                        ),
                        backends=None
                        if backend_option == "No preference"
                        else [backend_option],
                    )
                    st.session_state.run = run
                    st.write("Attaching to the LLM...")
                except Exception as e:
                    if hasattr(e, "message"):
                        st.session_state.error = e.message
                    else:
                        raise e
                    st.session_state.deploying = False
                    st.experimental_rerun()
            if not st.session_state.error:
                placeholder = st.sidebar.empty()
                placeholder.button(
                    "Cancel",
                    type="primary",
                    key="cancel_starting",
                    on_click=trigget_llm_undeployment,
                )
                try:
                    st.session_state.run.attach()
                except dstack.PortUsedError:
                    pass
                while True:
                    time.sleep(0.5)
                    try:
                        r = requests.get("http://localhost:8080/info")
                        if r.status_code == 200:
                            st.session_state.model_id = r.json()["model_id"]
                            st.session_state.deployed = True
                            break
                        elif st.session_state.run.status().is_finished():
                            st.session_state.error = "Failed or interrupted"
                            break
                    except Exception as e:
                        pass
            st.session_state.deploying = False
            st.experimental_rerun()


with st.sidebar:
    if st.session_state.deployed:
        st.button(
            "Undeploy",
            type="primary",
            key="stop",
            on_click=trigget_llm_undeployment,
        )

if not st.session_state.deployed:
    st.info("The LLM is down.", icon="😴")
else:
    st.info("The LLM is up!", icon="🙌")
    st.markdown(
        "Fee to access the LLM at at [`http://127.0.0.1:8080`](http://127.0.0.1:8080/docs)"
    )
    st.code(
        """curl 127.0.0.1:8080 \\
    -X POST \\
    -d '{"inputs":"<prompt>","parameters":{"max_new_tokens":20}}' \\
    -H 'Content-Type: application/json'
            """,
        language="shell",
    )
    if model_id.startswith("TheBloke/Llama-2"):
        st.markdown(
            "Make sure to use the Llama 2 Chat prompt [format](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/discussions/3)."
        )
    elif model_id.startswith("TheBloke/Phind-CodeLlama"):
        st.markdown(
            "Make sure to use the Phind prompt [format](https://huggingface.co/TheBloke/Phind-CodeLlama-34B-v2-GPTQ#prompt-template-phind)."
        )
