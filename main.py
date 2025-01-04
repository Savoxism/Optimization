import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np
import os
import math
import copy

class InputEmbeddings(nn.Module):
    def __init__(self, d_model, vocab_size):
        super().__init__()
        self.d_model = d_model
        self.vocab_size = vocab_size
        self.embedding = nn.Embedding(vocab_size, d_model)
        
    def forward(self, x):
        output = self.embedding(x) * math.sqrt(self.d_model)
        return output

class PositionalEmbeddings(nn.Module):
    def __init__(self, d_model, seq_len=200, dropout=0.1) :
        super().__init__()
        self.d_model = d_model
        self.seq_len = seq_len
        self.dropout = nn.Dropout(dropout)  # Initialize dropout

        # Create positional encoding matrix
        pe = torch.zeros(seq_len, d_model)
        position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)  # (seq_len, 1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        # Apply sin to even indices and cos to odd indices
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)  # (1, seq_len, d_model)
        self.register_buffer('pe', pe)  # Save as a persistent buffer
 
        
    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :].requires_grad_(False)  # Add positional encoding
        return self.dropout(x)  # Apply dropout
    
def attention(q, k, v, mask=None, dropout=None):
    """
    q: query shape (batch_size, num_heads, seq_len, d_model)
    k: key shape (batch_size, num_heads, seq_len, d_model)
    v: value shape (batch_size, num_heads, seq_len, d_model)
    mask: (batch_size, 1, 1, seq_len)
    output: (batch_size, num_heads, seq_len, d_model)
    """
    d_k = q.size(-1)
    scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(d_k)

    if mask is not None:
        mask = mask.unsqueeze(1)
        scores = scores.masked_fill(mask == 0, -1e9)

    weights = F.softmax(scores, dim=-1)

    if dropout is not None:
        weights = dropout(weights)

    output = torch.matmul(weights, v)
    return output, weights

class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads, d_model, dropout=0.1):
        super().__init__()
       
        assert d_model % num_heads == 0
       
        self.d_model = d_model
        self.d_k = d_model // num_heads
        self.h = num_heads
        self.attn = None
        
        self.q_linear = nn.Linear(d_model, d_model)
        self.k_linear = nn.Linear(d_model, d_model)
        self.v_linear = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
        self.out = nn.Linear(d_model, d_model)
        
    def forward(self, q, k, v, mask=None):
        """
        q: query shape (batch_size, seq_len, d_model)
        k: key shape (batch_size, seq_len, d_model)
        v: value shape (batch_size, seq_len, d_model)
        mask: (batch_size, 1, seq_len)
        output: (batch_size, seq_len, d_model)
        """
       
        batch_size = q.size(0)
        
        q = self.q_linear(q).view(batch_size, -1, self.h, self.d_k) # (batch_size, seq_len, d_model) -> (batch_size, seq_len, num_heads, d_k)
        k = self.k_linear(k).view(batch_size, -1, self.h, self.d_k)
        v = self.v_linear(v).view(batch_size, -1, self.h, self.d_k)
        
        q = q.transpose(1, 2) # (batch_size, seq_len, num_heads, d_k) -> (batch_size, num_heads, seq_len, d_k)
        k = k.transpose(1, 2) 
        v = v.transpose(1, 2)
        
        scores, self.attn = attention(q, k, v, mask=mask, dropout=self.dropout)
        concat = scores.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
        output = self.out(concat)
        
        return output
    
class LayerNormalization(nn.Module):
    def __init__(self, d_model, eps=1e-6):
        super().__init__()
        
        self.size = d_model
        
        self.alpha = nn.Parameter(torch.ones(self.size))
        self.bias = nn.Parameter(torch.zeros(self.size))
        
        self.eps = eps
        
    def forward(self, x):
        norm = self.alpha * (x - x.mean(dim=-1, keepdim=True)) / (x.std(dim=-1, keepdim=True) + self.eps) + self.bias 
        
        return norm       
    
class FeedForward(nn.Module):
    def __init__(self, d_model, d_ff=2048, dropout=0.1):
        super().__init__()
        
        self.linear_1 = nn.Linear(d_model, d_ff)
        
        self.dropput = nn.Dropout(dropout)
        
        self.linear_2 = nn.Linear(d_ff, d_model)
        
    def forward(self, x):
        x = self.dropout(F.relu(self.linear_1(x)))
        x = self.linear_2(x)
        return x
    
