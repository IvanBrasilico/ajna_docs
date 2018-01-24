""" mysession = MySession(nomebase='cargatest.db')
    dbsession = mysession.session
    engine = mysession.engine
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    escala = Escala()
    escala.Escala = 'E-1'
    escala.CNPJAgenciaNavegacao = 'E-C01'
    escala.CodigoIMO = 'E-IMO01'
    dbsession.add(escala)
    atracacao = AtracDesatracEscala()
    atracacao.Escala = 'E-1'
    atracacao.CodigoTerminal = 'A-T01'
    dbsession.add(atracacao)
    manifesto = Manifesto()
    manifesto.Manifesto = 'M-2'
    dbsession.add(manifesto)
    escalamanifesto = EscalaManifesto()
    escalamanifesto.Escala = 'E-1'
    escalamanifesto.Manifesto = 'M-2'
    dbsession.add(escalamanifesto)
    vazio = ContainerVazio()
    vazio.Manifesto = 'M-2'
    vazio.Container = 'C-C01'
    vazio.Capacidade = 'C-40'
    dbsession.add(vazio)
    vazio2 = ContainerVazio()
    vazio2.Manifesto = 'M-2'
    vazio2.Container = 'C-C02'
    vazio2.Capacidade = 'C-40'
    dbsession.add(vazio2)
    dbsession.commit()"""