import openai
import os

openai.organization = "org-fBoqj45hvJisAEGMR5cvPnDS"
openai.api_key = "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"

a=openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

print(a)