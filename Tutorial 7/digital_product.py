from product import Product


class DigitalProduct(Product):
    """A product delivered electronically (e.g. an operating system).

    Adds one attribute to Product: download size in megabytes.
    """

    PRODUCT_TYPE = "digital"

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    @property
    def download_size(self):
        """Download size in megabytes (read-only)."""
        return self.__download_size

    def display_information(self):
        """Common product info (from Product) plus the download size."""
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally via download."

    def to_dict(self):
        """Common fields (from Product) plus the type identifier and size."""
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   data["download_size"])

    def __str__(self):
        return f"{super().__str__()} | Download Size: {self.__download_size} MB"