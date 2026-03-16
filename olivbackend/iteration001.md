## Problem Statement: 
   In the first original iteration: the model used was Google Gemini 1.5 flash
   with a background knowledge limited to October 2023

   However we want to also use the function call tools method for Grounding: 
   specially the  conversation below


   We move from "conversational prompt" and move towards Structured Outputs.


   The reason you are seeing different results (one saying October 2025 and another saying 2023) --> Hallucination or drawing from old training data when it can't find a clear answer in search snippets


   Google-genai SDK allows to define a Schema