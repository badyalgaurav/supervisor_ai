import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, LineByLineTextDataset, DataCollatorForLanguageModeling, TrainingArguments, Trainer


def pre_train_model():
    # Load pre-trained model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2', padding=True)
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    return tokenizer, model


def train_custom_model():
    # #pretrained dataset
    # tokenizer, model = pre_train_model()
    # # Fine-tune the model on conversational data
    # # TODO: load and preprocess conversational data, and fine-tune the model
    # data_path="logic/custom_data.txt"
    # dataset = LineByLineTextDataset(tokenizer=tokenizer, file_path=data_path, block_size=128)
    # # Set up the data collator
    # data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    #
    # # Set up the training arguments
    # training_args = TrainingArguments(
    #     output_dir='./results',
    #     overwrite_output_dir=True,
    #     num_train_epochs=3,
    #     per_device_train_batch_size=16,
    #     save_steps=1000,
    #     save_total_limit=2,
    #     prediction_loss_only=True,
    # )
    # # Fine-tune the model on your custom data
    # trainer = Trainer(
    #     model=model,
    #     args=training_args,
    #     train_dataset=dataset,
    #     data_collator=data_collator,
    # )
    # # tokenizer.add_special_tokens({'pad_token': ' '})
    # trainer.train()
    #
    # # Save the fine-tuned model
    # model_path = 'logic/custom_data'
    # token_path = 'logic/token_path'
    # model.save_pretrained(model_path)
    # tokenizer.save_pretrained(token_path)

    # Step 1: Load the tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained('microsoft/DialoGPT-medium')
    model = GPT2LMHeadModel.from_pretrained('microsoft/DialoGPT-medium')

    # Step 2: Prepare the data
    text = "Hello, how are you today?\nI'm doing well, thanks for asking. How about you?\nI'm good too. What do you want to talk about?\n"
    text = """conversation = [    "User: Hello, how are you doing today?",    "Bot: Hi there, I'm doing well. How about you?",    "User: I'm doing pretty well, thanks for asking.",    "Bot: Great to hear! How can I assist you today?",    "User: I was wondering if you could help me with a question I have.",    "Bot: Of course! What's your question?",    "User: I was wondering how I can reset my password.",    "Bot: To reset your password, you can click on the 'forgot password' link on the login page and follow the instructions.",    "User: Thank you! That was very helpful.",    "Bot: You're welcome! Is there anything else I can assist you with?",    "User: No, that's all for now. Thanks again!",    "Bot: No problem, have a great day!"]"""

    inputs = tokenizer.encode(text, return_tensors='pt')
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    dataset = []
    for i in range(10):
        dataset.append(inputs)

    # Step 3: Set up the training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=1,
        per_device_train_batch_size=1,
        save_steps=5000,
        save_total_limit=2,
        logging_steps=5000,
        logging_dir='./logs',
    )

    # Step 4: Initialize the Trainer object
    trainer = Trainer(
        model=model,  # the instantiated 🤗 Transformers model to be trained
        args=training_args,  # training arguments, defined above
        train_dataset=dataset,  # training dataset
        data_collator=data_collator
    )

    # Step 5: Train the model
    trainer.train()

    # Step 6: Save the trained model and tokenizer
    model.save_pretrained('logic/trained_model_new')
    tokenizer.save_pretrained('logic/trained_token_new')
    return "test"


def data_collator(data):
    input_ids = []
    attention_mask = []
    labels = []
    for f in data:
        if len(f) == 2:
            input_ids.append(f[0])
            attention_mask.append(f[1])
        elif len(f) == 3:
            input_ids.append(f[0])
            attention_mask.append(f[1])
            labels.append(f[2])
        else:
            raise ValueError("Invalid input format. Each element of data should be a tuple of 2 or 3 elements.")
    return {'input_ids': torch.stack(input_ids), 'attention_mask': torch.stack(attention_mask), 'labels': torch.stack(labels)}


def res_from_custom_model(query):
    # model_path = 'logic/custom_data'
    # token_path = 'logic/token_path'
    model_path = 'logic/trained_model_new'
    token_path = 'logic/trained_token_new'
    # Load the fine-tuned model and tokenizer
    model = GPT2LMHeadModel.from_pretrained(model_path)
    tokenizer = GPT2Tokenizer.from_pretrained(token_path)
    # Set the model to generate text
    model.eval()

    input_ids = tokenizer.encode(query, return_tensors='pt')
    # Set the pad token ID to 0 and the EOS token ID to 50256 (the default for GPT-2)
    model.config.pad_token_id = 0
    model.config.eos_token_id = 50256
    generated_text = model.generate(
        input_ids,
        max_length=100,
        num_beams=5,
        no_repeat_ngram_size=2,
        early_stopping=True,

    )
    # Decode the generated text and print it
    generated_text = tokenizer.decode(generated_text[0], skip_special_tokens=True)
    print(generated_text)
    return generated_text


def chat_response(query):
    input_text = query
    tokenizer, model = pre_train_model()
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output_ids = model.generate(input_ids)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output_text


def another_test_full_train_n_test(query):
    # Load the pre-trained GPT-2 model and tokenizer
    model_name = 'gpt2'
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    # Add a new special token to the tokenizer to represent padding
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})

    # Use the new special token as the padding token
    tokenizer.pad_token = tokenizer.special_tokens_map['pad_token']
    # Load the training and testing data
    train_data = ["This is the first sentence.", "This is the second sentence."]
    test_data = ["This is the third sentence.", "This is the fourth sentence."]

    # Tokenize the training and testing data
    train_inputs = tokenizer(train_data, return_tensors='pt', padding=True, truncation=True)
    test_inputs = tokenizer(test_data, return_tensors='pt', padding=True, truncation=True)

    # Extract the input IDs and labels for the training and testing data
    train_input_ids = train_inputs['input_ids']
    train_labels = train_inputs['input_ids'].clone()
    train_labels[train_labels == tokenizer.pad_token_id] = -100  # ignore padding tokens during training
    test_input_ids = test_inputs['input_ids']
    test_labels = test_inputs['input_ids'].clone()
    test_labels[test_labels == tokenizer.pad_token_id] = -100  # ignore padding tokens during testing

    # Train the model on the training data
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
    for epoch in range(10):
        model.train()
        optimizer.zero_grad()
        outputs = model(train_input_ids, labels=train_labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch + 1} loss: {loss.item()}")

    # Test the model on the testing data
    model.eval()
    with torch.no_grad():
        outputs = model(test_input_ids)
        predicted_ids = outputs.logits.argmax(dim=-1)
        predicted_sentences = [tokenizer.decode(ids) for ids in predicted_ids]
        for i, sentence in enumerate(predicted_sentences):
            print(f"Input: {test_data[i]}\nPredicted output: {sentence}\n")
    return "success"


def eleuther_ai_gpt_model_back(input: str):
    from transformers import GPTNeoForCausalLM, GPT2Tokenizer
    from transformers import pipeline
    # model_name = "EleutherAI/gpt-neo-2.7B"
    # tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    # model = GPTNeoForCausalLM.from_pretrained(model_name)
    model = 'logic/trained_model_new_big'
    tokenizer = 'logic/trained_token_new_big'
    # model.save_pretrained('logic/trained_model_new_big')
    # tokenizer.save_pretrained('logic/trained_token_new_big')
    text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    generated_text = text_generator(input, max_length=50, do_sample=True)
    return {"text": generated_text[0]["generated_text"]}
