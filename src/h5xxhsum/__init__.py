# SPDX-FileCopyrightText: 2024-present S. Miccoli <stefano.miccoli@polimi.it>
#
# SPDX-License-Identifier: MIT
import logging

import h5py
import xxhash

from h5xxhsum._version import __version__

__all__ = ["Walker", "__version__"]

logger = logging.getLogger(__name__)


class Walker:
    def __init__(self, *, hashfun=xxhash.xxh3_128, chunked=False):
        self.chunked = chunked
        self.hashfun = hashfun

        self._names = []
        self._level1 = []
        self._digest = self.hashfun()

    def _iter_data(self, dset, /):
        if not self.chunked or dset.chunks is None:
            yield dset[()]
        else:
            for sl in dset.iter_chunks():
                yield dset[sl]

    def __call__(self, name, obj, /):
        """update hash"""

        # hash only datasets
        if not isinstance(obj, h5py.Dataset):
            return

        # Some object are skipped, and do not contribute to the overall hash.
        # Currently skipped:
        # - object arrays ('O') contain pointers to python Objects: it is
        #   in general impossible to compute an immutable hash
        if obj.dtype.hasobject:
            logger.warning(
                "%s: cannot hash '%s' (%s)",
                obj.file.filename,
                obj.name,
                obj.dtype.str,
            )
            return

        digest = self.hashfun()
        for data in self._iter_data(obj):
            digest.update(data)
        logger.debug("%s %s", name, digest.hexdigest())

        self._digest.update(digest.digest())
        self._level1.append(digest.hexdigest())
        self._names.append(name)

    @property
    def hexdigest(self):
        """Digest of the visited 'Dataset's"""
        return self._digest.hexdigest()

    @property
    def names(self):
        """Names of the visited 'Dataset's"""
        return self._names

    @property
    def level1(self):
        return zip(self._names, self._level1, strict=True)
