#from . import Base
#
#from sqlalchemy import (
#    Column,
#    Integer,
#    UnicodeText,
#    String,
#    )
#
#class Page(Base):
#    __tablename__ = 'pages'
#    id = Column(Integer, primary_key=True)
#    link_title = Column(UnicodeText, unique=True)
#    title = Column(UnicodeText) 
#    subtitle = Column(UnicodeText) 
#    type = Column(String)
#    prev = Column(Integer)
#    next = Column(Integer)
#    content = Column(UnicodeText)
#
#    def __init__(self, link_title, title, subtitle, type, prev, next):
#        self.link_title = link_title
#        self.title = title
#        self.subtitle = subtitle
#        self.type = type
#        self.prev = prev
#        self.next = next
#        self.content = u""
