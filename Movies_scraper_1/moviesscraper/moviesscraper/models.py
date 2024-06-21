from sqlalchemy import TEXT, Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# table de jointure M2M entre Media et Person
media_person_association = Table('media_person_association', Base.metadata,
                                 Column('media_id', Integer, ForeignKey('medias.id')),
                                 Column('person_id', Integer, ForeignKey('persons.id')))

# table de jointure M2M entre Media et Gender
media_gender_association = Table('media_gender_association', Base.metadata,
                                 Column('media_id', Integer, ForeignKey('medias.id')),
                                 Column('gender_id', Integer, ForeignKey('genders.id')))

# table de jointure M2M entre Media et Gender
media_language_association = Table('media_language_association', Base.metadata,
                                 Column('media_id', Integer, ForeignKey('medias.id')),
                                 Column('language_id', Integer, ForeignKey('languages.id')))

class Media(Base):
    __tablename__ = 'medias'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    original_title = Column(String(255))
    description = Column(TEXT)
    score = Column(Float)
    year = Column(Integer)
    duration = Column(Integer)
    public = Column(String(255))
    country = Column(String(255))
    type = Column(String(255))

    # relation M2M avec persons
    persons = relationship('Person', secondary=media_person_association, back_populates='medias')
    # relation M2M avec genders
    genders = relationship('Gender', secondary=media_gender_association, back_populates='medias')
    # relation M2M avec languages
    languages = relationship('Language', secondary=media_language_association, back_populates='medias')
    # relation 12M avec series
    series = relationship('Serie', uselist=False, back_populates='media')

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    role = Column(String(255), nullable=False)

    # relation M2M avec medias
    medias = relationship('Media', secondary=media_person_association, back_populates='persons')

class Gender(Base):
    __tablename__ = "genders"

    id = Column(Integer, primary_key=True)
    gender = Column(String(255), nullable=True)

    # relation M2M avec medias
    medias = relationship('Media', secondary=media_gender_association, back_populates='genders')

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)
    language = Column(String(255), nullable=False)

    # relation M2M avec medias
    medias = relationship('Media', secondary=media_language_association, back_populates='languages')

class Serie(Base):
    __tablename__ = "series"

    media_id = Column(Integer, ForeignKey('medias.id'), primary_key=True)
    seasons = Column(Integer, nullable=False)
    episodes = Column(Integer)

    # relation M21 avec medias
    media = relationship('Media', back_populates='series')
