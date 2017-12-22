"""Modelo de dados necessário para app Sentinela"""
import os

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, Numeric,
                        PickleType, String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker


class MySession():
    """Para definir a sessão com o BD na aplicação. Para os
    testes, passando o parâmetro test=True, um BD na memória"""

    def __init__(self, base, test=False):
        if test:
            path = ':memory:'
        else:
            path = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), 'carga.db')
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


class Escala(Base):
    """Cópia dados sobre escala das extrações"""
    __tablename__ = 'escalas'
    id = Column(Integer, primary_key=True)
    Escala = Column(String(11), unique=True)
    CNPJAgenciaNavegacao = Column(String(14))
    CodigoIMO = Column(String(7))
    atracacoes = relationship(
        'AtracDesatracEscala', back_populates='aescala')

    """def __init__(self, numero):
        self.Escala = numero"""


class AtracDesatracEscala(Base):
    """Cópia dados sobre escala das extrações"""
    __tablename__ = 'atracacoes'
    id = Column(Integer, primary_key=True)
    Escala = Column(String(11), ForeignKey('escalas.Escala'))
    aescala = relationship(
        'Escala', back_populates='atracacoes')
    atracacao = Column(DateTime)
    desatracacao = Column(DateTime)
    CodigoTerminal = Column(String(8))
    LocalAtracacao = Column(String(50))

    """def __init__(self, escala, terminal_sigla, local):
        self.Escala = escala.numero
        self.CodigoTerminal = terminal_sigla
        self.LocalAtracacao = local"""


class Manifesto(Base):
    """Cópia dados sobre manifesto das extrações"""
    __tablename__ = 'manifestos'
    id = Column(Integer, primary_key=True)
    Manifesto = Column(String(13), unique=True)
    manifesto_conhecimentos = relationship('ManifestoConhecimento',
                                           back_populates='omanifesto')
    vazios = relationship('ContainerVazio',
                          back_populates='omanifesto')

    """def __init__(self, numero):
        self.Manifesto = numero"""


class ManifestoConhecimento(Base):
    """Cópia dados sobre manifesto e conhecimentos das extrações"""
    __tablename__ = 'manifesto_conhecimento'
    id = Column(Integer, primary_key=True)
    Manifesto = Column(String(13), ForeignKey('manifestos.Manifesto'))
    omanifesto = relationship(
        'Manifesto', back_populates='manifesto_conhecimentos')
    Conhecimento = Column(String(15), ForeignKey('conhecimentos.Conhecimento'))
    oconhecimento = relationship(
        'Conhecimento', back_populates='manifesto_conhecimentos')
    CodigoTerminalCarregamento = Column(String(8))
    NomeTerminalCarregamento = Column(String(200))
    CodigoTerminalDescarregamento = Column(String(8))
    NomeTerminalDescarregamento = Column(String(200))

    """def __init__(self, manifesto, conhecimento):
        self.Manifesto = manifesto.numero
        self.Conhecimento = conhecimento.numero"""


class Conhecimento(Base):
    """Cópia dados sobre conhecimentos das extrações"""
    __tablename__ = 'conhecimentos'
    id = Column(Integer, primary_key=True)
    Conhecimento = Column(String(15), unique=True)
    manifesto_conhecimentos = relationship(
        'ManifestoConhecimento', back_populates='oconhecimento')
    NumeroBL = Column(String(50))
    DataEmissao = Column(DateTime)
    Tipo = Column(String(4))
    ConhecimentoMaster = Column(String(100))
    CodigoPortoOrigem = Column(String(5))
    CodigoPortoDestino = Column(String(5))
    CPFCNPJConsignatario = Column(String(14))
    CPFCNPJNotificado = Column(String(14))
    DataSituacao = Column(DateTime)
    CodigoSituacao = Column(String(50))
    CodigoDocumentoDespacho = Column(String(20))
    NumeroDocumentoDespacho = Column(String(20))
    CodigoDaSituacaoDespacho = Column(String(20))
    DataSituacaoDespacho = Column(DateTime)
    CodigoRAArmazenamento = Column(String(10))
    NomeEmbarcador = Column(String(100))
    ValorFrete = Column(Numeric(asdecimal=False))
    MoedaFrete = Column(String(40))
    ModalidadeFrete = Column(String(40))
    RecolhimentoFrete = Column(String(20))
    campos = Column(PickleType)
    container = relationship(
        'Container', back_populates='oconhecimento')
    granel = relationship(
        'Granel', back_populates='oconhecimento')
    cargasolta = relationship(
        'CargaSolta', back_populates='oconhecimento')
    veiculo = relationship(
        'Veiculo', back_populates='oconhecimento')