class EncoderLayer(nn.Module):
    def __init__(self, d_model, heads, dropout=0.1):
        super().__init__()
        
        self.norm_1 = LayerNormalization(d_model)
        self.norm_2 = LayerNormalization(d_model)
        self.attn = MultiHeadAttention(heads, d_model, dropout=dropout)
        
        self.ff = FeedForward(d_model, dropout=dropout)
        
        self.dropout_1 = nn.Dropout(dropout)
        self.dropout_2 = nn.Dropout(dropout)
        
    def forward(self, x, mask):
        """
        x: (batch_size, seq_len, d_model)
        mask: (batch_size, 1, seq_len)
        output: (batch_size, seq_len, d_model)
        """
        
        x2 = self.norm_1(x)
        
        x = x + self.dropout_1(self.attn(x2, x2, x2, mask))
        
        x2 = self.norm_2(x)
        
        x = x + self.dropout_2(self.ff(x2))
        return x
        
        
class DecoderLayer(nn.Module):
    def __init__(self, d_model, heads, dropout=0.1):
        super().__init__()
        
        self.norm_1 = LayerNormalization(d_model)
        self.norm_2 = LayerNormalization(d_model)
        self.norm_3 = LayerNormalization(d_model)
        
        self.dropout_1 = nn.Dropout(dropout)
        self.dropout_2 = nn.Dropout(dropout)
        self.dropout_3 = nn.Dropout(dropout)
        
        self.attn_1 = MultiHeadAttention(heads, d_model, dropout=dropout)
        self.attn_2 = MultiHeadAttention(heads, d_model, dropout=dropout)
        
        self.ff = FeedForward(d_model, dropout=dropout)
        
    def forward(self, x, e_outputs, src_mask, trg_mask):
        """
        x: batch_size x seq_length x d_model
        e_outputs: batch_size x seq_length x d_model
        src_mask: batch_size x 1 x seq_length
        trg_mask: batch_size x 1 x seq_length
        """
        
        x2 = self.norm_1(x)
        
        # First multi-head attention layer, 
        x = x + self.dropout_1(self.attn_1(x2, x2, x2, trg_mask))
        
        x2 = self.norm_2(x)
        
        # masked multi-head attention layer
        x = x + self.dropout_2(self.attn_2(x2, e_outputs, e_outputs, src_mask))
        
        x2 = self.norm_3(x)
        x = x + self.dropout_3(self.ff(x2))
        
        return x
    

def get_clones(module, N):
    return nn.ModuleList([copy.deepcopy(module) for i in range(N)])

class Encoder(nn.Module):
    def __init__(self, vocab_size, d_model, N, heads, dropout):
        super().__init__()
        
        self.N = N
        self.embed = InputEmbeddings(d_model, vocab_size)
        self.pe = PositionalEmbeddings(d_model, dropout=dropout)
        self.layers = get_clones(EncoderLayer(d_model, heads, dropout), N)
        self.norm = LayerNormalization(d_model)
        
    def forward(self, src, mask):
        """
        src: batch_size x seq_length
        mask: batch_size x 1 x seq_length
        output: batch_size x seq_length x d_model
        """
        x = self.embed(src)
        x = self.pe(x)
        for i in range(self.N):
            x = self.layers[i](x, mask)
        return self.norm(x)
        
        
class Decoder(nn.Module):
    def __init__(self, vocab_size, d_model, N, heads, dropout):
        super().__init__()
        
        self.N = N
        self.embed = InputEmbeddings(d_model, vocab_size)
        self.pe = PositionalEmbeddings(d_model, dropout=dropout)
        self.layers = get_clones(DecoderLayer(d_model, heads, dropout), N)
        self.norm = LayerNormalization(d_model)
        
    def forward(self, trg, e_outputs, src_mask, trg_mask):
        """
        trg: batch_size x seq_length
        e_outputs: batch_size x seq_length x d_model
        src_mask: batch_size x 1 x seq_length
        trg_mask: batch_size x 1 x seq_length
        output: batch_size x seq_length x d_model
        """
        x = self.embed(trg)
        x = self.pe(x)
        for i in range(self.N):
            x = self.layers[i](x, e_outputs, src_mask, trg_mask)
        return self.norm(x)
    
class Transformer(nn.Module):
    def __init__(self, src_vocab, trg_vocab, d_model, N, heads, dropout):
        super().__init__()
        self.encoder = Encoder(src_vocab, d_model, N, heads, dropout)
        
        self.decoder = Decoder(trg_vocab, d_model, N, heads, dropout)
        
        self.out = nn.Linear(d_model, trg_vocab)
        
    def forward(self, src, trg, src_mask, trg_mask):
        """
        src: batch_size x seq_length
        trg: batch_size x seq_length
        src_mask: batch_size x 1 x seq_length
        trg_mask: batch_size x 1 x seq_length
        output: batch_size x seq_length x trg_vocab
        """
        e_outputs = self.encoder(src, src_mask)
        d_output = self.decoder(trg, e_outputs, src_mask, trg_mask)
        output = self.out(d_output)
        return output
    
    





