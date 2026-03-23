"""
input data.py 
TODO: here I just put the data directly here 
which can be imported. however, the data can be read
online or anywhere or even a connector.
"""

import os 
import numpy as np



# Sample Conversaton about research paper search (30 Messages)
# Includes: technical info, emotional context, entities, action items

SAMPLE_RESEARCH_CONVERSATION = [
    ("user",
     "Hi! I'm working on my PhD thesis about transformer architectures in NLP. I need to find recent papers on attention mechanisms."),
    ("assistant",
     "Great topic! I can help you find relevant papers. Are you looking for foundational papers like 'Attention Is All You Need' by Vaswani et al. (2017), or more recent advances from 2023-2024?"),
    ("user", "FlashAttention sounds interesting! Can you find papers that cite it or build upon it?"),
    ("assistant",
     "Found several citing works: 'Ring Attention' extends FlashAttention for distributed training across GPUs. 'Paged Attention' from vLLM applies similar memory optimization for inference. Also, 'Flash-Decoding' focuses on the decoding phase specifically."),
    ("user",
     "This is exactly what I needed! I'm getting excited about this direction. Who are the main researchers in this space?"),
    ("assistant",
     "Key researchers include: Tri Dao (Stanford, FlashAttention author), Christopher Ré (Stanford, his advisor), Dan Fu (together.ai), and the team at Meta AI working on LLaMA optimizations. Dr. Sarah Chen at MIT is also doing great work on theoretical analysis of efficient attention."),
    ("user",
     "I should reach out to Dr. Chen - her work aligns with my theoretical focus. Can you find her recent publications?"),
    ("assistant",
     "Dr. Sarah Chen's recent papers include: 'Theoretical Bounds on Attention Complexity' (NeurIPS 2023), 'Provably Efficient Sparse Attention' (ICML 2024), and a preprint on arXiv about 'Linear Attention with Guaranteed Expressiveness'. Her email is listed as schen@mit.edu on her lab page."),
    ("user",
     "Amazing! I'm feeling much more confident about my literature review now. What about applications to code generation?"),
    ("assistant",
     "For code generation with efficient attention, check out: 'StarCoder' by BigCode - uses multi-query attention, 'CodeLlama' with grouped-query attention, and 'SantaCoder' which analyzes attention patterns in code. Also relevant: 'Repository-Level Code Generation' by Ding et al. addresses long-context code with retrieval-augmented approaches."),
    ("user",
     "Wait, retrieval-augmented approaches - that's actually closer to what I want to do! Tell me more about that direction."),
    ("assistant",
     "RAG for code is fascinating! Key papers: 'REALM' and 'RAG' by Lewis et al. (foundational), 'Retrieval-Augmented Code Generation' by Parvez et al., 'DocPrompting' which retrieves documentation, and 'ReACC' for repository-level completion. The main insight is reducing attention burden by retrieving relevant context."),
    ("user",
     "I'm now thinking my thesis should combine efficient attention WITH retrieval. Is anyone doing that combination?"),
    ("assistant",
     "Yes! 'RETRO' by DeepMind combines retrieval with transformers efficiently. 'Atlas' by Meta shows retrieval can match larger models. More recently, 'Self-RAG' adds self-reflection, and 'RAPTOR' uses hierarchical retrieval. Prof. Michael Zhang at Berkeley published 'Efficient Retrieval-Augmented Transformers' just last month."),
    ("user", "Prof. Zhang's work sounds perfect! I'm a bit nervous about reaching out to senior researchers though..."),
    ("assistant",
     "That's completely normal to feel! A few tips: 1) Read their papers thoroughly first, 2) Mention specific aspects you found interesting, 3) Share your preliminary ideas briefly, 4) Ask a specific question rather than general advice. Most researchers appreciate genuine interest from PhD students."),
    ("user",
     "Thanks, that's helpful advice. Let me refocus - can you summarize the key technical approaches we've discussed?"),
    ("assistant",
     "Here's a summary of efficient attention approaches: 1) **Sparse Attention**: Longformer, BigBird - O(n) complexity via patterns, 2) **Memory-Efficient**: FlashAttention - same computation, less memory, 3) **Linear Attention**: Performers, Linear Transformers - approximate softmax, 4) **Retrieval-Augmented**: RETRO, RAG - offload context to retrieval. Each has tradeoffs between speed, memory, and quality."),
    ("user", "What are the main evaluation benchmarks for these methods?"),
    ("assistant",
     "Key benchmarks include: 1) **Long Range Arena (LRA)** - synthetic tasks up to 16K tokens, 2) **SCROLLS** - real long-document tasks, 3) **PG-19** - book-level language modeling, 4) **CodeXGLUE** - for code tasks, 5) **Needle in a Haystack** - retrieval over long contexts. Also check perplexity on standard LM benchmarks and wall-clock time comparisons."),
    ("user", "I should probably implement some baselines. What frameworks support these efficient attention methods?"),
    ("assistant",
     "Framework support: 1) **FlashAttention** - native in PyTorch 2.0+, also xformers, 2) **HuggingFace Transformers** - many models supported, 3) **DeepSpeed** - has sparse attention ops, 4) **FairScale** - Meta's library, 5) **Triton** - for custom CUDA kernels. I'd recommend starting with HuggingFace + FlashAttention for easiest setup."),
    ("user", "Perfect! I'm feeling much more organized now. One more thing - any good survey papers I should read?"),
    ("assistant",
     "Essential surveys: 1) 'Efficient Transformers: A Survey' by Tay et al. (2022) - comprehensive overview, 2) 'A Survey on Long Text Modeling with Transformers' by Dong et al., 3) 'Scaling Laws for Neural Language Models' by Kaplan et al. - understanding model scaling, 4) 'Formal Algorithms for Transformers' by Phuong & Hutter - theoretical foundations."),
    ("user",
     "The Tay et al. survey is exactly what I needed as a starting point. Thank you so much for this deep dive!"),
    ("assistant",
     "You're welcome! To summarize your research direction: combining efficient attention (FlashAttention-style) with retrieval augmentation (RETRO-style) for code generation. Key contacts: Dr. Sarah Chen (MIT, theory), Prof. Michael Zhang (Berkeley, efficient RAG), Tri Dao (Stanford, FlashAttention). Your next steps: 1) Read the Tay survey, 2) Implement baselines with HuggingFace, 3) Reach out to researchers."),
    ("user", "One last question - what conferences should I target for submission?"),
    ("assistant",
     "Top venues for this work: 1) **NeurIPS** - broad ML, strong on efficiency, 2) **ICML** - theoretical contributions welcome, 3) **ACL/EMNLP** - if NLP-focused, 4) **ICLR** - representation learning angle, 5) **MLSys** - if systems-focused. Workshop options: EfficientNLP, Efficient Deep Learning. Deadlines typically: NeurIPS (May), ICML (Jan), ACL (Jan), ICLR (Sept)."),
    ("user",
     "I think I'll aim for NeurIPS first. This has been an incredibly productive conversation - I went from confused to having a clear research plan!"),
    ("assistant",
     "That's wonderful to hear! Your enthusiasm is contagious. Remember: thesis writing is a marathon, not a sprint. Take breaks, celebrate small wins, and don't hesitate to reach out to your advisor and the researchers we discussed. Good luck with your PhD journey - efficient attention + retrieval for code is a promising direction with real impact potential!"),
]

# TODO: Build Data Connectors on how to import 

