//! # Compression Algorithms
//!
//! This crates provides Encoders and Decoders of different algorithms. The code words are written from
//! and to bit streams where it is possible to write either the most or least significant 
//! bit first. The maximum possible code size is 16 bits. Both types rely on RAII to
//! produced correct results.

mod lzw;
mod bitstream;

pub use lzw::{
    Decoder,
    DecoderEarlyChange,
    Encoder,
    encode
};

pub use bitstream::{
    BitReader,
    BitWriter,
    LsbReader,
    LsbWriter,
    MsbReader,
    MsbWriter,
    Bits
};
