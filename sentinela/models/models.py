"""Modelo de dados necessário para app Sentinela"""
import enum
import os

from sqlalchemy import (Column, Enum, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker


class Filtro(enum.Enum):
    """Enumerado para escolha do tipo de filtro a ser
    aplicado no parâmetro de risco"""
    igual = 1
    comeca_com = 2
    contem = 3


class MySession():
    """Para definir a sessão com o BD na aplicação. Para os
    testes, passando o parâmetro test=True, um BD na memória"""
    def __init__(self, base, test=False):
        if test:
            path = ':memory:'
        else:
            path = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'sentinela.db')
            if os.name != 'nt':
                path = '/' + path
        self._engine = create_engine('sqlite:///' + path, convert_unicode=True)
        Session = sessionmaker(bind=self._engine)
        if test:
            self._session = Session()
        else:
            self._session = scoped_session(Session)
            base.metadata.bind = self._engine

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine


Base = declarative_base()


class ParametroRisco(Base):
    """Nomeia um parâmetro de risco que pode ser aplicado
    como filtro em um Banco de Dados. Um parâmetro tem uma
    lista de valores que serão o filtro efetivo"""
    __tablename__ = 'parametrosrisco'
    id = Column(Integer, primary_key=True)
    nome_campo = Column(String(20), unique=True)
    descricao = Column(String(200), unique=True)
    valores = relationship('ValorParametro', back_populates='risco')

    def __init__(self, nome, descricao=''):
        self.nome = nome
        self.descricao = descricao


class ValorParametro(Base):
    """Um valor de parametro a ser aplicado como filtro em uma
    fonte de dados
    nomecampo = nome do campo da fonte de dados
        a ser aplicado filtro
    tipofiltro = tipo de função de filtragem a ser
        realizada (ver enum TipoFiltro)"""
    __tablename__ = 'valoresparametro'
    id = Column(Integer, primary_key=True)
    valor = Column(String(50), unique=True)
    tipo_filtro = Column(Enum(Filtro))
    risco_id = Column(Integer, ForeignKey('parametrosrisco.id'))
    risco = relationship(
        'ParametroRisco', back_populates='valores')

    def __init__(self, nome, tipo):
        self.nome_campo = nome
        self.tipo_filtro = tipo
