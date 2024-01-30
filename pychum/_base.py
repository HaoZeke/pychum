# SPDX-FileCopyrightText: 2023-present Rohit Goswami <rog32@hi.is>
#
# SPDX-License-Identifier: MIT
from abc import ABC, abstractmethod
from pathlib import Path


class InpGeneratorBase(ABC):
    def __init__(self, filename):
        self.conf_path = Path(filename)
        self.config = None
        self.load_computation()

    def load_computation(self):
        with self.conf_path.open(mode="r") as file:
            self.config = self.parse_config(file)

    @abstractmethod
    def generate_config(self, file):
        pass
