from llava.conversation import conv_templates
from llava.mm_utils import process_images, tokenizer_image_token, load_image_from_base64
from llava.model.builder import load_pretrained_model

from PIL import Image
import torch

model_path = "liuhaotian/llava-v1.5-13b"

device = "cuda" if torch.cuda.is_available() else "cpu"


tokenizer, model, image_processor, context_len = load_pretrained_model(model_path, None, model_name="llava")

def generate_answer(prompt, image_paths):
    image_tensor = process_images([Image.open(img) for img in image_paths], image_processor, model.config)
    image_tensor = image_tensor.to(device, dtype=torch.float16)

    conv = conv_templates["llava_v1"].copy()
    conv.append_message(conv.roles[0], prompt)
    conv.append_message(conv.roles[1], None)

    input_ids = tokenizer_image_token(conv.get_prompt(), tokenizer, return_tensors="pt").unsqueeze(0).to(device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids=input_ids,
            images=image_tensor,
            do_sample=False,
            max_new_tokens=512,
            use_cache=True
        )

    output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output.split("### Assistant:")[1].strip()
