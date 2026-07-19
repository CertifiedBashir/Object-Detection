import os

base = os.path.dirname(os.path.abspath(__file__))

image_model = """\
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Image(Base):
    \"\"\"Model representing a stored image record.\"\"\"

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String, nullable=False)

    # One Image can have many TextToImage records
    text_to_images = relationship(
        "TextToImage",
        back_populates="image",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return "<Image id={} url={}>".format(self.id, self.image_url)
"""

text_to_image_model = """\
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .image_model import Base


class TextToImage(Base):
    \"\"\"Model representing a text-to-image mapping record.\"\"\"

    __tablename__ = "text_to_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)

    # Many-to-one relationship back to the Image model
    image = relationship("Image", back_populates="text_to_images")

    def __repr__(self):
        return "<TextToImage id={} image_id={} text={}>".format(
            self.id, self.image_id, self.text
        )
"""

with open(os.path.join(base, "image_model.py"), "w") as f:
    f.write(image_model)
print("image_model.py written")

with open(os.path.join(base, "text_to_image_model.py"), "w") as f:
    f.write(text_to_image_model)
print("text_to_image_model.py written")
