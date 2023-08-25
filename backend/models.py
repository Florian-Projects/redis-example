from tortoise import fields, models
from tortoise.contrib.pydantic.creator import pydantic_model_creator

class Books(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    isbn = fields.CharField(max_length=20)

    # pictures will be b64 encoded
    cover_picture = fields.TextField()
    


Books_Pydantic = pydantic_model_creator(Books, name="Book")
