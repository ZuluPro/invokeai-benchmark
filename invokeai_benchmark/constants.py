DEFAULT_ENQUEUE_PARAMS = {
  "prepend": False,
  "batch": {
    "graph": {
      "id": "text_to_image_graph",
      "nodes": {
        "main_model_loader": {
          "type": "main_model_loader",
          "id": "main_model_loader",
          "is_intermediate": True,
          "model": {
            "model_name": "stable-diffusion-v1-5",
            "base_model": "sd-1",
            "model_type": "main"
          }
        },
        "clip_skip": {
          "type": "clip_skip",
          "id": "clip_skip",
          "skipped_layers": 0,
          "is_intermediate": True
        },
        "positive_conditioning": {
          "type": "compel",
          "id": "positive_conditioning",
          "prompt": "A blue rose",
          "is_intermediate": True
        },
        "negative_conditioning": {
          "type": "compel",
          "id": "negative_conditioning",
          "prompt": "",
          "is_intermediate": True
        },
        "noise": {
          "type": "noise",
          "id": "noise",
          "seed": 0,
          "width": 512,
          "height": 512,
          "use_cpu": True,
          "is_intermediate": True
        },
        "denoise_latents": {
          "type": "denoise_latents",
          "id": "denoise_latents",
          "is_intermediate": True,
          "cfg_scale": 7.5,
          "scheduler": "euler",
          "steps": 50,
          "denoising_start": 0,
          "denoising_end": 1
        },
        "latents_to_image": {
          "type": "l2i",
          "id": "latents_to_image",
          "fp32": True,
          "is_intermediate": True
        },
        "core_metadata": {
          "id": "core_metadata",
          "type": "core_metadata",
          "generation_mode": "txt2img",
          "cfg_scale": 7.5,
          "positive_prompt": "A blue rose",
          "negative_prompt": "",
          "model": {
            "model_name": "stable-diffusion-v1-5",
            "base_model": "sd-1",
            "model_type": "main"
          },
          "steps": 50,
          "rand_device": "cpu",
          "scheduler": "euler",
          "clip_skip": 0
        },
        "linear_ui_output": {
          "id": "linear_ui_output",
          "type": "linear_ui_output",
          "is_intermediate": False,
          "use_cache": False
        }
      },
      "edges": [
        {
          "source": {
            "node_id": "main_model_loader",
            "field": "unet"
          },
          "destination": {
            "node_id": "denoise_latents",
            "field": "unet"
          }
        },
        {
          "source": {
            "node_id": "main_model_loader",
            "field": "clip"
          },
          "destination": {
            "node_id": "clip_skip",
            "field": "clip"
          }
        },
        {
          "source": {
            "node_id": "clip_skip",
            "field": "clip"
          },
          "destination": {
            "node_id": "positive_conditioning",
            "field": "clip"
          }
        },
        {
          "source": {
            "node_id": "clip_skip",
            "field": "clip"
          },
          "destination": {
            "node_id": "negative_conditioning",
            "field": "clip"
          }
        },
        {
          "source": {
            "node_id": "positive_conditioning",
            "field": "conditioning"
          },
          "destination": {
            "node_id": "denoise_latents",
            "field": "positive_conditioning"
          }
        },
        {
          "source": {
            "node_id": "negative_conditioning",
            "field": "conditioning"
          },
          "destination": {
            "node_id": "denoise_latents",
            "field": "negative_conditioning"
          }
        },
        {
          "source": {
            "node_id": "noise",
            "field": "noise"
          },
          "destination": {
            "node_id": "denoise_latents",
            "field": "noise"
          }
        },
        {
          "source": {
            "node_id": "denoise_latents",
            "field": "latents"
          },
          "destination": {
            "node_id": "latents_to_image",
            "field": "latents"
          }
        },
        {
          "source": {
            "node_id": "core_metadata",
            "field": "metadata"
          },
          "destination": {
            "node_id": "latents_to_image",
            "field": "metadata"
          }
        },
        {
          "source": {
            "node_id": "main_model_loader",
            "field": "vae"
          },
          "destination": {
            "node_id": "latents_to_image",
            "field": "vae"
          }
        },
        {
          "source": {
            "node_id": "latents_to_image",
            "field": "image"
          },
          "destination": {
            "node_id": "linear_ui_output",
            "field": "image"
          }
        }
      ]
    },
    "runs": 1,
    "data": [
      [
        {
          "node_path": "noise",
          "field_name": "seed",
          "items": [
            1112931680
          ]
        },
        {
          "node_path": "core_metadata",
          "field_name": "seed",
          "items": [
            1112931680
          ]
        }
      ]
    ]
  }
}
