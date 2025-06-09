from langchain_community.llms import LlamaCpp

def get_llama_model(model_path):
    return LlamaCpp(model_path="/content/drive/MyDrive/agentic_sop_project/models/meta-llama-3-8b.Q4_K_M.gguf", n_ctx=2048, n_gpu_layers=20)

