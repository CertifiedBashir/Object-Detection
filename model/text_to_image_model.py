from extensions import db


class TextToImage(db.Model):
    """Model representing a text-to-image mapping record."""

    __tablename__ = "text_to_images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)

    # Many-to-one relationship back to the Image model
    image = db.relationship("Image", back_populates="text_to_images")

    def __repr__(self):
        return "<TextToImage id={} image_id={} text={}>".format(
            self.id, self.image_id, self.text
        )
