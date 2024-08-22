# hdf5-xxh
Compute a xxHash of the Datasets in an HDF5 file.

## Motivation

For regression testing, it is sometimes useful to check for the strict equality of numerical data stored in an HDF5 file.
A reference copy of the HDF5 file could be saved, but this is not always desirable, especially if the file is very large.
Computing a hash digest of the HDF5 file is not possible because, for various reasons, HDF5 files are not byte-for-byte identical, even if the stored data is the same.
This small utility computes a hash digest of the datasets stored in the HDF5 files, thereby enabling an easy check for strict equality without the need to store a complete copy of the data itself.

## Installation

For now only source installation is possible:
```bash
pip install git+https://github.com/miccoli/hdf5-xxh.git
```

## Usage

```bash
$ h5xxhsum foo.h5
e92417e2e9a3425cffbe35fddc5f21a3  foo.h5
```

## Caveat emptor

I wrote this small utility for personal use, so there is no guarantee that the API will remain stable.
However, I believe it fills a small but useful niche.
Please feel free to open an issue if you think it can be improved.
