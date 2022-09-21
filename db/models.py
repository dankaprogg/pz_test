from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from misc import Base


class Foo(Base):
    __tablename__ = "foo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    parent_id = Column(UUID(as_uuid=True), ForeignKey(id))
    title = Column(String(256))
    registered_in = Column(DateTime, default=datetime.now)

    parent = relationship("foo.id", lazy="joined")
