import os
import torch
from unittest.mock import patch
from transformers import AutoProcessor, AutoModelForCausalLM
from transformers import dynamic_module_utils

class Florence2VLM:
    # def __init__(self, model_id: str = "microsoft/Florence-2-large"):
    #     """
    #     画像処理モデルをロードします。
    #     """
    #     self.device = "cuda"
    #     self.torch_dtype = torch.float16
    #     self.model = AutoModelForCausalLM.from_pretrained(
    #         model_id,
    #         trust_remote_code=True
    #     ).to(self.device).to(self.torch_dtype)

    #     self.processor = AutoProcessor.from_pretrained(
    #         model_id,
    #         trust_remote_code=True
    #     )

    def __init__(self, model_id: str = "microsoft/Florence-2-large"):
        """
        画像処理モデルをロードします。
        """
        self.device = "cuda"
        self.torch_dtype = torch.float16

        # =========================================================================
        # 【Windows向け修正】 flash_attn のチェックを回避するパッチ (修正版)
        # =========================================================================
        
        # 1. オリジナルの関数を退避
        original_get_imports = dynamic_module_utils.get_imports

        # 2. 偽装用関数を定義
        def get_imports_proxy(filename: str | os.PathLike) -> list[str]:
            # 退避しておいたオリジナルの関数を使う
            imports = original_get_imports(filename)
            
            # "flash_attn" があったら消す
            if "flash_attn" in imports:
                imports.remove("flash_attn")
            return imports

        # 3. パッチを適用してモデルロード
        with patch("transformers.dynamic_module_utils.get_imports", side_effect=get_imports_proxy):
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                trust_remote_code=True
            ).to(self.device).to(self.torch_dtype)
        # =========================================================================

        self.processor = AutoProcessor.from_pretrained(
            model_id,
            trust_remote_code=True,
            clean_up_tokenization_spaces=True
        )
    
    def process(self, image, task_prompt: str = "<CAPTION>"):
        """
        画像とプロンプトを受け取り、推論を実行します。
        """
        inputs = self.processor(
            text=task_prompt,
            images=image,
            return_tensors="pt"
        )

        inputs["input_ids"] = inputs["input_ids"].to(self.device)
        inputs["pixel_values"] = inputs["pixel_values"].to(self.device, self.torch_dtype)

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            do_sample=False,
            num_beams=3,
        )

        generated_text = self.processor.batch_decode(
            generated_ids, 
            skip_special_tokens=False
        )[0]

        parsed_answer = self.processor.post_process_generation(
            generated_text,
            task=task_prompt,
            image_size=(image.width, image.height)
        )

        return parsed_answer