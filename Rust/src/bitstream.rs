//! Module with bit read and write functions

// Dependencies
use std::io::{self, Write};

/// Stores the consumed bytes and reconstructed bits or
/// only the consumed bytes (if the supplied buffer was not bit enough)
pub enum Bits {
    Some(usize, u16),
    None(usize),
}

// Bit Reader Interface
pub trait BitReader {
    // Reads and returns the next n bits.
    /// buf: reference to u8 buffer
    /// n: buffer size
    fn read_bits(&mut self, buf: &[u8], n: u8) -> Bits;
}

// Bit Writer Interface
pub trait BitWriter {
    // Writes next n bits.
    /// v: 
    /// n:
    fn write_bits(&mut self, v: u16, n: u8) -> io::Result<()>;
}

macro_rules! define_bit_readers {
    {$(
        $name:ident, #[$doc:meta];
    )*} => {

$( // START Structure definitions

#[$doc]
#[derive(Debug)]
pub struct $name {
    bits: u8,
    acc: u32,
}

impl $name {

    /// Creates a new bit reader
    pub fn new() -> $name {
        $name {
            bits: 0,
            acc: 0,
        }
    }


}

)* // END Structure definitions

    }
}

define_bit_readers!{
    LsbReader, #[doc = "Reads bits from a byte stream, LSB first."];
    MsbReader, #[doc = "Reads bits from a byte stream, MSB first."];
}

impl BitReader for LsbReader {

    fn read_bits(&mut self, mut buf: &[u8], n: u8) -> Bits {
        if n > 16 {
            // This is a logic error the program should have prevented this
            // Ideally we would used bounded a integer value instead of u8
            panic!("Cannot read more than 16 bits")
        }
        let mut consumed = 0;
        while self.bits < n {
            let byte = if buf.len() > 0 {
                let byte = buf[0];
                buf = &buf[1..];
                byte
            } else {
                return Bits::None(consumed)
            };
            self.acc |= (byte as u32) << self.bits;
            self.bits += 8;
            consumed += 1;
        }
        let res = self.acc & ((1 << n) - 1);
        self.acc >>= n;
        self.bits -= n;
        Bits::Some(consumed, res as u16)
    }

}

impl BitReader for MsbReader {

    fn read_bits(&mut self, mut buf: &[u8], n: u8) -> Bits {
        if n > 16 {
            // This is a logic error the program should have prevented this
            // Ideally we would used bounded a integer value instead of u8
            panic!("Cannot read more than 16 bits")
        }
        let mut consumed = 0;
        while self.bits < n {
            let byte = if buf.len() > 0 {
                let byte = buf[0];
                buf = &buf[1..];
                byte
            } else {
                return Bits::None(consumed)
            };
            self.acc |= (byte as u32) << (24 - self.bits);
            self.bits += 8;
            consumed += 1;
        }
        let res = self.acc >> (32 - n);
        self.acc <<= n;
        self.bits -= n;
        Bits::Some(consumed, res as u16)
    }
}

macro_rules! define_bit_writers {
    {$(
        $name:ident, #[$doc:meta];
    )*} => {

$( // START Structure definitions

#[$doc]
#[allow(dead_code)]
pub struct $name<W: Write> {
    w: W,
    bits: u8,
    acc: u32,
}

impl<W: Write> $name<W> {
    /// Creates a new bit reader
    #[allow(dead_code)]
    pub fn new(writer: W) -> $name<W> {
        $name {
            w: writer,
            bits: 0,
            acc: 0,
        }
    }
}

impl<W: Write> Write for $name<W> {

    fn write(&mut self, buf: &[u8]) -> io::Result<usize> {
        if self.acc == 0 {
            self.w.write(buf)
        } else {
            for &byte in buf.iter() {
                self.write_bits(byte as u16, 8)?;
            }
            Ok(buf.len())
        }
    }

    fn flush(&mut self) -> io::Result<()> {
        let missing = 8 - self.bits;
        if missing > 0 {
            self.write_bits(0, missing)?;
        }
        self.w.flush()
    }
}

)* // END Structure definitions

    }
}

define_bit_writers!{
    LsbWriter, #[doc = "Writes bits to a byte stream, LSB first."];
    MsbWriter, #[doc = "Writes bits to a byte stream, MSB first."];
}

impl<W: Write> BitWriter for LsbWriter<W> {

    fn write_bits(&mut self, v: u16, n: u8) -> io::Result<()> {
        self.acc |= (v as u32) << self.bits;
        self.bits += n;
        while self.bits >= 8 {
            self.w.write_all(&[self.acc as u8])?;
            self.acc >>= 8;
            self.bits -= 8

        }
        Ok(())
    }

}

impl<W: Write> BitWriter for MsbWriter<W> {

    fn write_bits(&mut self, v: u16, n: u8) -> io::Result<()> {
        self.acc |= (v as u32) << (32 - n - self.bits);
        self.bits += n;
        while self.bits >= 8 {
            self.w.write_all(&[(self.acc >> 24) as u8])?;
            self.acc <<= 8;
            self.bits -= 8

        }
        Ok(())
    }

}

// Test module
#[cfg(test)]
mod test {
    use super::{BitReader, BitWriter, Bits};

    #[test]
    fn lsb_reader_writer() {
        // Test the LsbReader and LsbWriter.
        let data = [255, 20, 40, 120, 128];
        let mut offset = 0;
        let mut expanded_data = Vec::new();
        let mut reader = super::LsbReader::new();
        while let Bits::Some(consumed, b) = reader.read_bits(&data[offset..], 10) {
            offset += consumed;
            expanded_data.push(b)
        }
        let mut compressed_data = Vec::new();
        {
            let mut writer = super::LsbWriter::new(&mut compressed_data);
            for &datum in expanded_data.iter() {
                let _  = writer.write_bits(datum, 10);
            }
        }
        assert_eq!(&data[..], &compressed_data[..])
    }

    #[test]
    fn msb_reader_writer() {
        // Similar to the previous test, but using MsbReader and MsbWriter instead of LsbReader and LsbWriter.
        let data = [255, 20, 40, 120, 128];
        let mut offset = 0;
        let mut expanded_data = Vec::new();
        let mut reader = super::MsbReader::new();
        while let Bits::Some(consumed, b) = reader.read_bits(&data[offset..], 10) {
            offset += consumed;
            expanded_data.push(b)
        }
        let mut compressed_data = Vec::new();
        {
            let mut writer = super::MsbWriter::new(&mut compressed_data);
            for &datum in expanded_data.iter() {
                let _  = writer.write_bits(datum, 10);
            }
        }
        assert_eq!(&data[..], &compressed_data[..])
    }
}