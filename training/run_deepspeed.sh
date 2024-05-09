accelerate launch --config_file "configs/deepspeed_config.yaml" train.py \
--model_name_or_path "codellama/CodeLlama-7b-Instruct-hf" \
--dataset_name "smangrul/hug_stack" \
--splits "train" \
--max_seq_len 2048 \
--max_steps 2000 \
--save_steps 500 \
--eval_steps 100 \
--logging_steps 5 \
--log_level "info" \
--logging_strategy "steps" \
--evaluation_strategy "steps" \
--save_strategy "steps" \
--push_to_hub \
--hub_private_repo True \
--hub_strategy "every_save" \
--bf16 True \
--learning_rate 2e-5 \
--lr_scheduler_type "cosine" \
--weight_decay 0.1 \
--warmup_ratio 0.1 \
--max_grad_norm 1.0 \
--output_dir "codellama-hugcoder-df" \
--per_device_train_batch_size 16 \
--per_device_eval_batch_size 16 \
--gradient_accumulation_steps 4 \
--gradient_checkpointing True \
--use_reentrant False \
--dataset_text_field "text" \
--test_size 0.1 \
--fim_rate 0.5 \
--fim_spm_rate 0.5 \
--use_flash_attn True