from extensions import db


class Image(db.Model):
    """Model representing a stored image record."""

    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(500), nullable=False)

    # One Image can have many TextToImage records
    text_to_images = db.relationship(
        "TextToImage",
        back_populates="image",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return "<Image id={} url={}>".format(self.id, self.image_url)
