''' Define the Layers '''
import torch.nn as nn
import torch
from transformer.SubLayers import MultiHeadAttention, PositionwiseFeedForward, LowRankPositionwiseFeedForward, \
LowRankMultiHeadAttention, LowRankResidualMultiHeadAttention, LowRankResidualPositionwiseFeedForward


from torch.cuda.amp import autocast

import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

__author__ = "Yu-Hsiang Huang"


class EncoderLayer(nn.Module):
    ''' Compose with two layers '''

    def __init__(self, d_model, d_inner, n_head, d_k, d_v, dropout=0.1):
        super(EncoderLayer, self).__init__()
        self.slf_attn = MultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.pos_ffn = PositionwiseFeedForward(d_model, d_inner, dropout=dropout)

    @autocast()
    def forward(self, enc_input, slf_attn_mask=None):
        enc_output, enc_slf_attn = self.slf_attn(
            enc_input, enc_input, enc_input, mask=slf_attn_mask)
        enc_output = self.pos_ffn(enc_output)
        return enc_output, enc_slf_attn


class DecoderLayer(nn.Module):
    ''' Compose with three layers '''

    def __init__(self, d_model, d_inner, n_head, d_k, d_v, dropout=0.1):
        super(DecoderLayer, self).__init__()
        self.slf_attn = MultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.enc_attn = MultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.pos_ffn = PositionwiseFeedForward(d_model, d_inner, dropout=dropout)

    @autocast()
    def forward(
            self, dec_input, enc_output,
            slf_attn_mask=None, dec_enc_attn_mask=None):
        dec_output, dec_slf_attn = self.slf_attn(
            dec_input, dec_input, dec_input, mask=slf_attn_mask)
        dec_output, dec_enc_attn = self.enc_attn(
            dec_output, enc_output, enc_output, mask=dec_enc_attn_mask)
        dec_output = self.pos_ffn(dec_output)
        return dec_output, dec_slf_attn, dec_enc_attn


# Low Rank

class LowRankEncoderLayer(nn.Module):
    ''' Compose with two layers '''

    def __init__(self, d_model, d_inner, n_head, d_k, d_v, dropout=0.1):
        super(LowRankEncoderLayer, self).__init__()
        self.slf_attn = LowRankMultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.pos_ffn = LowRankPositionwiseFeedForward(d_model, d_inner, dropout=dropout)

    @autocast()
    def forward(self, enc_input, slf_attn_mask=None):
        enc_output, enc_slf_attn = self.slf_attn(
            enc_input, enc_input, enc_input, mask=slf_attn_mask)
        enc_output = self.pos_ffn(enc_output)
        return enc_output, enc_slf_attn


class LowRankDecoderLayer(nn.Module):
    ''' Compose with three layers '''

    def __init__(self, d_model, d_inner, n_head, d_k, d_v, dropout=0.1):
        super(LowRankDecoderLayer, self).__init__()
        self.slf_attn = LowRankMultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.enc_attn = LowRankMultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.pos_ffn = LowRankPositionwiseFeedForward(d_model, d_inner, dropout=dropout)

    @autocast()
    def forward(
            self, dec_input, enc_output,
            slf_attn_mask=None, dec_enc_attn_mask=None):
        dec_output, dec_slf_attn = self.slf_attn(
            dec_input, dec_input, dec_input, mask=slf_attn_mask)
        dec_output, dec_enc_attn = self.enc_attn(
            dec_output, enc_output, enc_output, mask=dec_enc_attn_mask)
        dec_output = self.pos_ffn(dec_output)
        return dec_output, dec_slf_attn, dec_enc_attn


# Low Rank Residual

class LowRankResidualEncoderLayer(nn.Module):
    ''' Compose with two layers '''

    def __init__(self, d_model, d_inner, n_head, d_k, d_v, dropout=0.1):
        super(LowRankResidualEncoderLayer, self).__init__()
        self.slf_attn = LowRankResidualMultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.pos_ffn = LowRankResidualPositionwiseFeedForward(d_model, d_inner, dropout=dropout)

    @autocast()
    def forward(self, enc_input, slf_attn_mask=None):
        enc_output, enc_slf_attn = self.slf_attn(
            enc_input, enc_input, enc_input, mask=slf_attn_mask)
        enc_output = self.pos_ffn(enc_output)
        return enc_output, enc_slf_attn


class LowRankResidualDecoderLayer(nn.Module):
    ''' Compose with three layers '''

    def __init__(self, d_model, d_inner, n_head, d_k, d_v, dropout=0.1):
        super(LowRankResidualDecoderLayer, self).__init__()
        self.slf_attn = LowRankResidualMultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.enc_attn = LowRankResidualMultiHeadAttention(n_head, d_model, d_k, d_v, dropout=dropout)
        self.pos_ffn = LowRankResidualPositionwiseFeedForward(d_model, d_inner, dropout=dropout)

    @autocast()
    def forward(
            self, dec_input, enc_output,
            slf_attn_mask=None, dec_enc_attn_mask=None):
        dec_output, dec_slf_attn = self.slf_attn(
            dec_input, dec_input, dec_input, mask=slf_attn_mask)
        dec_output, dec_enc_attn = self.enc_attn(
            dec_output, enc_output, enc_output, mask=dec_enc_attn_mask)
        dec_output = self.pos_ffn(dec_output)
        return dec_output, dec_slf_attn, dec_enc_attn