class Container(Base):
    """Cópia dados sobre containeres das extrações"""
    __tablename__ = 'containers'
    id = Column(Integer, primary_key=True)
    Conhecimento = Column(String(15), ForeignKey('conhecimentos.Conhecimento'))
    oconhecimento = relationship(
        'Conhecimento', back_populates='container')
    Item = Column(String(4))
    Container = Column(String(11))
    Lacre1 = Column(String(15))
    Lacre2 = Column(String(15))
    Lacre3 = Column(String(15))
    Lacre4 = Column(String(15))
    Tipo = Column(String(10))
    Capacidade = Column(String(10))
    TaraContainer = Column(String(10))
    PesoBrutoItem = Column(Numeric(asdecimal=False))
    VolumeItem = Column(Numeric(asdecimal=False))
    IndicadorUsoParcial = Column(String(1))
    CodigoMercadoriaPerigosa = Column(String(10))
    CodigoClasseMercadoriaPerigosa = Column(String(10))


class CargaSolta(Base):
    """Cópia dados sobre containeres das extrações"""
    __tablename__ = 'cargasolta'
    id = Column(Integer, primary_key=True)
    Conhecimento = Column(String(15), ForeignKey('conhecimentos.Conhecimento'))
    oconhecimento = relationship(
        'Conhecimento', back_populates='cargasolta')
    Item = Column(String(4))
    TipoEmbalagem = Column(String(100))
    Quantidade = Column(String(10))
    Marca = Column(String(200))
    Contramarca = Column(String(200))
    PesoBrutoItem = Column(Numeric(asdecimal=False))
    VolumeItem = Column(Numeric(asdecimal=False))
    CodigoMercadoriaPerigosa = Column(String(10))
    CodigoClasseMercadoriaPerigosa = Column(String(10))


class Granel(Base):
    """Cópia dados sobre containeres das extrações"""
    __tablename__ = 'granel'
    id = Column(Integer, primary_key=True)
    Conhecimento = Column(String(15), ForeignKey('conhecimentos.Conhecimento'))
    oconhecimento = relationship(
        'Conhecimento', back_populates='granel')
    Item = Column(String(4))
    Tipo = Column(String(10))
    Descricao = Column(String(200))
    PesoBrutoItem = Column(Numeric(asdecimal=False))
    VolumeItem = Column(Numeric(asdecimal=False))
    CodigoMercadoriaPerigosa = Column(String(10))
    CodigoClasseMercadoriaPerigosa = Column(String(10))


class NCM(Base):
    """Cópia dados sobre containeres das extrações"""
    __tablename__ = 'ncm'
    id = Column(Integer, primary_key=True)
    Conhecimento = Column(String(15), ForeignKey('conhecimentos.Conhecimento'))
    Item = Column(String(4))
    NCM = Column(String(4))
    PesoBrutoItem = Column(Numeric(asdecimal=False))


class Veiculo(Base):
    """Cópia dados sobre containeres das extrações"""
    __tablename__ = 'veiculo'
    id = Column(Integer, primary_key=True)
    Conhecimento = Column(String(15), ForeignKey('conhecimentos.Conhecimento'))
    oconhecimento = relationship(
        'Conhecimento', back_populates='veiculo')
    Item = Column(String(4))
    Chassi = Column(String(50))
    Marca = Column(String(200))
    Contramarca = Column(String(200))


class ContainerVazio(Base):
    """Cópia dados sobre containeres das extrações"""
    __tablename__ = 'containervazio'
    id = Column(Integer, primary_key=True)
    Manifesto = Column(String(13), ForeignKey('manifestos.Manifesto'))
    omanifesto = relationship(
        'Manifesto', back_populates='vazios')
    Container = Column(String(11))
    NomeTipo = Column(String(50))
    Capacidade = Column(String(2))
    Tara = Column(Numeric(asdecimal=False))
