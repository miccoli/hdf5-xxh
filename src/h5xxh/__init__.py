# SPDX-FileCopyrightText: 2024-present S. Miccoli <stefano.miccoli@polimi.it>
#
# SPDX-License-Identifier: MIT
import h5py
import xxhash


class Walker:
    def __init__(self, /, hashfun=xxhash.xxh3_128):
        self._names = []
        self._digest = hashfun()

    def __call__(self, name, obj):
        if isinstance(obj, h5py.Dataset):
            assert name > (
                self._names[-1] if self._names else ""
            ), f"Visiting in unexpected order: {name}, {self._names}"
            self._names.append(name)
            self._digest.update(obj[()])

    @property
    def hexdigest(self):
        """Digest of the visited 'Dataset's"""
        return self._digest.hexdigest()

    @property
    def names(self):
        """Names of the visited 'Dataset's"""
        return self._names
