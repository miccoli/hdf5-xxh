# SPDX-FileCopyrightText: 2024-present S. Miccoli <stefano.miccoli@polimi.it>
#
# SPDX-License-Identifier: MIT
import logging

import h5py
import xxhash

logger = logging.getLogger(__name__)


class Walker:
    def __init__(self, /, hashfun=xxhash.xxh3_128):
        self._names = []
        self._digest = hashfun()

    def __call__(self, name, obj):
        # runtime check of lexicographical iteration order
        assert name > (
            self._names[-1] if self._names else ""
        ), f"Visiting in unexpected order: {name}, {self._names}"
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

        logger.debug("hashing '%s' (%s)", obj.name, obj.dtype.str)
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
