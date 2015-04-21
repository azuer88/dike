#!/user/bin/env python
# -*- coding: utf-8 -*-
"""
Define all the data classes:
    Category - Cagetory of the offenses
    Offenses
    PartyKind - the type of parties:
        Counsel for Accused/Defendant
        Counsel for Victim/Plaintiff
        Defendant / Accused
        Plaintiff / Victim
        Witness
    Party - the parties of a case
    Doocket - the case info
    EventType - what the names of the different events/schedules
    Event - when, what, and remarks... docket history
"""

import sys

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
# import for testing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


_Base = declarative_base()
_Engine = None
_SessionMaker = None


def _get_base():
    global _Base
    assert _Base is not None
    return _Base


def get_engine(*argv, **kwarg):
    """Create an engine if there is none, using the passed arguments"""
    global _Engine
    if _Engine is None:
        _Engine = create_engine(*argv, **kwarg)
    return _Engine


def _get_session_maker():
    """Create a session maker bound to _Engine,
    assumes that get_engine is called first"""
    global _SessionMaker
    if _SessionMaker is None:
        engine = get_engine()
        _SessionMaker = sessionmaker(bind=engine)
    return _SessionMaker


def get_session():
    """Create and return a session from our global session maker factory"""
    global _Engine
    assert _Engine is not None
    session_maker = _get_session_maker()
    assert session_maker is not None
    return session_maker()


def init_tables():
    """Drop all and creates the tables,
    be sure that there are no existing data"""
    global _Engine
    assert _Engine is not None
    engine = get_engine()
    base = _get_base()

    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)


class Category(_Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False, default='')
    sort_rank = Column(Integer, default=0)

    def __repr__(self):
        return "<category(name=%s)>" % self.name


class Offense(_Base):
    __tablename__ = "offenses"

    id = Column(Integer, primary_key=True)
    title = Column(String(60), nullable=False, default='')
    section = Column(String(60), nullable=False, default='')
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', backref=backref('offenses',
                                                        lazy='dynamic'))

    def __repr__(self):
        if self.section:
            return "<Offense(title=%s, section=%s)>" % \
                (self.title, self.section)
        else:
            return "<Offense(title=%s)>" % self.title


class Kind(_Base):
    __tablename__ = "kinds"
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False, default='')


def main():
    get_engine("sqlite:///test.sqlite.db")
    init_tables()

    c = Category(name="Test")
    print c

    o = Offense(title="RA1601", section="", category=c)
    print o

    print o.category

    s = get_session()
    s.add(c)

    s.commit()


if __name__ == "__main__":
    sys.exit(main())
