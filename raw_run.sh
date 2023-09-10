for size in medium
do
  LOCAL_RANK=0 CUDA_VISIBLE_DEVICES=1 python -m torch.distributed.launch --nproc_per_node 1 --use-env run_whisper.py \
	--model_name_or_path="openai/whisper-${size}" \
	--dataset_name="./RAW" \
	--dataset_config_name="vi" \
	--language="vietnamese" \
	--train_split_name="train" \
	--eval_split_name="validation" \
    --do_lower_case="True" \
	--max_steps="500" \
	--output_dir="./whisper-${size}-vi" \
	--per_device_train_batch_size="16" \
	--gradient_accumulation_steps="2" \
	--per_device_eval_batch_size="16" \
	--logging_steps="25" \
	--learning_rate="1e-5" \
	--warmup_steps="50" \
	--evaluation_strategy="steps" \
	--eval_steps="25" \
	--save_strategy="steps" \
	--save_steps="25" \
	--generation_max_length="225" \
	--preprocessing_num_workers="32" \
	--length_column_name="input_length" \
	--max_duration_in_seconds="30" \
	--text_column_name="sentence" \
	--freeze_feature_encoder="False" \
	--gradient_checkpointing \
	--group_by_length \
	--overwrite_output_dir \
	--do_train \
	--do_eval \
	--predict_with_generate \
	--use_auth_token
done
